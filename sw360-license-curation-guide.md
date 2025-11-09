# SW360 License Curation Guide - REST API

## Current Setup Status

### Services Running
- **SW360 Backend**: http://localhost:8080
- **CouchDB**: http://localhost:5984 (admin/password)
- **Resource Server (REST API)**: Deployed and running
- **Authorization Server**: Deployed but OAuth endpoints not accessible

### OAuth Client Configuration
- Client ID: `trusted-sw360-client`
- Client Secret: `sw360-secret`
- Database: `sw360oauthclients` (created in CouchDB)

## Authentication Challenge

The OAuth endpoints are not accessible at the expected paths:
- ❌ `http://localhost:8080/authorization/oauth/token` - 404
- ❌ `http://localhost:8080/oauth/token` - 404
- ❌ `http://localhost:8080/authorization/client-management` - 404
- ❌ `http://localhost:8090/oauth/token` - Connection refused

### Root Cause
The authorization service (Spring Boot app) runs embedded in Tomcat but the endpoint mappings suggest it may need:
1. A web UI session to access `/client-management` (requires ADMIN authority)
2. Liferay integration for user authentication
3. Pre-configured users in the system

## License Curation Workflow (Once Authenticated)

### 1. Get OAuth Token
```bash
curl -X POST --user 'trusted-sw360-client:sw360-secret' \
  -d 'grant_type=password&username=<USER>&password=<PASSWORD>' \
  http://localhost:8080/authorization/oauth/token
```

Expected Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGci...",
  "expires_in": 1800,
  "scope": "READ WRITE ADMIN"
}
```

### 2. List All Licenses
```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://localhost:8080/resource/api/licenses
```

### 3. Get Specific License
```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://localhost:8080/resource/api/licenses/<LICENSE_ID>
```

### 4. Create a New License
```bash
curl -X POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Apache License 2.0",
    "shortName": "Apache-2.0",
    "text": "Licensed under the Apache License, Version 2.0...",
    "OSIApproved": true,
    "checked": false
  }' \
  http://localhost:8080/resource/api/licenses
```

### 5. Update License
```bash
curl -X PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated license text here",
    "checked": true
  }' \
  http://localhost:8080/resource/api/licenses/<LICENSE_ID>
```

### 6. Delete License
```bash
curl -X DELETE \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://localhost:8080/resource/api/licenses/<LICENSE_ID>
```

## License Object Structure

```json
{
  "fullName": "String - Full license name",
  "shortName": "String - SPDX identifier or short name",
  "text": "String - Full license text",
  "OSIApproved": "Boolean - OSI approval status",
  "checked": "Boolean - Review status",
  "licenseType": {
    "licenseType": "String",
    "licenseTypeId": "Number"
  },
  "externalIds": {
    "SPDX-License-Identifier": "Apache-2.0"
  },
  "_links": {
    "self": {
      "href": "http://localhost:8080/resource/api/licenses/<ID>"
    }
  }
}
```

## Alternative: Direct CouchDB Access

Since OAuth is not working, you can directly manipulate licenses in CouchDB:

### Access CouchDB Admin Interface
Open http://localhost:5984/_utils in your browser
- Username: `admin`
- Password: `password`

### License Database
Licenses are stored in the `sw360db` database under document type `license`.

### Example CouchDB Query
```bash
curl http://admin:password@localhost:5984/sw360db/_all_docs?include_docs=true
```

## Next Steps to Resolve OAuth

1. **Build SW360 from Source** with full Liferay frontend
   - This provides the web UI for user management
   - Enables client-management interface
   - Full OAuth flow support

2. **Create Admin User** in Liferay
   - Required to access `/client-management` endpoint
   - Needed for managing OAuth clients

3. **Use Hosted SW360 Instance**
   - https://sw360.eclipse.org/ (if available)
   - Pre-configured authentication
   - Full web interface

## Resources

- SW360 Documentation: https://eclipse.dev/sw360/
- REST API Docs: https://eclipse.dev/sw360/docs/development/restapi/
- GitHub Repository: https://github.com/eclipse-sw360/sw360
- CouchDB Documentation: https://docs.couchdb.org/

## Summary

The SW360 backend services are running correctly, but the Docker image doesn't include:
- Liferay web frontend (ROOT.war)
- Pre-configured admin users
- Accessible OAuth endpoints without web UI session

To fully use SW360 for license curation, you would need either:
1. The complete build including Liferay (30+ minutes build time)
2. Access to a fully deployed SW360 instance
3. Direct CouchDB manipulation (bypasses SW360 business logic)
