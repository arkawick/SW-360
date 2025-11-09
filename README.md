# SW360 License Curation - Complete Setup

Complete documentation for Eclipse SW360 backend setup and license curation.

## What You Have

✅ **SW360 Backend** (v18.1.0-M1) running in Docker
✅ **CouchDB** accessible at http://localhost:5984
✅ **3 Licenses** in database (MIT, Apache-2.0, GPL-3.0)
✅ **Python interface** for programmatic access
✅ **Complete documentation** for all operations

---

## Quick Access

### CouchDB Web Interface (Easiest)
- **URL**: http://localhost:5984/_utils
- **Login**: admin / password
- **Database**: sw360db
- **Visual interface** for managing licenses

### Python Interface (Programmatic)
```bash
# Run tests
python sw360_license_manager.py

# Run examples
python example_usage.py
```

### Command Line (curl)
**PowerShell:**
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"}}"
```

**Git Bash/WSL:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'
```

---

## Documentation Files

### Setup Guides
1. **BACKEND-SETUP-GUIDE.md** - Complete backend installation from scratch
   - Docker setup
   - CouchDB configuration
   - Troubleshooting

### License Curation Guides
2. **COUCHDB-LICENSE-CURATION-GUIDE.md** - Comprehensive CouchDB operations
   - All CRUD operations
   - Query examples
   - Best practices

3. **PYTHON-README.md** - Python quick start guide
   - Installation
   - Basic usage
   - Common patterns

4. **PYTHON-USAGE-GUIDE.md** - Complete Python documentation
   - All methods
   - Advanced examples
   - API reference

### Platform-Specific Commands
5. **powershell-commands.md** - Windows PowerShell commands
6. **linux-wsl-commands.sh** - Bash helper script with functions
7. **quick-reference.txt** - Quick command reference

### Python Files
8. **sw360_license_manager.py** - Main Python module
9. **example_usage.py** - Practical examples

### Other Guides
10. **sw360-license-curation-guide.md** - REST API documentation
11. **SETUP_SUMMARY.md** - Setup status and reference

---

## Which Method Should I Use?

### Option 1: CouchDB Web Interface (Recommended for Beginners)
**Best for:** Visual interface, quick edits, exploring data

**Pros:**
- Easy to use
- No coding required
- Visual feedback
- Good for learning

**Access:** http://localhost:5984/_utils

---

### Option 2: Python Interface (Recommended for Automation)
**Best for:** Bulk operations, automation, integration with other tools

**Pros:**
- Programmatic control
- Bulk import/export
- Error handling
- Scripting capabilities
- No external dependencies

**Quick Start:**
```bash
python example_usage.py
```

**Read:** PYTHON-README.md

---

### Option 3: curl Commands (Advanced Users)
**Best for:** Shell scripts, CI/CD pipelines, manual operations

**Pros:**
- Works anywhere
- Scriptable
- Direct API access
- Platform specific guides available

**Read:**
- powershell-commands.md (Windows)
- linux-wsl-commands.sh (Linux/WSL)

---

## Common Tasks

### List All Licenses

**Web UI:** http://localhost:5984/_utils → sw360db → Filter by type:"license"

**Python:**
```python
from sw360_license_manager import SW360LicenseManager
manager = SW360LicenseManager()
licenses = manager.list_licenses()
```

**curl (PowerShell):**
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"}}"
```

---

### Create a License

**Web UI:** sw360db → + button → Create Document

**Python:**
```python
result = manager.create_license(
    full_name="MIT License",
    short_name="MIT",
    text="Permission is hereby granted...",
    osi_approved=True,
    checked=False
)
```

**curl (PowerShell):**
```powershell
curl.exe -X POST "http://admin:password@localhost:5984/sw360db" `
  -H "Content-Type: application/json" `
  -d "{\"type\":\"license\",\"fullName\":\"MIT License\",\"shortName\":\"MIT\",...}"
```

---

### Update a License

**Web UI:** Click license → Edit → Save

**Python:**
```python
license = manager.get_license("license_id")
manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],
    full_name=license['fullName'],
    short_name=license['shortName'],
    text=license['text'],
    osi_approved=license['OSIApproved'],
    checked=True  # Mark as reviewed
)
```

---

### Find License by SPDX ID

**Python:**
```python
mit = manager.find_by_short_name("MIT")
```

**curl (PowerShell):**
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\",\"shortName\":\"MIT\"}}"
```

---

### Get Statistics

**Python:**
```python
total = manager.count_licenses()
osi_approved = len(manager.get_osi_approved_licenses())
checked = len(manager.get_checked_licenses())

print(f"Total: {total}, OSI: {osi_approved}, Reviewed: {checked}")
```

---

## Your Current Setup

### Services Running
```
sw360                       - Port 8080 (Spring Boot backend)
sw360-stable-couchdb-1      - Port 5984 (CouchDB)
sw360-stable-postgresdb-1   - Port 5438 (PostgreSQL)
```

### Current Licenses (3)
1. **MIT License** (reviewed ✓)
   - ID: 1301e495e309a30f9e304974aa000fe2
   - SPDX: MIT
   - OSI Approved: Yes

2. **Apache License 2.0** (reviewed ✓)
   - ID: 1301e495e309a30f9e304974aa001650
   - SPDX: Apache-2.0
   - OSI Approved: Yes

