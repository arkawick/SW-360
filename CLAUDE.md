# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains Eclipse SW360 license curation setup with direct CouchDB access. The primary workflow uses **CouchDB directly** rather than the SW360 REST API, as the stable backend (v18.1.0-M1) requires OAuth2 authentication that's difficult to obtain without the Liferay portal.

## Architecture

### Three-Layer System

1. **Backend Layer** (`sw360-stable/`)
   - SW360 Spring Boot application (port 8080)
   - CouchDB database (port 5984) - Primary data store
   - PostgreSQL database (port 5438) - Liferay portal data
   - Deployed via Docker Compose

2. **Data Access Layer** (Root directory)
   - Python module (`sw360_license_manager.py`) - Primary programmatic interface
   - Direct CouchDB HTTP API access via curl
   - CouchDB Fauxton web UI (http://localhost:5984/_utils)

3. **Documentation Layer**
   - Setup guides (BACKEND-SETUP-GUIDE.md, PYTHON-README.md)
   - Platform-specific commands (powershell-commands.md, linux-wsl-commands.sh)
   - Complete API reference (PYTHON-USAGE-GUIDE.md, COUCHDB-LICENSE-CURATION-GUIDE.md)

### Data Model

Licenses are stored as JSON documents in CouchDB `sw360db` database:

```json
{
  "_id": "auto-generated-uuid",
  "_rev": "revision-number",
  "type": "license",
  "fullName": "MIT License",
  "shortName": "MIT",
  "text": "License text...",
  "OSIApproved": true,
  "checked": false
}
```

Key fields:
- `type: "license"` - Required for license documents
- `_rev` - Required for updates/deletes (CouchDB optimistic locking)
- `shortName` - SPDX identifier used for searching
- `checked` - Review/approval status

## Commands

### Backend Management

**Start services:**
```bash
cd sw360-stable
docker compose up -d
```

**Stop services:**
```bash
docker compose down
```

**View logs:**
```bash
docker compose logs -f
docker compose logs -f sw360
docker compose logs -f couchdb
```

**Restart specific service:**
```bash
docker restart sw360
docker restart sw360-stable-couchdb-1
```

**Check service status:**
```bash
docker ps
```

### Python License Operations

**Run test suite:**
```python
python sw360_license_manager.py
```

**Run examples:**
```python
python example_usage.py
```

**Interactive usage:**
```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# List all licenses
licenses = manager.list_licenses()

# Create license
manager.create_license(
    full_name="MIT License",
    short_name="MIT",
    text="...",
    osi_approved=True,
    checked=False
)

# Find by SPDX ID
mit = manager.find_by_short_name("MIT")

# Get by document ID
license = manager.get_license("license_id")

# Update (requires current _rev)
manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],
    full_name=license['fullName'],
    short_name=license['shortName'],
    text=license['text'],
    osi_approved=license['OSIApproved'],
    checked=True
)

# Statistics
total = manager.count_licenses()
osi_approved = manager.get_osi_approved_licenses()
checked = manager.get_checked_licenses()
unchecked = manager.get_unchecked_licenses()
```

### Direct CouchDB Access

**PowerShell:**
```powershell
# List licenses
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"}}"

# Create license
curl.exe -X POST "http://admin:password@localhost:5984/sw360db" `
  -H "Content-Type: application/json" `
  -d "{\"type\":\"license\",\"fullName\":\"MIT\",\"shortName\":\"MIT\",\"OSIApproved\":true}"
```

**Git Bash/WSL:**
```bash
# List licenses
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'

# Source helper functions
source linux-wsl-commands.sh
create_license "MIT License" "MIT" "License text..."
```

## Important Constraints

### Authentication Compatibility Issue

- **Frontend** (sw360-frontend, port 3000): Uses Basic Auth, incompatible with stable backend
- **Backend REST API** (port 8080): Requires OAuth2 tokens, not accessible without Liferay
- **Solution**: Use direct CouchDB access (recommended approach)

### CouchDB Revision Handling

CouchDB uses optimistic locking via `_rev` field:
1. Always fetch current document before updating
2. Include current `_rev` in update/delete requests
3. If `_rev` is stale, request fails with HTTP 409
4. Re-fetch document and retry

**Correct update pattern:**
```python
# Fetch current state
license = manager.get_license(license_id)

# Update using current revision
manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],  # Must be current!
    ...
)
```

### Platform-Specific curl Syntax

**Windows PowerShell:**
- Use `curl.exe` not `curl` (PowerShell has its own curl alias)
- Escape JSON double quotes: `\"`
- Line continuation: backtick `` ` ``

**Git Bash/WSL/Linux:**
- Use `curl` with `-u username:password` flag
- Single quotes for JSON strings
- Line continuation: backslash `\`

## Development Workflow

### Adding New License

1. Check if license exists:
   ```python
   existing = manager.find_by_short_name("GPL-3.0")
   ```

2. Create if not exists:
   ```python
   if not existing:
       manager.create_license(...)
   ```

3. Verify creation:
   ```python
   new_license = manager.find_by_short_name("GPL-3.0")
   ```

### Bulk Import

```python
licenses_data = [
    {"full_name": "MIT", "short_name": "MIT", ...},
    {"full_name": "Apache-2.0", "short_name": "Apache-2.0", ...},
]

for lic in licenses_data:
    try:
        manager.create_license(**lic)
        print(f"Created: {lic['short_name']}")
    except Exception as e:
        print(f"Failed: {e}")
```

### License Review Workflow

1. Get unchecked licenses:
   ```python
   unchecked = manager.get_unchecked_licenses()
   ```

2. Review and mark as checked:
   ```python
   for license in unchecked:
       # Review logic here
       manager.update_license(
           license_id=license['_id'],
           rev=license['_rev'],
           ...
           checked=True
       )
   ```

## Configuration

### CouchDB Credentials

- URL: `http://localhost:5984`
- Username: `admin`
- Password: `password`
- Database: `sw360db`

Configured in:
- `sw360-stable/docker-compose.yml` (lines 58-59)
- Python module default parameters
- All curl examples

### Docker Volumes

Persistent data stored in named volumes:
- `postgres:/var/lib/postgresql/data/` - Liferay data
- `couchdb:/opt/couchdb/data` - License documents
- `etc:/etc/sw360` - SW360 configuration
- `document_library:/app/sw360/data/document_library` - Attachments

### Port Mapping

- 8080: SW360 REST API (requires OAuth2)
- 5984: CouchDB HTTP API (direct access)
- 5438: PostgreSQL (Liferay portal)

## Troubleshooting

### Container Won't Start

Check for port conflicts:
```bash
netstat -ano | findstr :5984
netstat -ano | findstr :8080
```

View detailed logs:
```bash
docker compose logs -f couchdb
```

### CouchDB Authentication Errors

Verify credentials in docker-compose.yml match Python/curl usage:
```yaml
environment:
  - COUCHDB_USER=admin
  - COUCHDB_PASSWORD=password
```

### HTTP 409 Conflict on Update

Document revision is stale. Fetch current document:
```python
license = manager.get_license(license_id)
# Now license['_rev'] is current
```

### Python Unicode Errors (Windows)

The Python scripts use ASCII-friendly output (`[OK]`, `[ERROR]`) instead of Unicode characters to avoid Windows console encoding issues.

## Testing

The repository includes working test data:
- MIT License (ID: 1301e495e309a30f9e304974aa000fe2, checked)
- Apache-2.0 (ID: 1301e495e309a30f9e304974aa001650, checked)
- GPL-3.0 (ID: 1301e495e309a30f9e304974aa005375, unchecked)

Run `python sw360_license_manager.py` to verify setup.

## Documentation Index

- **README.md** - Master overview, quick access guide
- **BACKEND-SETUP-GUIDE.md** - Docker setup, troubleshooting
- **PYTHON-README.md** - Python quick start
- **PYTHON-USAGE-GUIDE.md** - Complete Python API reference with advanced examples
- **COUCHDB-LICENSE-CURATION-GUIDE.md** - Direct CouchDB operations
- **powershell-commands.md** - Windows PowerShell commands
- **linux-wsl-commands.sh** - Bash helper functions
- **quick-reference.txt** - Quick command reference
