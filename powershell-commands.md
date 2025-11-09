# SW360 License Curation - PowerShell Commands

## Important: Use curl.exe in PowerShell

PowerShell has its own `curl` alias that points to `Invoke-WebRequest` with different syntax.
Always use `curl.exe` instead of `curl` in PowerShell.

## Working Commands for PowerShell

### 1. List All Databases
```powershell
curl.exe -s http://admin:password@localhost:5984/_all_dbs
```

### 2. Query Licenses
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"},\"limit\":10}"
```

### 3. Create a License
```powershell
curl.exe -X POST "http://admin:password@localhost:5984/sw360db" `
  -H "Content-Type: application/json" `
  -d "{\"type\":\"license\",\"fullName\":\"Apache License 2.0\",\"shortName\":\"Apache-2.0\",\"text\":\"Licensed under Apache 2.0\",\"OSIApproved\":true,\"checked\":false}"
```

### 4. Get Specific License
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/LICENSE_ID"
```

### 5. Update a License
```powershell
curl.exe -X PUT "http://admin:password@localhost:5984/sw360db/LICENSE_ID" `
  -H "Content-Type: application/json" `
  -d "{\"_rev\":\"CURRENT_REV\",\"type\":\"license\",\"fullName\":\"Updated Name\",\"shortName\":\"SHORT\",\"text\":\"Updated text\",\"OSIApproved\":true,\"checked\":true}"
```

### 6. Delete a License
```powershell
curl.exe -X DELETE "http://admin:password@localhost:5984/sw360db/LICENSE_ID?rev=REV"
```

### 7. List All Documents (including licenses)
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_all_docs?limit=10"
```

### 8. Get All Licenses with Full Documents
```powershell
curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
  -H "Content-Type: application/json" `
  -d "{\"selector\":{\"type\":\"license\"}}"
```

## Alternative: Use PowerShell Native (Invoke-RestMethod)

If you prefer PowerShell's native commands:

### Query Licenses
```powershell
$uri = "http://localhost:5984/sw360db/_find"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    selector = @{
        type = "license"
    }
    limit = 10
} | ConvertTo-Json

$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:password"))
$headers["Authorization"] = "Basic $cred"

Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
```

### Create License
```powershell
$uri = "http://localhost:5984/sw360db"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    type = "license"
    fullName = "BSD 3-Clause License"
    shortName = "BSD-3-Clause"
    text = "Copyright (c) ..."
    OSIApproved = $true
    checked = $false
} | ConvertTo-Json

$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:password"))
$headers["Authorization"] = "Basic $cred"

Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
```

## CouchDB Web Interface (Easiest Option)

The easiest way to work with licenses in Windows:

1. Open your browser
2. Go to: http://localhost:5984/_utils
3. Login: admin / password
4. Click on "sw360db" database
5. Use the visual interface to:
   - Create new documents
   - Edit existing licenses
   - Query with Mango queries
   - View all license documents

## Common PowerShell Mistakes to Avoid

❌ **Wrong:** `curl http://admin:password@localhost:5984/...`
✅ **Right:** `curl.exe http://admin:password@localhost:5984/...`

❌ **Wrong:** `-H "Content-Type: application/json"`
✅ **Right:** `-H "Content-Type: application/json"` (use curl.exe, not curl)

❌ **Wrong:** `-d '{"key":"value"}'` (single quotes don't work in PowerShell JSON)
✅ **Right:** `-d "{\"key\":\"value\"}"` (escape double quotes)

## Quick Test Commands

### Test 1: Check CouchDB is accessible
```powershell
curl.exe http://admin:password@localhost:5984
```

Expected output: `{"couchdb":"Welcome","version":"3.4.2",...}`

### Test 2: List all databases
```powershell
curl.exe http://admin:password@localhost:5984/_all_dbs
```

Expected output: `["sw360attachments","sw360changelogs",...]`

### Test 3: Get the MIT license we created
```powershell
curl.exe http://admin:password@localhost:5984/sw360db/1301e495e309a30f9e304974aa000fe2
```

Expected output: Full MIT license document

## Tips

1. **Always use `curl.exe`** in PowerShell to get the real curl command
2. **Escape quotes** in JSON strings with backslash: `\"`
3. **Use backtick `` ` ``** for line continuation in PowerShell
4. **Use the web interface** at http://localhost:5984/_utils for visual management
5. **Save common queries** as PowerShell functions for reuse

## Example: Reusable PowerShell Function

```powershell
function Get-SW360Licenses {
    param(
        [int]$Limit = 10
    )

    $result = curl.exe -s "http://admin:password@localhost:5984/sw360db/_find" `
        -H "Content-Type: application/json" `
        -d "{\"selector\":{\"type\":\"license\"},\"limit\":$Limit}"

    return $result | ConvertFrom-Json
}

# Usage
Get-SW360Licenses -Limit 5
```

## Save this file for reference!

Location: `C:\Users\Arkajyoti\Desktop\SW360\powershell-commands.md`
