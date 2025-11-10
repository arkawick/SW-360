# Quick Start Guide

Get started with SW360 license curation in 5 minutes!

## Prerequisites Check

Before you begin, verify your setup:

```bash
# 1. Check Docker containers are running
docker ps

# You should see:
# - sw360
# - sw360-stable-couchdb-1
# - sw360-stable-postgresdb-1

# 2. Test CouchDB connection (PowerShell)
curl.exe http://localhost:5984

# 3. Test Python
python --version
```

## 5-Minute Demo

### Step 1: Basic Operations (2 minutes)

Learn the basics of license management:

```bash
cd license-curation-sample
python 01_basic_operations.py
```

**What you'll see:**
- ✅ Connection to CouchDB
- ✅ Create a new license (BSD-2-Clause)
- ✅ Search and retrieve license details
- ✅ Update license (mark as checked)
- ✅ View database statistics

---

### Step 2: Bulk Import (1 minute)

Import 10 common open source licenses:

```bash
python 02_bulk_import.py
```

**What you'll see:**
- ✅ Import 10 licenses from JSON
- ✅ Skip duplicates automatically
- ✅ Summary of import results
- ✅ List of all licenses in database

---

### Step 3: Review Workflow (1 minute)

Review and approve imported licenses:

```bash
python 03_review_workflow.py --auto-approve
```

**What you'll see:**
- ✅ Display each unchecked license
- ✅ Automatically approve all licenses
- ✅ Track review progress
- ✅ 100% completion status

---

### Step 4: Generate Report (1 minute)

Create a comprehensive license report:

```bash
python 04_generate_report.py
```

**What you'll see:**
- ✅ Summary statistics
- ✅ Complete license list
- ✅ OSI-approved licenses
- ✅ Review completion rate

---

## Export Reports

### JSON Export (for APIs)

```bash
python 04_generate_report.py --format json
```

Creates: `license_report_YYYYMMDD_HHMMSS.json`

### CSV Export (for Excel)

```bash
python 04_generate_report.py --format csv
```

Creates: `license_report_YYYYMMDD_HHMMSS.csv`

---

## What's Next?

### Interactive Review

Review licenses manually (instead of auto-approve):

```bash
python 03_review_workflow.py
```

Options during review:
- **[A]** Approve - Mark license as checked
- **[S]** Skip - Review later
- **[Q]** Quit - Exit review process

---

### Custom License Data

1. Create your own JSON file:

```json
[
  {
    "full_name": "My Custom License",
    "short_name": "MyLicense-1.0",
    "text": "License text here...",
    "osi_approved": false,
    "checked": false
  }
]
```

2. Import it:

```bash
python 02_bulk_import.py path/to/your/licenses.json
```

---

### Web Interface

View licenses in CouchDB Fauxton:

1. Open: http://localhost:5984/_utils
2. Login: `admin` / `password`
3. Click: `sw360db` database
4. Browse licenses visually

---

### Python API

Use the license manager programmatically:

```python
import sys
sys.path.insert(0, '..')
from sw360_license_manager import SW360LicenseManager

# Initialize
manager = SW360LicenseManager()

# Find license
licenses = manager.find_by_short_name("MIT")

# Get statistics
total = manager.count_licenses()
checked = len(manager.get_checked_licenses())
print(f"Reviewed: {checked}/{total}")
```

---

## Troubleshooting

### "Could not connect to CouchDB"

```bash
# Check containers
docker ps

# Restart if needed
cd ../sw360-stable
docker compose restart

# Wait 30 seconds and retry
```

---

### "License already exists"

This is normal! The scripts detect duplicates and skip them.
To update an existing license, use the update functionality in script 01.

---

## Common Workflows

### New Project Setup

```bash
# 1. Import standard licenses
python 02_bulk_import.py

# 2. Review all licenses
python 03_review_workflow.py --auto-approve

# 3. Generate baseline report
python 04_generate_report.py --format json
```

---

### Weekly License Review

```bash
# 1. Check for new unchecked licenses
python 03_review_workflow.py

# 2. Generate updated report
python 04_generate_report.py --format csv
```

---

### Compliance Audit

```bash
# Generate comprehensive report
python 04_generate_report.py --format text > audit_report.txt

# Export for stakeholders
python 04_generate_report.py --format csv
```

---

## Learn More

- **Full Documentation:** See [README.md](README.md)
- **Python API Guide:** See `../PYTHON-USAGE-GUIDE.md`
- **CouchDB Guide:** See `../COUCHDB-LICENSE-CURATION-GUIDE.md`

---

## Success! 🎉

You've completed the quick start guide. You now know how to:

✅ Create and manage licenses
✅ Bulk import license data
✅ Review and approve licenses
✅ Generate reports and exports

Continue exploring the scripts and customize them for your workflow!
