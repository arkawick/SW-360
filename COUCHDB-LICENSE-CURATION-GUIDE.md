# CouchDB Direct Access Guide for SW360 License Curation

## Overview

This guide explains how to directly manage SW360 licenses using CouchDB, bypassing the REST API and web interface. This is the recommended approach when working with the Docker-deployed SW360 backend.

## Quick Start

**CouchDB Connection:**
- URL: http://localhost:5984
- Username: `admin`
- Password: `password`
- Database: `sw360db`

**Authentication Methods:**
```bash
# Method 1: Using -u flag (recommended for bash/Git Bash)
curl -u admin:password "http://localhost:5984/..."

# Method 2: Using curl.exe in PowerShell
curl.exe -u admin:password "http://localhost:5984/..."

# Method 3: Web Interface
# Open browser: http://localhost:5984/_utils
# Login with admin/password
```

## SW360 License Document Structure

Every license in SW360 is stored as a JSON document with this structure:

```json
{
  "_id": "auto-generated-unique-id",
  "_rev": "revision-number",
  "type": "license",
  "fullName": "Full License Name",
  "shortName": "SPDX-Identifier or Short Name",
  "text": "Complete license text",
  "OSIApproved": true,
  "checked": false,
  "licenseTypeDatabaseId": "optional",
  "licenseType": {
    "licenseType": "String",
    "licenseTypeId": 123
  },
  "externalIds": {
    "SPDX-License-Identifier": "MIT"
  }
}
```

### Required Fields
- `type`: Must be `"license"`
- `fullName`: Official license name
- `shortName`: Brief identifier (use SPDX IDs when possible)

### Optional Fields
- `text`: Full license text
- `OSIApproved`: Boolean - OSI approval status
- `checked`: Boolean - Internal review flag
- `licenseTypeDatabaseId`: Reference to license type
- `externalIds`: Map of external identifiers

## Complete CRUD Operations

### 1. CREATE - Add a New License

**Basic License:**
```bash
curl -X POST -u admin:password "http://localhost:5984/sw360db" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "license",
    "fullName": "MIT License",
    "shortName": "MIT",
    "text": "Permission is hereby granted, free of charge...",
    "OSIApproved": true,
    "checked": false
  }'
```

**Response:**
```json
{
  "ok": true,
  "id": "1301e495e309a30f9e304974aa000fe2",
  "rev": "1-a185bf32a420bd295bab540115dfa7ad"
}
```

**Complete License with All Fields:**
```bash
curl -X POST -u admin:password "http://localhost:5984/sw360db" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "license",
    "fullName": "Apache License 2.0",
    "shortName": "Apache-2.0",
    "text": "Licensed under the Apache License, Version 2.0...",
    "OSIApproved": true,
    "checked": false,
    "licenseTypeDatabaseId": "type-001",
    "externalIds": {
      "SPDX-License-Identifier": "Apache-2.0",
      "URL": "https://opensource.org/licenses/Apache-2.0"
    }
  }'
```

### 2. READ - Query and Retrieve Licenses

**Get All Licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'
```

**Get Specific License by ID:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/1301e495e309a30f9e304974aa000fe2"
```

**Get Licenses with Limit:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"limit":10}'
```

**Search by Short Name:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","shortName":"MIT"}}'
```

**Search by Full Name (partial match):**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","fullName":{"$regex":"(?i)apache"}}}'
```

**Get Only OSI-Approved Licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","OSIApproved":true}}'
```

**Get Checked Licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","checked":true}}'
```

**Get Unchecked Licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","checked":false}}'
```

### 3. UPDATE - Modify an Existing License

**Important:** You MUST include the current `_rev` value to update a document.

**Step 1: Get the current license with its revision:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/LICENSE_ID"
```

**Step 2: Update with the revision:**
```bash
curl -X PUT -u admin:password "http://localhost:5984/sw360db/1301e495e309a30f9e304974aa000fe2" \
  -H "Content-Type: application/json" \
  -d '{
    "_rev": "1-a185bf32a420bd295bab540115dfa7ad",
    "type": "license",
    "fullName": "MIT License",
    "shortName": "MIT",
    "text": "UPDATED: Permission is hereby granted, free of charge...",
    "OSIApproved": true,
    "checked": true
  }'
```

**Response:**
```json
{
  "ok": true,
  "id": "1301e495e309a30f9e304974aa000fe2",
  "rev": "2-b7a670951e704bde51f232232c43b745"
}
```

**Mark License as Checked:**
```bash
# First get current document
LICENSE=$(curl -s -u admin:password "http://localhost:5984/sw360db/LICENSE_ID")

