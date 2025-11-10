# SW360 License Curation Sample Project

This sample project demonstrates practical license curation workflows using the SW360 system with direct CouchDB access.

## Overview

License curation is the process of managing and reviewing software licenses in your organization. This sample project shows you how to:

- **Create** individual licenses
- **Import** multiple licenses in bulk
- **Review** and approve licenses
- **Query** license information
- **Generate** reports and exports

## Project Structure

```
license-curation-sample/
├── README.md                    # This file
├── sample_licenses.json         # Sample license data (10 common licenses)
├── 01_basic_operations.py       # Basic CRUD operations
├── 02_bulk_import.py            # Bulk import from JSON
├── 03_review_workflow.py        # License review process
└── 04_generate_report.py        # Generate reports and exports
```

## Prerequisites

Before running these examples, ensure you have:

1. **SW360 Backend Running**
   ```bash
   cd ../sw360-stable
   docker ps  # Verify containers are running
   ```

2. **CouchDB Accessible**
   - URL: http://localhost:5984
   - Credentials: admin / password
   - Database: sw360db

3. **Python Dependencies**
   - The `sw360_license_manager.py` module in the parent directory
   - Python 3.7+ installed

## Quick Start

### 1. Basic Operations

Learn fundamental license operations:

```bash
python 01_basic_operations.py
```

**What it does:**
- Connects to CouchDB
- Creates a new license (BSD-2-Clause)
- Retrieves license details
- Searches for licenses
- Updates license metadata (marks as checked)
- Shows database statistics

**Use this when:**
- Learning the basics
- Testing your setup
- Understanding the license lifecycle

---

### 2. Bulk Import

Import multiple licenses at once:

```bash
python 02_bulk_import.py
```

**What it does:**
- Loads 10 common licenses from `sample_licenses.json`
- Checks if each license already exists
- Creates only new licenses
- Shows import statistics
- Lists all licenses in the database

**Included licenses:**
- BSD-2-Clause, BSD-3-Clause
- ISC
- MPL-2.0 (Mozilla Public License)
- EPL-2.0 (Eclipse Public License)
- LGPL-2.1, LGPL-3.0
- CC0-1.0 (Creative Commons)
- Unlicense
- BSL-1.0 (Boost Software License)

**Use this when:**
- Setting up a new database
- Importing from another system
- Adding multiple licenses at once

---

### 3. License Review Workflow

Review and approve unchecked licenses:

```bash
# Interactive mode (manual review)
python 03_review_workflow.py

# Auto-approve mode (for demo/testing)
python 03_review_workflow.py --auto-approve
```

**What it does:**
- Finds all unchecked licenses
- Displays license details for review
- Allows you to approve or skip each license
- Tracks review progress
- Shows completion statistics

**Interactive mode options:**
- `[A]` - Approve (mark as checked)
- `[S]` - Skip (review later)
- `[Q]` - Quit review process

**Use this when:**
- Reviewing new licenses before deployment
- Validating license text accuracy
- Ensuring compliance approval

---

### 4. Generate Reports

Create reports in various formats:

```bash
# Text report (console output)
python 04_generate_report.py

# JSON export
python 04_generate_report.py --format json

# CSV export (for Excel/Sheets)
python 04_generate_report.py --format csv
```

**What it does:**
- Shows summary statistics
- Lists all licenses
- Highlights OSI-approved licenses
- Shows pending reviews
- Exports to JSON or CSV

**Use this when:**
- Generating compliance reports
- Auditing license database
- Exporting for other tools
- Sharing with stakeholders

---

## Sample Workflows

### Workflow 1: Initial Setup

**Scenario:** Setting up a new SW360 license database

```bash
# Step 1: Import common licenses
python 02_bulk_import.py

# Step 2: Review all imported licenses
python 03_review_workflow.py --auto-approve

# Step 3: Generate initial report
python 04_generate_report.py
```

---

### Workflow 2: Adding Custom License

**Scenario:** Adding a proprietary or custom license

1. Add your license to `sample_licenses.json`:

```json
{
  "full_name": "My Company Proprietary License",
  "short_name": "MyCompany-Proprietary",
  "text": "Copyright (c) 2025 My Company...",
  "osi_approved": false,
  "checked": false
}
```

2. Import it:

```bash
python 02_bulk_import.py
```

3. Review and approve:

```bash
python 03_review_workflow.py
```

---

### Workflow 3: License Audit

**Scenario:** Quarterly license compliance audit

```bash
# Generate current state report
python 04_generate_report.py --format csv

# Check for unchecked licenses
python 03_review_workflow.py

# Export final approved list
python 04_generate_report.py --format json
```

---

## Understanding the Data Model

