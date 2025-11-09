# Python License Manager - Usage Guide

Complete guide for using the Python interface to manage SW360 licenses via CouchDB.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Operations](#basic-operations)
- [Advanced Usage](#advanced-usage)
- [Complete Examples](#complete-examples)
- [API Reference](#api-reference)

---

## Installation

**No external dependencies required!** The script uses only Python standard library.

**Requirements:**
- Python 3.6 or higher
- CouchDB running at http://localhost:5984

**Check Python version:**
```bash
python --version
# or
python3 --version
```

---

## Quick Start

### 1. Test the Connection

```python
python sw360_license_manager.py
```

This runs the built-in test suite and shows:
- CouchDB connection status
- List of databases
- Count of existing licenses
- Sample license data

**Expected output:**
```
SW360 License Manager - Python Interface
============================================================

1. Testing CouchDB connection...
✓ Connected to CouchDB 3.4.2

2. Listing databases...
✓ Found 14 databases
✓ sw360db database exists

3. Counting licenses...
✓ Found 2 licenses in database

4. Listing all licenses...
✓ Retrieved 2 licenses
  - MIT: MIT License
  - Apache-2.0: Apache License 2.0
...
```

---

## Basic Operations

### Initialize the Manager

```python
from sw360_license_manager import SW360LicenseManager

# Using default settings
manager = SW360LicenseManager()

# Or with custom settings
manager = SW360LicenseManager(
    url="http://localhost:5984",
    username="admin",
    password="password",
    database="sw360db"
)
```

---

### 1. List All Licenses

```python
# Get all licenses
licenses = manager.list_licenses()
print(f"Total licenses: {len(licenses)}")

for license in licenses:
    print(f"{license['shortName']}: {license['fullName']}")

# Get limited number of licenses
licenses = manager.list_licenses(limit=10)
```

**Output:**
```
Total licenses: 2
MIT: MIT License
Apache-2.0: Apache License 2.0
```

---

### 2. Create a New License

```python
# Create a license
result = manager.create_license(
    full_name="BSD 3-Clause License",
    short_name="BSD-3-Clause",
    text="Redistribution and use in source and binary forms, with or without modification...",
    osi_approved=True,
    checked=False
)

print(f"Created license with ID: {result['id']}")
print(f"Revision: {result['rev']}")
```

**Output:**
```
Created license with ID: 1301e495e309a30f9e304974aa002abc
Revision: 1-abc123def456...
```

---

### 3. Get a Specific License

```python
# Get by ID
license_id = "1301e495e309a30f9e304974aa000fe2"
license = manager.get_license(license_id)

print(f"License: {license['fullName']}")
print(f"SPDX ID: {license['shortName']}")
print(f"OSI Approved: {license['OSIApproved']}")
print(f"Checked: {license['checked']}")
```

---

### 4. Update a License

```python
# First, get the current license
license = manager.get_license("1301e495e309a30f9e304974aa000fe2")

# Update it (mark as checked/reviewed)
result = manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],  # Current revision required!
    full_name=license['fullName'],
    short_name=license['shortName'],
    text=license['text'],
    osi_approved=license['OSIApproved'],
    checked=True  # Mark as reviewed
)

print(f"Updated to revision: {result['rev']}")
```

---

### 5. Delete a License

```python
# Get the license first
license = manager.get_license("license_id_here")

# Delete it
result = manager.delete_license(
    license_id=license['_id'],
    rev=license['_rev']
)

print(f"Deleted license: {result['id']}")
```

**⚠️ Warning:** This permanently deletes the license!

---

### 6. Search for Licenses

```python
# Find by short name (SPDX identifier)
mit_licenses = manager.find_by_short_name("MIT")
for license in mit_licenses:
    print(f"Found: {license['fullName']}")

# Get OSI approved licenses
osi_licenses = manager.get_osi_approved_licenses()
print(f"OSI approved: {len(osi_licenses)}")

# Get checked/reviewed licenses
checked = manager.get_checked_licenses()
print(f"Reviewed: {len(checked)}")

# Get unchecked licenses (need review)
unchecked = manager.get_unchecked_licenses()
print(f"Pending review: {len(unchecked)}")

# Search by text
results = manager.search_licenses("General Public")
for license in results:
    print(f"Found: {license['shortName']}")
```

---

### 7. Count Licenses

```python
count = manager.count_licenses()
print(f"Total licenses in database: {count}")
```

---

## Advanced Usage

### Bulk Import Licenses

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Define licenses to import
licenses_to_import = [
    {
        "full_name": "GNU General Public License v3.0",
        "short_name": "GPL-3.0",
        "text": "This program is free software...",
        "osi_approved": True
    },
    {
        "full_name": "Mozilla Public License 2.0",
        "short_name": "MPL-2.0",
        "text": "This Source Code Form is subject to...",
        "osi_approved": True
    },
    {
        "full_name": "ISC License",
        "short_name": "ISC",
        "text": "Permission to use, copy, modify...",
        "osi_approved": True
    }
]

# Import all licenses
for lic in licenses_to_import:
    try:
        result = manager.create_license(
            full_name=lic["full_name"],
            short_name=lic["short_name"],
            text=lic["text"],
            osi_approved=lic["osi_approved"],
            checked=False
        )
        print(f"✓ Created: {lic['short_name']}")
    except Exception as e:
        print(f"✗ Failed to create {lic['short_name']}: {e}")

print(f"\nTotal licenses now: {manager.count_licenses()}")
```

---

### Export Licenses to JSON

```python
import json
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Get all licenses
licenses = manager.list_licenses()

# Export to JSON file
with open("licenses_export.json", "w", encoding="utf-8") as f:
    json.dump(licenses, f, indent=2, ensure_ascii=False)

print(f"Exported {len(licenses)} licenses to licenses_export.json")
```

---

### Generate License Report

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Get statistics
total = manager.count_licenses()
osi_approved = len(manager.get_osi_approved_licenses())
checked = len(manager.get_checked_licenses())
unchecked = len(manager.get_unchecked_licenses())

# Generate report
print("=" * 60)
print("SW360 LICENSE REPORT")
print("=" * 60)
print(f"Total Licenses:        {total}")
print(f"OSI Approved:          {osi_approved} ({osi_approved/total*100:.1f}%)")
print(f"Reviewed (Checked):    {checked} ({checked/total*100:.1f}%)")
print(f"Pending Review:        {unchecked} ({unchecked/total*100:.1f}%)")
print("=" * 60)

# List licenses by category
print("\nOSI Approved Licenses:")
for license in manager.get_osi_approved_licenses():
    status = "✓" if license.get('checked') else "○"
    print(f"  {status} {license['shortName']}: {license['fullName']}")

print("\nPending Review:")
for license in manager.get_unchecked_licenses():
    print(f"  ○ {license['shortName']}: {license['fullName']}")
```

---

### Mark Multiple Licenses as Reviewed

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Get all unchecked licenses
unchecked = manager.get_unchecked_licenses()

print(f"Found {len(unchecked)} licenses pending review")

for license in unchecked:
    # Review and update each license
    result = manager.update_license(
        license_id=license['_id'],
        rev=license['_rev'],
        full_name=license['fullName'],
        short_name=license['shortName'],
        text=license.get('text', ''),
        osi_approved=license.get('OSIApproved', False),
        checked=True  # Mark as reviewed
    )
    print(f"✓ Reviewed: {license['shortName']}")

print(f"\nAll {len(unchecked)} licenses have been reviewed!")
```

---

### Custom Query with Additional Fields

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Create license with custom fields
result = manager.create_license(
    full_name="Custom License",
    short_name="CUSTOM-1.0",
    text="License text here...",
    osi_approved=False,
    checked=False,
    # Additional custom fields
    category="Proprietary",
    riskLevel="High",
    approvedBy="Legal Team",
    notes="Special handling required"
)

print(f"Created license with custom fields: {result['id']}")

# Retrieve and display
license = manager.get_license(result['id'])
print(f"Category: {license.get('category')}")
print(f"Risk Level: {license.get('riskLevel')}")
print(f"Approved By: {license.get('approvedBy')}")
```

---

## Complete Examples

### Example 1: Complete CRUD Operations

```python
from sw360_license_manager import SW360LicenseManager

# Initialize
manager = SW360LicenseManager()

# CREATE
print("1. Creating license...")
result = manager.create_license(
    full_name="Example License",
    short_name="EXAMPLE-1.0",
    text="This is an example license",
    osi_approved=False,
    checked=False
)
license_id = result['id']
print(f"✓ Created: {license_id}")

# READ
print("\n2. Reading license...")
license = manager.get_license(license_id)
print(f"✓ Retrieved: {license['fullName']}")
print(f"   Revision: {license['_rev']}")

# UPDATE
print("\n3. Updating license...")
result = manager.update_license(
    license_id=license['_id'],
    rev=license['_rev'],
    full_name="Example License (Updated)",
    short_name="EXAMPLE-1.0",
    text="This is an updated example license",
    osi_approved=False,
    checked=True
)
print(f"✓ Updated to revision: {result['rev']}")

# READ again
license = manager.get_license(license_id)
print(f"✓ Verified update: {license['fullName']}")
print(f"   Checked: {license['checked']}")

# DELETE
print("\n4. Deleting license...")
result = manager.delete_license(
    license_id=license['_id'],
    rev=license['_rev']
)
print(f"✓ Deleted: {result['id']}")

print("\nCRUD operations completed successfully!")
```

---

### Example 2: Import Common Open Source Licenses

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

# Common open source licenses
common_licenses = {
    "MIT": {
        "full_name": "MIT License",
        "text": """Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software..."""
    },
    "Apache-2.0": {
        "full_name": "Apache License 2.0",
        "text": """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License..."""
    },
    "GPL-3.0": {
        "full_name": "GNU General Public License v3.0",
        "text": """This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License..."""
    },
    "BSD-3-Clause": {
        "full_name": "BSD 3-Clause \"New\" or \"Revised\" License",
        "text": """Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met..."""
    }
}

print("Importing common open source licenses...")
print("=" * 60)

for short_name, details in common_licenses.items():
    # Check if already exists
    existing = manager.find_by_short_name(short_name)

    if existing:
        print(f"⊙ {short_name}: Already exists")
    else:
        try:
            result = manager.create_license(
                full_name=details["full_name"],
                short_name=short_name,
                text=details["text"],
                osi_approved=True,
                checked=False
            )
            print(f"✓ {short_name}: Created successfully")
        except Exception as e:
            print(f"✗ {short_name}: Failed - {e}")

print("=" * 60)
print(f"Total licenses in database: {manager.count_licenses()}")
```

---

### Example 3: Interactive License Browser

```python
from sw360_license_manager import SW360LicenseManager, print_license

def browse_licenses():
    manager = SW360LicenseManager()
    licenses = manager.list_licenses()

    print(f"\nFound {len(licenses)} licenses")
    print("=" * 60)

    for i, license in enumerate(licenses, 1):
        print(f"{i}. {license['shortName']}: {license['fullName']}")

    print("=" * 60)

    while True:
        choice = input("\nEnter license number to view details (or 'q' to quit): ")

        if choice.lower() == 'q':
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(licenses):
                print_license(licenses[index], detailed=True)
            else:
                print("Invalid number")
        except ValueError:
            print("Please enter a number")

if __name__ == "__main__":
    browse_licenses()
```

---

## API Reference

### Class: SW360LicenseManager

#### Constructor
```python
SW360LicenseManager(url, username, password, database)
```

**Parameters:**
- `url` (str): CouchDB server URL (default: "http://localhost:5984")
- `username` (str): CouchDB username (default: "admin")
- `password` (str): CouchDB password (default: "password")
- `database` (str): Database name (default: "sw360db")

---

#### Methods

**test_connection()**
```python
info = manager.test_connection()
# Returns: {'couchdb': 'Welcome', 'version': '3.4.2', ...}
```

**list_databases()**
```python
databases = manager.list_databases()
# Returns: ['_replicator', '_users', 'sw360db', ...]
```

**list_licenses(limit=None)**
```python
licenses = manager.list_licenses()  # All licenses
licenses = manager.list_licenses(limit=10)  # First 10
# Returns: List of license documents
```

**create_license(full_name, short_name, text, osi_approved, checked, **kwargs)**
```python
result = manager.create_license(
    full_name="MIT License",
    short_name="MIT",
    text="...",
    osi_approved=True,
    checked=False
)
# Returns: {'ok': True, 'id': '...', 'rev': '...'}
```

**get_license(license_id)**
```python
license = manager.get_license("1301e495e309a30f9e304974aa000fe2")
# Returns: License document dictionary
```

**update_license(license_id, rev, full_name, short_name, text, osi_approved, checked, **kwargs)**
```python
result = manager.update_license(
    license_id="...",
    rev="1-abc123",
    full_name="Updated Name",
    short_name="MIT",
    text="...",
    osi_approved=True,
    checked=True
)
# Returns: {'ok': True, 'id': '...', 'rev': '...'}
```

**delete_license(license_id, rev)**
```python
result = manager.delete_license("license_id", "1-abc123")
# Returns: {'ok': True, 'id': '...', 'rev': '...'}
```

**find_by_short_name(short_name)**
```python
licenses = manager.find_by_short_name("MIT")
# Returns: List of matching licenses
```

**get_osi_approved_licenses()**
```python
licenses = manager.get_osi_approved_licenses()
# Returns: List of OSI approved licenses
```

**get_checked_licenses()**
```python
licenses = manager.get_checked_licenses()
# Returns: List of reviewed licenses
```

**get_unchecked_licenses()**
```python
licenses = manager.get_unchecked_licenses()
# Returns: List of unreviewed licenses
```

**count_licenses()**
```python
count = manager.count_licenses()
# Returns: Integer count
```

**search_licenses(search_text, fields=None)**
```python
results = manager.search_licenses("General Public")
results = manager.search_licenses("BSD", fields=["shortName", "fullName"])
# Returns: List of matching licenses
```

---

### Utility Function: print_license

```python
print_license(license, detailed=False)
```

Pretty prints a license document.

**Parameters:**
- `license` (dict): License document
- `detailed` (bool): If True, includes full license text

---

## Error Handling

```python
from sw360_license_manager import SW360LicenseManager

manager = SW360LicenseManager()

try:
    license = manager.get_license("invalid_id")
except Exception as e:
    print(f"Error: {e}")
    # Output: Error: HTTP 404 Error: {"error":"not_found",...}
```

**Common errors:**
- `HTTP 401`: Authentication failed (wrong username/password)
- `HTTP 404`: Document not found
- `HTTP 409`: Conflict (wrong revision number for update)
- `Connection refused`: CouchDB not running

---

## Tips & Best Practices

1. **Always get current revision before updating:**
   ```python
   license = manager.get_license(license_id)
   # Use license['_rev'] for update
   ```

2. **Check if license exists before creating:**
   ```python
   existing = manager.find_by_short_name("MIT")
   if not existing:
       manager.create_license(...)
   ```

3. **Use try-except for error handling:**
   ```python
   try:
       result = manager.create_license(...)
   except Exception as e:
       print(f"Failed: {e}")
   ```

4. **Backup before bulk operations:**
   ```python
   # Export all licenses
   licenses = manager.list_licenses()
   import json
   with open("backup.json", "w") as f:
       json.dump(licenses, f)
   ```

---

## Running the Examples

Save any example code to a file and run:

```bash
python example.py
```

Or use the interactive Python shell:

```bash
python
>>> from sw360_license_manager import SW360LicenseManager
>>> manager = SW360LicenseManager()
>>> licenses = manager.list_licenses()
>>> print(len(licenses))
```

---

## Next Steps

- Read: `BACKEND-SETUP-GUIDE.md` for backend setup
- Read: `COUCHDB-LICENSE-CURATION-GUIDE.md` for detailed CouchDB operations
- Explore: CouchDB Web UI at http://localhost:5984/_utils

---

**Python License Manager provides a clean, Pythonic interface for all your SW360 license curation needs!**