# Extract revision
REV=$(echo $LICENSE | grep -o '"_rev":"[^"]*"' | cut -d'"' -f4)

# Update with checked=true
curl -X PUT -u admin:password "http://localhost:5984/sw360db/LICENSE_ID" \
  -H "Content-Type: application/json" \
  -d "$(echo $LICENSE | sed 's/"checked":false/"checked":true/')"
```

### 4. DELETE - Remove a License

**Delete License:**
```bash
curl -X DELETE -u admin:password \
  "http://localhost:5984/sw360db/LICENSE_ID?rev=REVISION"
```

**Example:**
```bash
curl -X DELETE -u admin:password \
  "http://localhost:5984/sw360db/1301e495e309a30f9e304974aa000fe2?rev=2-b7a670951e704bde51f232232c43b745"
```

## Common License Curation Workflows

### Workflow 1: Import New License

```bash
# Create comprehensive license entry
curl -X POST -u admin:password "http://localhost:5984/sw360db" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "license",
    "fullName": "GNU General Public License v3.0",
    "shortName": "GPL-3.0",
    "text": "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
    "OSIApproved": true,
    "checked": false,
    "externalIds": {
      "SPDX-License-Identifier": "GPL-3.0-or-later",
      "URL": "https://www.gnu.org/licenses/gpl-3.0.html"
    }
  }'
```

### Workflow 2: Review and Approve License

```bash
# 1. Find unchecked licenses
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","checked":false}}'

# 2. Get specific license for review
curl -s -u admin:password "http://localhost:5984/sw360db/LICENSE_ID"

# 3. Update and mark as checked
curl -X PUT -u admin:password "http://localhost:5984/sw360db/LICENSE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "_rev": "CURRENT_REV",
    "type": "license",
    "fullName": "Reviewed Name",
    "shortName": "SHORT",
    "text": "Reviewed and verified license text",
    "OSIApproved": true,
    "checked": true
  }'
```

### Workflow 3: Bulk License Import

```bash
# Import multiple licenses from a JSON file
cat licenses-to-import.json | while read line; do
  curl -X POST -u admin:password "http://localhost:5984/sw360db" \
    -H "Content-Type: application/json" \
    -d "$line"
done
```

**Example licenses-to-import.json:**
```json
{"type":"license","fullName":"BSD 3-Clause License","shortName":"BSD-3-Clause","OSIApproved":true,"checked":false}
{"type":"license","fullName":"ISC License","shortName":"ISC","OSIApproved":true,"checked":false}
{"type":"license","fullName":"Mozilla Public License 2.0","shortName":"MPL-2.0","OSIApproved":true,"checked":false}
```

### Workflow 4: Export All Licenses

```bash
# Export to JSON file
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}' > licenses-export.json

# Pretty print with jq (if installed)
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}' | jq '.' > licenses-export-pretty.json
```

## Advanced Queries

### Complex Selector Queries

**Find GPL licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{
    "selector": {
      "type": "license",
      "$or": [
        {"shortName": {"$regex": "(?i)gpl"}},
        {"fullName": {"$regex": "(?i)gnu general public"}}
      ]
    }
  }'
```

**Find OSI-approved and checked licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{
    "selector": {
      "type": "license",
      "OSIApproved": true,
      "checked": true
    }
  }'
```

**Get only specific fields:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{
    "selector": {"type": "license"},
    "fields": ["_id", "shortName", "fullName", "OSIApproved"]
  }'
```

**Sort licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{
    "selector": {"type": "license"},
    "sort": [{"shortName": "asc"}],
    "limit": 20
  }'
```

## Using CouchDB Web Interface (Fauxton)

### Access
1. Open browser: http://localhost:5984/_utils
2. Login: admin / password

### Visual License Management

**Create License:**
1. Click "Databases" → "sw360db"
2. Click "Create Document"
3. Add JSON:
```json
{
  "type": "license",
  "fullName": "New License",
  "shortName": "NEW",
  "OSIApproved": true,
  "checked": false
}
```
4. Click "Create Document"

**Query Licenses:**
1. Click "Databases" → "sw360db"
2. Click "Run A Query with Mango"
3. Enter selector:
```json
{
  "selector": {
    "type": "license"
  }
}
```
4. Click "Run Query"

**Edit License:**
1. Find license in database
2. Click on document ID
3. Modify fields
4. Click "Save Changes"

## Statistics and Monitoring

**Count Total Licenses:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"fields":["_id"]}' | \
  grep -o '"_id"' | wc -l
```

