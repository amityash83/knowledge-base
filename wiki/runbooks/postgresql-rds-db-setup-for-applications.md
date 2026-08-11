---
title: PostgreSQL RDS Setup for Applications
type: runbook
domain: [devops]
status: stable
tags: [runbook, postgresql, rds, aws]
sources: [raw-sources/archive/postgresql-rds-db-setup-for-applications.md]
created: 2026-08-11
updated: 2026-08-11
---

# PostgreSQL RDS Setup for Applications

## Summary
Step-by-step instructions to create a PostgreSQL database and user in AWS RDS, configure proper permissions, fix common errors, and connect an application (Docker/backend) to RDS.

## Prerequisites
- AWS RDS PostgreSQL instance created
- RDS endpoint available
- Access to `psql` (or pgAdmin) and RDS master user credentials
- Security Group allows inbound access on port `5432`

## Steps

### 1. Connect to RDS
```bash
psql -h <rds-endpoint> -U <master-user> -d postgres
```

### 2. Create database
```sql
CREATE DATABASE agentwatch_db;
```

### 3. Create user (must include `WITH LOGIN`)
```sql
CREATE USER agentwatch_user
WITH LOGIN
PASSWORD 'StrongPassword123';
```

### 4. Grant database privileges
```sql
GRANT ALL PRIVILEGES ON DATABASE agentwatch_db TO agentwatch_user;
```

### 5. Connect to the new database
```sql
\c agentwatch_db
```

### 6. Fix schema ownership (critical)
```sql
ALTER SCHEMA public OWNER TO agentwatch_user;
```

### 7. Grant schema permissions
```sql
GRANT ALL ON SCHEMA public TO agentwatch_user;
GRANT USAGE, CREATE ON SCHEMA public TO agentwatch_user;
```

### 8. Set default privileges for future tables
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO agentwatch_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO agentwatch_user;
```

### 9. Verify access
```sql
SET ROLE agentwatch_user;

CREATE TABLE test_table (id INT);
DROP TABLE test_table;
```
If this succeeds, setup is correct.

## Common Errors & Fixes

**`permission denied for schema public`**
```sql
GRANT ALL ON SCHEMA public TO agentwatch_user;
ALTER SCHEMA public OWNER TO agentwatch_user;
```

**`role is not permitted to log in`**
```sql
ALTER USER agentwatch_user WITH LOGIN;
```
or recreate the user:
```sql
DROP USER IF EXISTS agentwatch_user;

CREATE USER agentwatch_user
WITH LOGIN
PASSWORD 'StrongPassword123';
```

**Connection timeout / refused**
- Check Security Group (port 5432)
- Verify RDS endpoint
- Ensure correct VPC / public access

**Authentication failed**
```sql
ALTER USER agentwatch_user WITH PASSWORD 'newpassword';
```

## Best Practices
- Do NOT use the RDS master user in the application
- Always set schema owner and grant default privileges
- Use AWS Secrets Manager or SSM Parameter Store for credentials
- Enable connection pooling (PgBouncer)
- Add retry logic in the backend

## Reusable Template
```sql
CREATE DATABASE {{DB_NAME}};

CREATE USER {{DB_USER}} WITH LOGIN PASSWORD '{{DB_PASS}}';

GRANT ALL PRIVILEGES ON DATABASE {{DB_NAME}} TO {{DB_USER}};

\c {{DB_NAME}}

ALTER SCHEMA public OWNER TO {{DB_USER}};

GRANT ALL ON SCHEMA public TO {{DB_USER}};
GRANT USAGE, CREATE ON SCHEMA public TO {{DB_USER}};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO {{DB_USER}};

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO {{DB_USER}};
```

## Open questions
- None; this runbook has been used and verified against a real setup (`agentwatch_db`).

## Related
- [[kubernetes-cluster-fundamentals]]
- [[devops-lab-platform-foundation]]
