---
title: AWS ALB Logs to OpenSearch Pipeline Runbook
tags: [runbook, aws, alb, opensearch, fluent-bit, logging]
domain: observability
difficulty: intermediate
created: 2026-04-10
updated: 2026-04-10
---

# AWS ALB Logs to OpenSearch Pipeline Runbook

## Context
This runbook documents a complete log ingestion pipeline for AWS Application Load Balancer logs stored in Amazon S3. The pipeline pulls ALB logs from S3, extracts them locally, forwards them through Fluent Bit, stores them in OpenSearch, and visualizes them in OpenSearch Dashboards.

## Problem
ALB access logs in S3 are useful for traffic analysis, debugging, and performance monitoring, but they are not directly queryable for operational workflows. A repeatable ingestion setup is needed to move S3-hosted ALB logs into a searchable and visualizable platform.

## Solution
Use a Docker Compose stack with four services:

- OpenSearch for log indexing and search
- OpenSearch Dashboards for visualization
- Fluent Bit for log tailing and forwarding
- An AWS CLI-based sync container to continuously pull logs from S3

This creates the following operational flow:

```text
S3 -> Sync Container -> Local Logs -> Fluent Bit -> OpenSearch -> Dashboards
```

## Commands / Config

### Docker Compose
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

### Fluent Bit Configuration
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

### Run Setup
```bash
docker-compose down -v
rm -rf logs state
mkdir logs state
docker-compose up -d
```

### Verification Commands
```bash
docker logs -f fluent-bit
curl localhost:9200/_cat/indices?v
```

### Single-Node Replica Fix
```bash
curl -X PUT "localhost:9200/logstash-*/_settings" \
  -H 'Content-Type: application/json' \
  -d '{"index":{"number_of_replicas":0}}'
```

## Architecture / Design
- AWS S3 stores raw ALB access logs.
- The `s3-sync` container polls S3 every 60 seconds and copies files into the local `logs/` directory.
- Compressed `.gz` ALB log files are expanded into `.log` files for Fluent Bit processing.
- Fluent Bit tails the extracted log files and forwards records to OpenSearch.
- OpenSearch indexes the logs and exposes them to OpenSearch Dashboards.
- OpenSearch Dashboards provides a UI for ad hoc search, dashboards, and visual analysis.

## Folder / File Layout
```text
project/
├── docker-compose.yml
├── fluent-bit.conf
├── parsers.conf
├── logs/
└── state/
```

## Verification

### Check Fluent Bit ingestion
```bash
docker logs -f fluent-bit
```

### Check OpenSearch indices
```bash
curl localhost:9200/_cat/indices?v
```

Expected index pattern:

```text
logstash-YYYY.MM.DD
```

### Access OpenSearch Dashboards
```text
http://localhost:5601
```

Create index pattern:

```text
logstash-*
```

Use time field:

```text
@timestamp
```

## Learnings
- Fluent Bit can re-ingest logs after restart when the tail database is disabled with `DB /dev/null`.
- OpenSearch 2.x does not use the legacy `_type` mapping approach.
- ALB `.gz` log files must be extracted before tail-based ingestion works.
- Deep log paths require an explicit recursive path pattern in the Fluent Bit input configuration.
- Single-node OpenSearch setups often show yellow health because replicas cannot be assigned.

## Important Notes
- Yellow index health is expected for a single-node deployment unless replicas are set to `0`.
- ALB log delivery from AWS S3 is delayed by roughly 5 to 10 minutes and is not real-time.
- The current tail input configuration does not persist read offsets across restarts.

## Future Improvements
- Persist Fluent Bit state with:

```ini
DB /tmp/fluentbit/tail.db
```

- Move to an event-driven ingestion design:

```text
S3 -> SQS -> Fluent Bit -> OpenSearch
```

Benefits:
- lower latency
- better scalability
- cleaner event-driven processing

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

## Related
- [[platform-reference-map]]
- [[ops-vault-bootstrap-log]]
- [[llm-rag-basic-concepts]]

## Tags
#runbook #aws #alb #opensearch #fluent-bit #logging #observability