**Count OSI-Approved:**
```bash
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","OSIApproved":true},"fields":["_id"]}' | \
  grep -o '"_id"' | wc -l
```

**Count Checked vs Unchecked:**
```bash
echo "Checked:"
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","checked":true},"fields":["_id"]}' | \
  grep -o '"_id"' | wc -l

echo "Unchecked:"
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","checked":false},"fields":["_id"]}' | \
  grep -o '"_id"' | wc -l
```

## Helper Script Functions

Use the provided `linux-wsl-commands.sh` script:

```bash
# Load functions
source linux-wsl-commands.sh

# Create license
create_license "BSD 3-Clause" "BSD-3-Clause" "Redistribution and use..."

# Get license
get_license "1301e495e309a30f9e304974aa000fe2"

# Find by name
find_by_shortname "MIT"

# List all OSI-approved
get_osi_licenses

# Count licenses
count_licenses

# Pretty print (requires jq)
list_licenses_pretty
```

## Best Practices

### 1. License Naming
- Use official SPDX identifiers for `shortName` when available
- Check https://spdx.org/licenses/ for standard names
- Use consistent casing (e.g., "Apache-2.0" not "apache-2.0")

### 2. License Text
- Include complete license text in the `text` field
- Preserve original formatting and copyright notices
- For long licenses, ensure proper escaping of special characters

### 3. Metadata Management
- Set `OSIApproved: true` only for officially OSI-approved licenses
- Use `checked: false` for newly added licenses requiring review
- Update to `checked: true` after legal/compliance review

### 4. External IDs
- Always add SPDX identifier when available
- Include official URLs for reference
- Add any proprietary internal identifiers your organization uses

### 5. Revisions
- Always fetch current `_rev` before updating
- Never reuse old revision numbers
- If update fails with 409 conflict, fetch latest version and retry

### 6. Backup
- Regularly export all licenses to JSON files
- Use version control for exported license data
- Document any customizations or internal license additions

## Troubleshooting

### Error: "unauthorized"
```bash
# Check credentials
curl -u admin:password http://localhost:5984

# Verify database exists
curl -u admin:password http://localhost:5984/_all_dbs
```

### Error: "Document update conflict" (409)
```bash
# Always fetch latest revision before update
curl -s -u admin:password "http://localhost:5984/sw360db/LICENSE_ID"
# Use the _rev from response in your update
```

### Error: "No DB shards could be opened"
```bash
# Restart CouchDB container
docker restart sw360-stable-couchdb-1
```

### Empty Results
```bash
# Check if license type exists
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"limit":1}'

# If empty, no licenses exist yet - create one
```

## Data Validation

**Validate License Structure:**
```bash
# Get a license and validate required fields
LICENSE=$(curl -s -u admin:password "http://localhost:5984/sw360db/LICENSE_ID")

# Check required fields exist
echo $LICENSE | jq 'if .type and .fullName and .shortName then "Valid" else "Invalid - missing required fields" end'
```

**Check for Duplicates:**
```bash
# Find licenses with same short name
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license","shortName":"MIT"}}'
```

## Integration with SW360

When you eventually deploy the full SW360 frontend (Liferay), all licenses you create now will be:
- ✅ Automatically available in the web interface
- ✅ Accessible via REST API
- ✅ Usable for component and project license associations
- ✅ Included in license compliance reports

Your license curation work via CouchDB is production-ready and future-proof!

## Quick Reference Card

```bash
# List all
curl -s -u admin:password "http://localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" -d '{"selector":{"type":"license"}}'

# Create
curl -X POST -u admin:password "http://localhost:5984/sw360db" \
  -H "Content-Type: application/json" -d '{"type":"license",...}'

# Get one
curl -s -u admin:password "http://localhost:5984/sw360db/ID"

# Update
curl -X PUT -u admin:password "http://localhost:5984/sw360db/ID" \
  -H "Content-Type: application/json" -d '{"_rev":"REV",...}'

# Delete
curl -X DELETE -u admin:password "http://localhost:5984/sw360db/ID?rev=REV"

# Web UI
http://localhost:5984/_utils (admin/password)
```

## Support Resources

- CouchDB Documentation: https://docs.couchdb.org/
- Mango Query Guide: https://docs.couchdb.org/en/stable/api/database/find.html
- SPDX License List: https://spdx.org/licenses/
- SW360 Documentation: https://eclipse.dev/sw360/

---

**You are now ready to curate licenses directly in SW360's CouchDB backend!** 🚀
