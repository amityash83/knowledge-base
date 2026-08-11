# 📘 Runbook: PostgreSQL RDS Setup for Application 

## 🎯 Objective
This runbook provides step-by-step instructions to:
- Create a PostgreSQL database and user in AWS RDS
- Configure proper permissions
- Fix common errors
- Connect application (Docker / Backend) to RDS

---

## 🧱 Prerequisites
- AWS RDS PostgreSQL instance created
- RDS endpoint available
- Access to:
  - pgAdmin OR psql
  - RDS master user credentials
- Security Group allows inbound access on port `5432`

---

## 🔐 Step 1: Connect to RDS

### Using psql:
```bash
psql -h <rds-endpoint> -U <master-user> -d postgres
```
```
```

🗄️ Step 2: Create Database
```SQL
CREATE DATABASE agentwatch_db;
```

👤 Step 3: Create User (IMPORTANT: WITH LOGIN)
```sql
CREATE USER agentwatch_user 
WITH LOGIN 
PASSWORD 'StrongPassword123';
```

🔑 Step 4: Grant Database Privileges
```SQL
GRANT ALL PRIVILEGES ON DATABASE agentwatch_db TO agentwatch_user;
```

🔄 Step 5: Connect to New Database
```sql
\c agentwatch_db
```

🧩 Step 6: Fix Schema Ownership (CRITICAL)
```sql
ALTER SCHEMA public OWNER TO agentwatch_user;
```

🔓 Step 7: Grant Schema Permissions
```SQL
GRANT ALL ON SCHEMA public TO agentwatch_user;
GRANT USAGE, CREATE ON SCHEMA public TO agentwatch_user;
```

🔁 Step 8: Set Default Privileges (Future Tables)
```SQL
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO agentwatch_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO agentwatch_user;
```

🧪 Step 9: Verify Access
```SQL
SET ROLE agentwatch_user;

CREATE TABLE test_table (id INT);
DROP TABLE test_table;
```
✅ If successful → Setup is correct


⚠️ Common Errors & Fixes
❌ permission denied for schema public
```sql
GRANT ALL ON SCHEMA public TO agentwatch_user;
ALTER SCHEMA public OWNER TO agentwatch_user;
```

❌ role is not permitted to log in
```SQL
ALTER USER agentwatch_user WITH LOGIN;
```
OR
```SQL
DROP USER IF EXISTS agentwatch_user;

CREATE USER agentwatch_user 
WITH LOGIN 
PASSWORD 'StrongPassword123';
```


❌ connection timeout / refused
- Check Security Group (port 5432)
- Verify RDS endpoint
- Ensure correct VPC / public access

❌ authentication failed
```SQL
ALTER USER agentwatch_user WITH PASSWORD 'newpassword';
```



🧠 Best Practices
- Do NOT use RDS master user in application
- Always:
    - Set schema owner
    - Grant default privileges
- Use AWS Secrets Manager or SSM Parameter Store
- Enable connection pooling (PgBouncer)
- Add retry logic in backend


🛠️ Reusable SQL Template
```SQL
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







