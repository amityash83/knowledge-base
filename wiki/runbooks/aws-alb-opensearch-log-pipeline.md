---
title: AWS ALB Logs to OpenSearch Pipeline
type: runbook
domain: [devops]
status: stable
tags: [runbook, aws, alb, opensearch, fluent-bit, logging, observability]
sources: [raw-sources/archive/aws-alb-opensearch-log-pipeline-runbook.md]
created: 2026-08-11
updated: 2026-08-11
---

# AWS ALB Logs to OpenSearch Pipeline

## Summary
A complete log-ingestion pipeline for AWS Application Load Balancer logs stored in S3. Pulls ALB logs from S3, extracts them locally, forwards them through Fluent Bit, stores them in OpenSearch, and visualizes them in OpenSearch Dashboards. ALB access logs in S3 aren't directly queryable — this runbook makes them searchable and visualizable.

## Prerequisites
- An S3 bucket receiving ALB access logs
- Docker and Docker Compose
- AWS credentials with read access to the log bucket (`~/.aws` mounted read-only)

## Architecture
```text
S3 -> Sync Container -> Local Logs -> Fluent Bit -> OpenSearch -> Dashboards
```
- The `s3-sync` container polls S3 every 60 seconds and copies files into the local `logs/` directory.
- Compressed `.gz` ALB log files are expanded into `.log` files for Fluent Bit processing.
- Fluent Bit tails the extracted log files and forwards records to OpenSearch.
- OpenSearch indexes the logs; OpenSearch Dashboards exposes ad hoc search and visualization.

## Steps

### 1. Docker Compose stack
Four services: OpenSearch, OpenSearch Dashboards, an AWS CLI–based S3 sync container, and Fluent Bit.

```yaml
version: "3.8"

services:

  opensearch:
    image: opensearchproject/opensearch:2.12.0
    container_name: opensearch
    environment:
      - discovery.type=single-node
      - DISABLE_SECURITY_PLUGIN=true
      - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    volumes:
      - opensearch-data:/usr/share/opensearch/data

  dashboards:
    image: opensearchproject/opensearch-dashboards:2.12.0
    container_name: dashboards
    environment:
      - OPENSEARCH_HOSTS=["http://opensearch:9200"]
      - DISABLE_SECURITY_DASHBOARDS_PLUGIN=true
    ports:
      - "5601:5601"

  s3-sync:
    image: ubuntu:22.04
    container_name: s3-sync
    volumes:
      - ./logs:/logs
      - ~/.aws:/root/.aws:ro
    environment:
      - AWS_PROFILE=realt
      - AWS_DEFAULT_REGION=us-west-2
      - DEBIAN_FRONTEND=noninteractive
    command: >
      bash -c "
        apt update &&
        apt install -y awscli gzip &&
        ln -fs /usr/share/zoneinfo/UTC /etc/localtime &&
        while true; do
          echo 'Syncing logs...' &&
          aws s3 sync s3://YOUR_BUCKET/AWSLogs/ /logs &&
          find /logs -name '*.gz' -exec gunzip -c {} > {}.log \; &&
          sleep 60;
        done
      "

  fluent-bit:
    image: fluent/fluent-bit:2.2
    container_name: fluent-bit
    volumes:
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
      - ./parsers.conf:/fluent-bit/etc/parsers.conf
      - ./logs:/logs
      - ./state:/tmp/fluentbit

volumes:
  opensearch-data:
```

### 2. Fluent Bit configuration
`fluent-bit.conf`
```ini
[SERVICE]
    Flush        5
    Log_Level    info

[INPUT]
    Name              tail
    Path              /logs/*/elasticloadbalancing/*/*/*/*/*.log
    Tag               alb
    Read_from_Head    On
    Refresh_Interval  5
    DB                /dev/null

[OUTPUT]
    Name                opensearch
    Match               *
    Host                opensearch
    Port                9200
    Index               alb-logs
    Logstash_Format     On
    Suppress_Type_Name  On
```

`parsers.conf`
```ini
[PARSER]
    Name        alb
    Format      regex
    Regex       ^(?<type>[^ ]*) (?<time>[^ ]*) (?<elb>[^ ]*) (?<client>[^ ]*):(?<port>[^ ]*) (?<target>[^ ]*) (?<request_processing_time>[^ ]*) (?<target_processing_time>[^ ]*) (?<response_processing_time>[^ ]*) (?<elb_status_code>[^ ]*) (?<target_status_code>[^ ]*) (?<received_bytes>[^ ]*) (?<sent_bytes>[^ ]*) "(?<request>[^"]*)" "(?<user_agent>[^"]*)"
    Time_Key    time
    Time_Format %Y-%m-%dT%H:%M:%S.%LZ
```

### 3. Run setup
```bash
docker-compose down -v
rm -rf logs state
mkdir logs state
docker-compose up -d
```

### 4. Verify ingestion
```bash
docker logs -f fluent-bit
curl localhost:9200/_cat/indices?v
```
Expected index pattern: `logstash-YYYY.MM.DD`

### 5. Single-node replica fix
Single-node OpenSearch shows yellow health because replicas can't be assigned. Fix:
```bash
curl -X PUT "localhost:9200/logstash-*/_settings" \
  -H 'Content-Type: application/json' \
  -d '{"index":{"number_of_replicas":0}}'
```

### 6. Access OpenSearch Dashboards
Open `http://localhost:5601`, create an index pattern `logstash-*`, and use `@timestamp` as the time field.

## Folder Layout
```text
project/
├── docker-compose.yml
├── fluent-bit.conf
├── parsers.conf
├── logs/
└── state/
```

## Common Errors & Fixes
- **Yellow index health** — expected for single-node deployments unless replicas are set to `0` (see step 5).
- **ALB `.gz` files not ingesting** — they must be extracted to `.log` before tail-based ingestion works; confirm the `s3-sync` container's `gunzip` step is running.
- **Fluent Bit not re-tailing after restart** — expected, since `DB /dev/null` disables offset persistence; see Future Improvements below if this becomes a problem.
- **Log paths not matching** — deep S3 log paths require an explicit recursive path pattern in the Fluent Bit `[INPUT]` `Path`.

## Important Notes
- ALB log delivery from S3 is delayed roughly 5–10 minutes; this pipeline is not real-time.
- OpenSearch 2.x does not use the legacy `_type` mapping approach.
- The current tail input configuration does not persist read offsets across restarts (by design, via `DB /dev/null`).

## Future Improvements
- Persist Fluent Bit state across restarts:
  ```ini
  DB /tmp/fluentbit/tail.db
  ```
- Move to an event-driven design for lower latency and better scalability:
  ```text
  S3 -> SQS -> Fluent Bit -> OpenSearch
  ```

## MCP Task Shape
```yaml
task: deploy-alb-logs-opensearch-pipeline
steps:
  - provision opensearch and dashboards
  - configure s3 sync container
  - configure fluent bit input and output
  - start docker compose stack
  - verify log ingestion
  - create dashboard index pattern
```
See [[mcp-architecture]] for what a task shape like this plugs into.

## Open questions
- Whether to adopt the SQS event-driven redesign noted under Future Improvements hasn't been decided.

## Related
- [[aiops]]
- [[mcp-architecture]]
- [[kubernetes-cluster-fundamentals]]
