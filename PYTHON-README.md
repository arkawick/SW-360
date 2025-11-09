# Python License Manager - Quick Start

Python interface for managing SW360 licenses via CouchDB.

## Files

- **sw360_license_manager.py** - Main module with `SW360LicenseManager` class
- **example_usage.py** - Practical examples demonstrating common operations
- **PYTHON-USAGE-GUIDE.md** - Complete documentation with all features

## Quick Start

### Test the Setup

```bash
python sw360_license_manager.py
```

This runs built-in tests and shows:
- Connection status
- Database list
- License count
- Sample data

### Run Examples

```bash
python example_usage.py
```

Shows 6 practical examples:
1. List all licenses
2. Get license details
3. Create new license
4. View statistics
5. Find unchecked licenses
6. Update a license

## Basic Usage in Your Code

```python
from sw360_license_manager import SW360LicenseManager

# Initialize
manager = SW360LicenseManager()

# List all licenses
licenses = manager.list_licenses()
for lic in licenses:
    print(f"{lic['shortName']}: {lic['fullName']}")

# Create a license
result = manager.create_license(
    full_name="MIT License",
    short_name="MIT",
    text="Permission is hereby granted...",
    osi_approved=True,
    checked=False
)

# Find by SPDX identifier
mit = manager.find_by_short_name("MIT")

# Get license by ID
license = manager.get_license("license_id_here")

# Update license
manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],
    full_name=license['fullName'],
    short_name=license['shortName'],
    text=license['text'],
    osi_approved=license['OSIApproved'],
    checked=True  # Mark as reviewed
)

# Statistics
total = manager.count_licenses()
osi = len(manager.get_osi_approved_licenses())
checked = len(manager.get_checked_licenses())
```

## Available Methods

### Query Operations
- `list_licenses(limit=None)` - Get all licenses
- `get_license(license_id)` - Get specific license
- `find_by_short_name(short_name)` - Search by SPDX ID
- `count_licenses()` - Count total licenses
- `search_licenses(text, fields)` - Text search

### CRUD Operations
- `create_license(...)` - Create new license
- `update_license(...)` - Update existing license
- `delete_license(license_id, rev)` - Delete license

### Filter Operations
- `get_osi_approved_licenses()` - Get OSI approved
- `get_checked_licenses()` - Get reviewed licenses
- `get_unchecked_licenses()` - Get pending review

### System Operations
- `test_connection()` - Test CouchDB connection
- `list_databases()` - List all databases

## Common Patterns

### Check if License Exists Before Creating

```python
existing = manager.find_by_short_name("MIT")
if not existing:
    manager.create_license(
        full_name="MIT License",
        short_name="MIT",
        text="...",
        osi_approved=True
    )
else:
    print("License already exists")
```

### Bulk Import Licenses

```python
licenses_data = [
    {"full_name": "MIT License", "short_name": "MIT", ...},
    {"full_name": "Apache 2.0", "short_name": "Apache-2.0", ...},
]

for lic in licenses_data:
    try:
        manager.create_license(**lic)
        print(f"Created: {lic['short_name']}")
    except Exception as e:
        print(f"Failed: {e}")
```

### Export to JSON

```python
import json

licenses = manager.list_licenses()
with open("licenses.json", "w") as f:
    json.dump(licenses, f, indent=2)
```

### Mark All Licenses as Reviewed

```python
unchecked = manager.get_unchecked_licenses()
for license in unchecked:
    manager.update_license(
        license_id=license['_id'],
        rev=license['_rev'],
        full_name=license['fullName'],
        short_name=license['shortName'],
        text=license.get('text', ''),
        osi_approved=license.get('OSIApproved', False),
        checked=True
    )
```

### Generate Report

```python
total = manager.count_licenses()
osi = len(manager.get_osi_approved_licenses())
checked = len(manager.get_checked_licenses())

print(f"Total: {total}")
print(f"OSI Approved: {osi} ({osi/total*100:.1f}%)")
print(f"Reviewed: {checked} ({checked/total*100:.1f}%)")
```

## Error Handling

```python
try:
    license = manager.get_license("some_id")
except Exception as e:
    print(f"Error: {e}")
```

**Common Errors:**
- HTTP 401: Wrong username/password
- HTTP 404: License not found
- HTTP 409: Revision conflict (use current `_rev`)

## Requirements

- Python 3.6+
- No external dependencies (uses standard library only)
- CouchDB running at http://localhost:5984

## Configuration

Default settings:
```python
manager = SW360LicenseManager(
    url="http://localhost:5984",
    username="admin",
    password="password",
    database="sw360db"
)
```

Change credentials:
```python
manager = SW360LicenseManager(
    username="myuser",
    password="mypass"
)
```

## Interactive Python Shell

```bash
python
```

```python
>>> from sw360_license_manager import SW360LicenseManager
>>> manager = SW360LicenseManager()
>>> licenses = manager.list_licenses()
>>> len(licenses)
3
>>> licenses[0]['shortName']
'MIT'
```

## Testing

Run the built-in test suite:
```bash
python sw360_license_manager.py
```

Run practical examples:
```bash
python example_usage.py
```

## Documentation

- **PYTHON-USAGE-GUIDE.md** - Complete guide with advanced examples
- **BACKEND-SETUP-GUIDE.md** - Backend setup instructions
- **COUCHDB-LICENSE-CURATION-GUIDE.md** - CouchDB operations

## Tips

1. Always get current revision before updating:
   ```python
   license = manager.get_license(id)
   # Use license['_rev'] for update
   ```

2. Check existence before creating:
   ```python
   if not manager.find_by_short_name("MIT"):
       manager.create_license(...)
   ```

3. Handle errors gracefully:
   ```python
   try:
       result = manager.create_license(...)
   except Exception as e:
       print(f"Error: {e}")
   ```

4. Use Python's context for better code:
   ```python
   # List comprehension
   short_names = [lic['shortName'] for lic in licenses]

   # Filter
   mit_licenses = [lic for lic in licenses if 'MIT' in lic['fullName']]

   # Sort
   sorted_licenses = sorted(licenses, key=lambda x: x['shortName'])
   ```

## What Just Happened?

When you ran `example_usage.py`, it:
1. ✅ Listed 2 existing licenses (MIT, Apache-2.0)
2. ✅ Created GPL-3.0 license
3. ✅ Marked Apache-2.0 as reviewed
4. ✅ Showed statistics and pending reviews

Your database now has **3 licenses**:
- MIT (reviewed ✓)
- Apache-2.0 (reviewed ✓)
- GPL-3.0 (pending review)

## Next Steps

1. Read **PYTHON-USAGE-GUIDE.md** for advanced features
2. Modify **example_usage.py** for your needs
3. Write custom scripts using `SW360LicenseManager`
4. Import your license data programmatically

---

**Ready to use! Start managing licenses with Python!**