Each license in SW360 has these fields:

```json
{
  "_id": "auto-generated-uuid",
  "_rev": "revision-number",
  "type": "license",
  "fullName": "Full License Name",
  "shortName": "SPDX-Identifier",
  "text": "Full license text...",
  "OSIApproved": true/false,
  "checked": true/false
}
```

**Key fields:**
- `_id` - Unique identifier (auto-generated by CouchDB)
- `_rev` - Revision number (required for updates)
- `type` - Must be "license"
- `shortName` - SPDX identifier (e.g., MIT, Apache-2.0)
- `OSIApproved` - Is this OSI-approved?
- `checked` - Has this been reviewed/approved?

---

## Advanced Usage

### Python Interactive Shell

```python
import sys
sys.path.insert(0, '..')
from sw360_license_manager import SW360LicenseManager

# Initialize manager
manager = SW360LicenseManager()

# Get all MIT licenses
mit_licenses = manager.find_by_short_name("MIT")

# Count all licenses
total = manager.count_licenses()

# Get unchecked licenses
unchecked = manager.get_unchecked_licenses()
print(f"Pending review: {len(unchecked)}")

# Update a license
license = mit_licenses[0]
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

### Direct CouchDB Access

You can also use CouchDB directly:

**Via Web UI:**
http://localhost:5984/_utils/#database/sw360db/_all_docs

**Via curl (PowerShell):**
```powershell
# List all licenses
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"}}"

# Get specific license
curl.exe -s "http://admin:password@localhost:5984/sw360db/LICENSE_ID"
```

**Via curl (Git Bash/WSL):**
```bash
# List all licenses
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'
```

---

## Troubleshooting

### Issue: "Could not connect to CouchDB"

**Solution:**
```bash
# Check if containers are running
docker ps

# Check if CouchDB is accessible
curl.exe http://localhost:5984

# Restart containers if needed
cd ../sw360-stable
docker compose restart
```

---

### Issue: "License already exists"

**Solution:**
This is expected behavior. The scripts check for existing licenses and skip duplicates. To update an existing license, use the update functionality in script 01.

---

### Issue: "Failed to create license"

**Solution:**
```bash
# Check CouchDB credentials
curl.exe -u admin:password http://localhost:5984

# Verify database exists
curl.exe -u admin:password http://localhost:5984/_all_dbs
```

---

## Real-World Use Cases

### Use Case 1: Open Source Compliance

**Problem:** Need to track all open source licenses used in your software

**Solution:**
1. Extract licenses from your dependencies
2. Format as JSON (see `sample_licenses.json`)
3. Bulk import: `python 02_bulk_import.py custom_licenses.json`
4. Review: `python 03_review_workflow.py`
5. Report: `python 04_generate_report.py --format csv`

---

### Use Case 2: License Policy Enforcement

**Problem:** Ensure only approved licenses are used

**Solution:**
1. Import allowed licenses
2. Mark as checked after legal review
3. Generate approved list: `python 04_generate_report.py --format json`
4. Integrate with CI/CD to validate dependencies

---

### Use Case 3: Vendor License Management

**Problem:** Track third-party vendor licenses

**Solution:**
1. Create licenses with vendor-specific names
2. Set `osi_approved=false` for proprietary licenses
3. Review terms: `python 03_review_workflow.py`
4. Generate vendor report: `python 04_generate_report.py`

---

## Next Steps

After completing this sample project:

1. **Explore Python API**
   - Read: `../PYTHON-USAGE-GUIDE.md`
   - Module: `../sw360_license_manager.py`

2. **Direct CouchDB Access**
   - Guide: `../COUCHDB-LICENSE-CURATION-GUIDE.md`
   - Web UI: http://localhost:5984/_utils

3. **Customize for Your Needs**
   - Modify scripts for your workflow
   - Add custom fields to licenses
   - Integrate with your tools

4. **Production Deployment**
   - Backup CouchDB regularly
   - Implement proper access controls
   - Monitor license compliance

---

## Additional Resources

- **SW360 Documentation:** https://eclipse.dev/sw360/docs/
- **CouchDB Documentation:** https://docs.couchdb.org/
- **SPDX License List:** https://spdx.org/licenses/
- **OSI Approved Licenses:** https://opensource.org/licenses

---

## Support

For questions or issues:

1. Check the main README: `../README.md`
2. Review documentation: `../PYTHON-USAGE-GUIDE.md`
3. Check CouchDB Fauxton: http://localhost:5984/_utils
4. View container logs: `docker compose logs -f`

---

## License

This sample project is part of the Eclipse SW360 ecosystem and follows the Eclipse Public License 2.0.

---

**Happy License Curating! 🎉**
