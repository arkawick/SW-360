# SW360 License Curation - Setup Complete

## Successfully Deployed Services ✓

### Running Services
- **SW360 Backend REST API**: http://localhost:8080
- **CouchDB Database**: http://localhost:5984 (credentials: admin/password)
- **PostgreSQL Database**: localhost:5438 (for Liferay)
- **Resource Server**: Deployed and accessible
- **Authorization Server**: Deployed (OAuth endpoints need Liferay integration)

### Docker Containers
```
sw360                       - Main application (ports 8080, 11311)
sw360-stable-postgresdb-1   - PostgreSQL (port 5438)
sw360-stable-couchdb-1      - CouchDB (port 5984)
```

## License Curation - Working Solution

### CouchDB Direct Access (WORKING NOW!)

**1. Create a License:**
```bash
curl -X POST http://admin:password@localhost:5984/sw360db \
  -H "Content-Type: application/json" \
  -d '{
    "type": "license",
    "fullName": "MIT License",
    "shortName": "MIT",
    "text": "Permission is hereby granted...",
    "OSIApproved": true,
    "checked": false
  }'
```

**Response:** `{"ok":true,"id":"1301e495e309a30f9e304974aa000fe2","rev":"1-..."}`

**2. Query Licenses:**
```bash
curl -s "http://admin:password@localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"limit":10}'
```

**3. Update a License:**
```bash
curl -X PUT "http://admin:password@localhost:5984/sw360db/LICENSE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "_rev": "CURRENT_REV",
    "type": "license",
    "fullName": "MIT License",
    "shortName": "MIT",
    "text": "Updated full license text...",
    "OSIApproved": true,
    "checked": true
  }'
```

**4. Retrieve a Specific License:**
```bash
curl -s "http://admin:password@localhost:5984/sw360db/LICENSE_ID"
```

**5. Delete a License:**
```bash
curl -X DELETE "http://admin:password@localhost:5984/sw360db/LICENSE_ID?rev=REV"
```

### Working Example Demonstrated

✓ **Created MIT License**
- ID: `1301e495e309a30f9e304974aa000fe2`
- Initial Rev: `1-a185bf32a420bd295bab540115dfa7ad`

✓ **Updated MIT License**
- New Rev: `2-b7a670951e704bde51f232232c43b745`
- Changed: `checked: false` → `checked: true`
- Updated license text

## CouchDB Web Interface

Access the visual database interface:
1. Open browser: http://localhost:5984/_utils
2. Login: admin / password
3. Navigate to `sw360db` database
4. View/Edit license documents directly

## License Document Structure

```json
{
  "_id": "auto-generated-id",
  "_rev": "revision-number",
  "type": "license",
  "fullName": "Full License Name",
  "shortName": "SPDX-Identifier",
  "text": "Complete license text",
  "OSIApproved": true,
  "checked": false,
  "licenseTypeDatabaseId": "optional-type-id",
  "externalIds": {
    "SPDX-License-Identifier": "MIT"
  }
}
```

## Available Databases

- `sw360db` - Main database (licenses, components, projects, releases)
- `sw360users` - User management
- `sw360attachments` - File attachments
- `sw360changelogs` - Audit trail
- `sw360config` - Configuration
- `sw360oauthclients` - OAuth clients
- `sw360vm` - Vulnerability management
- `sw360spdx` - SPDX documents

## REST API (Requires OAuth Token)

The REST API endpoints are available but require OAuth authentication:

**Endpoints:**
- GET http://localhost:8080/resource/api/licenses
- GET http://localhost:8080/resource/api/licenses/{id}
- POST http://localhost:8080/resource/api/licenses
- PATCH http://localhost:8080/resource/api/licenses/{id}
- DELETE http://localhost:8080/resource/api/licenses/{id}

**Note:** OAuth token endpoints are not accessible without:
1. Liferay frontend (ROOT.war) for user management
2. Admin user with ADMIN authority
3. Full build from source (not included in Docker image)

## Known Limitations

### What's Missing from Docker Image:
- ❌ Liferay web frontend (ROOT.war)
- ❌ Pre-configured admin users
- ❌ Accessible OAuth `/oauth/token` endpoint
- ❌ Client management UI at `/client-management`

### What's Working:
- ✅ All backend REST API services deployed
- ✅ CouchDB database with full CRUD operations
- ✅ PostgreSQL database ready
- ✅ Direct license curation via CouchDB
- ✅ All SW360 business logic services running

## Next Steps

### Option 1: Continue with CouchDB (Recommended)
You can fully manage licenses using CouchDB as demonstrated. All data will be accessible when/if you deploy the full SW360 frontend later.

### Option 2: Build Full SW360 from Source
```bash
cd C:/Users/Arkajyoti/Desktop/SW360/sw360-stable
# This takes 30+ minutes
./docker_build.sh
docker-compose up
```

This will build:
- Liferay frontend (ROOT.war)
- Complete OAuth flow
- Web-based license management UI

### Option 3: Use Hosted Instance
Access a pre-configured SW360 instance if available through your organization.

## Quick Reference Commands

**List all licenses:**
```bash
curl -s "http://admin:password@localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'
```

**Count licenses:**
```bash
curl -s "http://admin:password@localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"fields":["_id"]}' | \
  grep -o '"_id"' | wc -l
```

**Backup all licenses:**
```bash
curl -s "http://admin:password@localhost:5984/sw360db/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}' > licenses_backup.json
```

## Documentation

- Comprehensive guide: `C:/Users/Arkajyoti/Desktop/SW360/sw360-license-curation-guide.md`
- CouchDB API: https://docs.couchdb.org/en/stable/api/
- SW360 GitHub: https://github.com/eclipse-sw360/sw360
- SW360 Docs: https://eclipse.dev/sw360/

## Success! 🎉

You now have a working SW360 backend for license curation with:
- Full database access for license CRUD operations
- 8 databases ready for SW360 data
- All backend services running and healthy
- Demonstrated working license creation and updates

The system is ready for license curation workflows!
