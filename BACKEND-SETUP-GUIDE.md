# SW360 Backend Setup Guide

Complete guide to setting up Eclipse SW360 backend for license curation using Docker.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Starting the Backend](#starting-the-backend)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

1. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Verify installation: `docker --version`
   - Verify Docker Compose: `docker compose version`

2. **Git** installed
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

3. **System Requirements**
   - At least 4GB RAM available for Docker
   - 10GB free disk space
   - Windows 10/11, macOS, or Linux

---

## Installation Steps

### Step 1: Clone SW360 Stable Version

```bash
cd C:\Users\Arkajyoti\Desktop\SW360
git clone --branch sw360-18.1.0-M1 https://github.com/eclipse-sw360/sw360.git sw360-stable
cd sw360-stable
```

**What this does:**
- Clones the stable SW360 release (version 18.1.0-M1)
- This version has been tested and is more reliable than beta versions

---

### Step 2: Configure Docker Compose

Edit the `docker-compose.yml` file to add CouchDB credentials:

```yaml
couchdb:
  image: couchdb
  ports:
    - "5984:5984"
  environment:
    - COUCHDB_USER=admin
    - COUCHDB_PASSWORD=password
  volumes:
    - couchdb-data:/opt/couchdb/data
  networks:
    - sw360-network
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5984"]
    interval: 30s
    timeout: 10s
    retries: 5
```

**Why this is needed:**
- CouchDB 3.0+ requires authentication (no more "Admin Party" mode)
- Sets up admin credentials: `admin` / `password`
- Health check ensures CouchDB is ready before SW360 starts

---

### Step 3: Start Docker Services

```bash
cd C:\Users\Arkajyoti\Desktop\SW360\sw360-stable
docker compose up -d
```

**Expected output:**
```
[+] Running 3/3
 ✔ Container sw360-stable-couchdb-1     Started
 ✔ Container sw360-stable-postgresdb-1  Started
 ✔ Container sw360                      Started
```

**What this does:**
- `-d` flag runs containers in detached mode (background)
- Starts 3 containers:
  - `couchdb`: Document database for SW360 data
  - `postgresdb`: Relational database for Liferay portal
  - `sw360`: Main Spring Boot application

**Time to start:**
- First time: 2-5 minutes (downloading images)
- Subsequent starts: 30-60 seconds

---

### Step 4: Monitor Container Startup

Watch the logs to ensure services start successfully:

```bash
# Watch all logs
docker compose logs -f

# Watch specific service
docker compose logs -f sw360

# Check container status
docker ps
```

**Wait for this message in logs:**
```
INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [XXXXX] milliseconds
```

---

## Configuration

### CouchDB Credentials Update

The SW360 container needs to be configured with the correct CouchDB credentials.

**Option A: Using Docker Exec (Recommended)**

```bash
# Access the running container
docker exec -it sw360 bash

# Edit couchdb.properties
vi /etc/sw360/couchdb.properties
```

Update the following lines:
```properties
couchdb.user = admin
couchdb.password = password
couchdb.url = http://couchdb:5984
couchdb.database = sw360db
```

**Option B: Environment Variables**

Add to `docker-compose.yml` under `sw360` service:
```yaml
sw360:
  environment:
    - COUCHDB_USER=admin
    - COUCHDB_PASSWORD=password
    - COUCHDB_URL=http://couchdb:5984
```

### Restart After Configuration

```bash
docker restart sw360
```

Wait 30-60 seconds for the service to restart.

---

## Verification

### 1. Check Container Status

```bash
docker ps
```

**Expected output:**
```
NAMES                       IMAGE                    STATUS
sw360                       ghcr.io/eclipse-sw360    Up X hours
sw360-stable-postgresdb-1   postgres:16              Up X hours (healthy)
sw360-stable-couchdb-1      couchdb                  Up X hours (healthy)
```

All containers should show "Up" and databases should show "(healthy)".

---

### 2. Test CouchDB Access

**Via curl (Git Bash/WSL):**
```bash
curl -u admin:password http://localhost:5984
```

**Via curl (PowerShell):**
```powershell
curl.exe -u admin:password http://localhost:5984
```

**Expected response:**
```json
{
  "couchdb": "Welcome",
  "version": "3.4.2",
  "git_sha": "...",
  "uuid": "...",
  "features": [...]
}
```

---

### 3. Test CouchDB Web Interface

Open browser and go to: **http://localhost:5984/_utils**

**Login credentials:**
- Username: `admin`
- Password: `password`

You should see the Fauxton interface with databases:
- sw360db
- sw360attachments
- sw360changelogs
- sw360users
- and more...

---

### 4. List All Databases

**Git Bash/WSL:**
```bash
curl -s -u admin:password http://localhost:5984/_all_dbs
```

**PowerShell:**
```powershell
curl.exe -s -u admin:password http://localhost:5984/_all_dbs
```

**Expected output:**
```json
[
  "_replicator",
  "_users",
  "sw360attachments",
  "sw360changelogs",
  "sw360components",
  "sw360db",
  "sw360licenses",
  "sw360projects",
  "sw360users",
  ...
]
```

---

### 5. Test Backend API (Optional)

Check if the REST API is accessible:

```bash
curl -s http://localhost:8080/health
```

or

```bash
curl -s http://localhost:8080/actuator/health
```

**Note:** Most REST API endpoints require OAuth2 authentication, which is why we use direct CouchDB access for license curation.

---

## Database Structure for Licenses

### License Document Format

Licenses are stored in the `sw360db` database as JSON documents:

```json
{
  "_id": "1301e495e309a30f9e304974aa000fe2",
  "_rev": "2-abc123...",
  "type": "license",
  "fullName": "MIT License",
  "shortName": "MIT",
  "text": "Permission is hereby granted...",
  "OSIApproved": true,
  "checked": true
}
```

**Key fields:**
- `_id`: Unique identifier (auto-generated)
- `_rev`: Revision number (required for updates)
- `type`: Must be "license" to identify this as a license document
- `fullName`: Full license name
- `shortName`: SPDX identifier (e.g., MIT, Apache-2.0, GPL-3.0)
- `text`: Full license text
- `OSIApproved`: Boolean - is this OSI approved?
- `checked`: Boolean - has this been reviewed/approved?

---

## Troubleshooting

### Issue 1: Container Won't Start

**Symptoms:**
```
Error: port 5984 already in use
```

**Solution:**
```bash
# Check what's using the port
netstat -ano | findstr :5984

# Kill the process (Windows)
taskkill /F /PID <process_id>

# Or stop old containers
docker ps -a
docker stop <container_name>
docker rm <container_name>
```

---

### Issue 2: CouchDB Authentication Errors

**Symptoms:**
```json
{"error":"unauthorized","reason":"Name or password is incorrect."}
```

**Solution 1:** Verify credentials in docker-compose.yml
```bash
docker compose down
# Edit docker-compose.yml to add COUCHDB_USER and COUCHDB_PASSWORD
docker compose up -d
```

**Solution 2:** Reset CouchDB data
```bash
docker compose down -v  # WARNING: Deletes all data!
docker compose up -d
```

---

### Issue 3: SW360 Container Crashes

**Check logs:**
```bash
docker compose logs sw360
```

**Common causes:**
1. CouchDB not ready when SW360 starts
   - Solution: Wait longer, check CouchDB health
2. Incorrect CouchDB credentials in SW360 config
   - Solution: Update /etc/sw360/couchdb.properties
3. Port conflicts
   - Solution: Change ports in docker-compose.yml

---

### Issue 4: Database Not Created

**Symptoms:**
- sw360db database doesn't exist

**Solution:**
```bash
# SW360 auto-creates databases on first start
# Force recreation:
docker restart sw360

# Or create manually:
curl -X PUT -u admin:password http://localhost:5984/sw360db
```

---

### Issue 5: Docker Compose Command Not Found

**Symptoms:**
```
docker-compose: command not found
```

**Solution:**
Use `docker compose` (with space) instead of `docker-compose` (with hyphen):
```bash
docker compose up -d
```

Docker Compose V2 is now integrated into Docker CLI.

---

## Useful Commands Reference

### Container Management
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart a specific service
docker restart sw360

# View logs
docker compose logs -f

# Check container status
docker ps

# Access container shell
docker exec -it sw360 bash
```

### CouchDB Operations
```bash
# Test connection
curl -u admin:password http://localhost:5984

# List databases
curl -s -u admin:password http://localhost:5984/_all_dbs

# Access web UI
# Open: http://localhost:5984/_utils
```

### Port Reference
```
- 5984: CouchDB HTTP API and Fauxton UI
- 5438: PostgreSQL database
- 8080: SW360 REST API (requires OAuth2)
```

---

## Next Steps

Now that your backend is running, proceed to license curation:

1. **Direct CouchDB Access** (Recommended)
   - See: `COUCHDB-LICENSE-CURATION-GUIDE.md`
   - Use CouchDB web interface or curl commands
   - Full CRUD operations on licenses

2. **Command-Line Tools**
   - PowerShell: See `powershell-commands.md`
   - Bash/WSL: See `linux-wsl-commands.sh`
   - Quick reference: `quick-reference.txt`

3. **CouchDB Web Interface**
   - Open: http://localhost:5984/_utils
   - Login: admin / password
   - Navigate to sw360db database
   - Visual interface for license management

---

## Summary

You now have:
- ✅ SW360 backend running in Docker
- ✅ CouchDB accessible at http://localhost:5984
- ✅ PostgreSQL for Liferay support
- ✅ All databases initialized
- ✅ Authentication configured
- ✅ Ready for license curation operations

**Backend is fully operational and ready for license management via direct CouchDB access.**

---

## Support & Documentation

- SW360 Documentation: https://eclipse.dev/sw360/docs/
- CouchDB Documentation: https://docs.couchdb.org/
- Docker Documentation: https://docs.docker.com/

For license curation operations, refer to:
- `COUCHDB-LICENSE-CURATION-GUIDE.md` - Comprehensive license management guide
- `powershell-commands.md` - Windows/PowerShell commands
- `linux-wsl-commands.sh` - Linux/WSL/Git Bash commands
- `quick-reference.txt` - Quick command reference
