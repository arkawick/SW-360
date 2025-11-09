#!/bin/bash
# SW360 License Curation - Linux/WSL/Git Bash Commands

# CouchDB credentials
COUCHDB_USER="admin"
COUCHDB_PASS="password"
COUCHDB_URL="http://localhost:5984"
DB_NAME="sw360db"

# 1. Test CouchDB connection
echo "=== Testing CouchDB Connection ==="
curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL"
echo -e "\n"

# 2. List all databases
echo "=== List All Databases ==="
curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/_all_dbs"
echo -e "\n"

# 3. Query all licenses
echo "=== Query All Licenses ==="
curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"}}'
echo -e "\n"

# 4. Query licenses with limit
echo "=== Query Licenses (Limit 5) ==="
curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector":{"type":"license"},"limit":5}'
echo -e "\n"

# 5. Create a new license
create_license() {
    local FULLNAME=$1
    local SHORTNAME=$2
    local TEXT=$3

    echo "=== Create New License: $SHORTNAME ==="
    curl -X POST -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME" \
      -H "Content-Type: application/json" \
      -d "{
        \"type\": \"license\",
        \"fullName\": \"$FULLNAME\",
        \"shortName\": \"$SHORTNAME\",
        \"text\": \"$TEXT\",
        \"OSIApproved\": true,
        \"checked\": false
      }"
    echo -e "\n"
}

# Example: Create GPL-3.0
# create_license "GNU General Public License v3.0" "GPL-3.0" "This program is free software..."

# 6. Get specific license by ID
get_license() {
    local LICENSE_ID=$1
    echo "=== Get License: $LICENSE_ID ==="
    curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/$LICENSE_ID"
    echo -e "\n"
}

# Example: get_license "1301e495e309a30f9e304974aa000fe2"

# 7. Update a license
update_license() {
    local LICENSE_ID=$1
    local REV=$2
    local FULLNAME=$3
    local SHORTNAME=$4
    local TEXT=$5

    echo "=== Update License: $LICENSE_ID ==="
    curl -X PUT -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/$LICENSE_ID" \
      -H "Content-Type: application/json" \
      -d "{
        \"_rev\": \"$REV\",
        \"type\": \"license\",
        \"fullName\": \"$FULLNAME\",
        \"shortName\": \"$SHORTNAME\",
        \"text\": \"$TEXT\",
        \"OSIApproved\": true,
        \"checked\": true
      }"
    echo -e "\n"
}

# 8. Delete a license
delete_license() {
    local LICENSE_ID=$1
    local REV=$2
    echo "=== Delete License: $LICENSE_ID ==="
    curl -X DELETE -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/$LICENSE_ID?rev=$REV"
    echo -e "\n"
}

# 9. Search licenses by short name
find_by_shortname() {
    local SHORTNAME=$1
    echo "=== Find Licenses: $SHORTNAME ==="
    curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
      -H "Content-Type: application/json" \
      -d "{\"selector\":{\"type\":\"license\",\"shortName\":\"$SHORTNAME\"}}"
    echo -e "\n"
}

# 10. Get checked licenses
get_checked_licenses() {
    echo "=== Get Checked Licenses ==="
    curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
      -H "Content-Type: application/json" \
      -d '{"selector":{"type":"license","checked":true}}'
    echo -e "\n"
}

# 11. Get OSI approved licenses
get_osi_licenses() {
    echo "=== Get OSI Approved Licenses ==="
    curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
      -H "Content-Type: application/json" \
      -d '{"selector":{"type":"license","OSIApproved":true}}'
    echo -e "\n"
}

# 12. Count all licenses
count_licenses() {
    echo "=== Count All Licenses ==="
    curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
      -H "Content-Type: application/json" \
      -d '{"selector":{"type":"license"},"fields":["_id"]}' | \
      grep -o '"_id"' | wc -l
}

# 13. Pretty print licenses with jq (if available)
list_licenses_pretty() {
    if command -v jq &> /dev/null; then
        echo "=== Licenses (Pretty Printed) ==="
        curl -s -u $COUCHDB_USER:$COUCHDB_PASS "$COUCHDB_URL/$DB_NAME/_find" \
          -H "Content-Type: application/json" \
          -d '{"selector":{"type":"license"}}' | jq '.'
    else
        echo "Install jq for pretty JSON output"
        echo "Linux: sudo apt-get install jq"
        echo "macOS: brew install jq"
    fi
}

# Show usage
show_usage() {
    echo "SW360 License Curation Helper Script"
    echo "====================================="
    echo ""
    echo "Functions available:"
    echo "  create_license <fullname> <shortname> <text>"
    echo "  get_license <license_id>"
    echo "  update_license <license_id> <rev> <fullname> <shortname> <text>"
    echo "  delete_license <license_id> <rev>"
    echo "  find_by_shortname <shortname>"
    echo "  get_checked_licenses"
    echo "  get_osi_licenses"
    echo "  count_licenses"
    echo "  list_licenses_pretty"
    echo ""
    echo "Examples:"
    echo "  source linux-wsl-commands.sh"
    echo "  create_license 'BSD 3-Clause' 'BSD-3-Clause' 'Redistribution and use...'"
    echo "  get_license '1301e495e309a30f9e304974aa000fe2'"
    echo "  find_by_shortname 'MIT'"
    echo "  count_licenses"
}

# If script is executed (not sourced), show usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_usage
fi