3. **GNU General Public License v3.0** (pending review)
   - ID: 1301e495e309a30f9e304974aa005375
   - SPDX: GPL-3.0
   - OSI Approved: Yes

---

## Getting Started

### For First-Time Users

1. **Start with CouchDB Web UI:**
   - Open: http://localhost:5984/_utils
   - Login: admin / password
   - Explore: sw360db database
   - Try: Creating, editing, viewing licenses

2. **Try Python Examples:**
   ```bash
   cd C:\Users\Arkajyoti\Desktop\SW360
   python example_usage.py
   ```

3. **Read Documentation:**
   - Start with: PYTHON-README.md
   - Then: COUCHDB-LICENSE-CURATION-GUIDE.md

### For Automation

1. **Use Python Interface:**
   ```python
   from sw360_license_manager import SW360LicenseManager
   manager = SW360LicenseManager()
   ```

2. **Read:**
   - PYTHON-USAGE-GUIDE.md (complete examples)
   - example_usage.py (working code)

### For Shell Scripts

1. **Read platform-specific guide:**
   - Windows: powershell-commands.md
   - Linux/WSL: linux-wsl-commands.sh

---

## Troubleshooting

### CouchDB Not Accessible

**Check if running:**
```bash
docker ps
```

**Restart:**
```bash
cd C:\Users\Arkajyoti\Desktop\SW360\sw360-stable
docker compose restart couchdb
```

### Python Script Errors

**Test connection:**
```bash
python sw360_license_manager.py
```

**Common issues:**
- CouchDB not running → Start Docker containers
- Wrong credentials → Check username/password
- Port conflict → Check if port 5984 is in use

### Docker Containers Not Starting

**View logs:**
```bash
docker compose logs -f
```

**Restart all services:**
```bash
docker compose down
docker compose up -d
```

**Check for port conflicts:**
```bash
netstat -ano | findstr :5984
netstat -ano | findstr :8080
```

---

## Important Notes

### Authentication Compatibility Issue

The **frontend** (http://localhost:3000) **cannot authenticate** with the backend due to:
- Frontend uses: Basic Authentication
- Backend requires: OAuth2 tokens
- Version mismatch: Beta frontend vs Stable backend

**Solution:** Use direct CouchDB access (recommended approach)

### No REST API Access

The backend REST API at http://localhost:8080 requires OAuth2 tokens which are difficult to obtain without the Liferay portal.

**Solution:** Use direct CouchDB access via:
- Web interface (easiest)
- Python interface (programmatic)
- curl commands (shell scripts)

---

## Docker Management

### Start Services
```bash
cd C:\Users\Arkajyoti\Desktop\SW360\sw360-stable
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
docker compose logs -f
docker compose logs -f sw360
docker compose logs -f couchdb
```

### Restart Service
```bash
docker restart sw360
docker restart sw360-stable-couchdb-1
```

### Check Status
```bash
docker ps
```

---

## File Structure

```
C:\Users\Arkajyoti\Desktop\SW360\
│
├── sw360-stable/                    # Backend repository
│   ├── docker-compose.yml           # Docker configuration
│   └── ...
│
├── sw360-frontend/                  # Frontend (not compatible)
│   └── ...
│
├── README.md                        # This file
├── BACKEND-SETUP-GUIDE.md          # Backend setup
├── COUCHDB-LICENSE-CURATION-GUIDE.md # CouchDB guide
├── PYTHON-README.md                # Python quick start
├── PYTHON-USAGE-GUIDE.md           # Python full docs
├── powershell-commands.md          # PowerShell commands
├── linux-wsl-commands.sh           # Bash commands
├── quick-reference.txt             # Quick reference
├── sw360-license-curation-guide.md # REST API guide
├── SETUP_SUMMARY.md                # Setup status
│
├── sw360_license_manager.py        # Python module
└── example_usage.py                # Python examples
```

---

## Next Steps

1. **Learn the basics:**
   - Open CouchDB web UI and explore
   - Run `python example_usage.py`
   - Read PYTHON-README.md

2. **Import your licenses:**
   - Use Python bulk import (see PYTHON-USAGE-GUIDE.md)
   - Or use CouchDB web interface
   - Or use curl commands

3. **Automate your workflow:**
   - Create Python scripts for regular tasks
   - Set up CI/CD integration
   - Export/import license data

4. **Explore advanced features:**
   - Custom queries
   - Bulk operations
   - Reporting and analytics

---

## Support & Resources

- **SW360 Official Docs**: https://eclipse.dev/sw360/docs/
- **CouchDB Docs**: https://docs.couchdb.org/
- **Docker Docs**: https://docs.docker.com/

---

## Summary

You have a **fully operational SW360 backend** with **direct CouchDB access** for license curation:

✅ Docker containers running
✅ CouchDB accessible and authenticated
✅ Python interface ready to use
✅ Complete documentation suite
✅ 3 licenses already in database
✅ Multiple access methods available

**Choose your preferred method and start curating licenses!**

---

**Last Updated:** 2025-11-09
**Location:** C:\Users\Arkajyoti\Desktop\SW360\
**CouchDB:** http://localhost:5984/_utils (admin/password)
**Database:** sw360db
