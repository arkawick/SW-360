#!/usr/bin/env python3
"""
SW360 License Manager - Python Interface for CouchDB License Curation

This module provides a Python interface for managing licenses in SW360's CouchDB database.
No external dependencies required - uses only Python standard library.
"""

import json
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, List, Optional, Any
from base64 import b64encode


class SW360LicenseManager:
    """
    Main class for managing SW360 licenses via CouchDB REST API.

    Usage:
        manager = SW360LicenseManager(
            url="http://localhost:5984",
            username="admin",
            password="password",
            database="sw360db"
        )

        # List all licenses
        licenses = manager.list_licenses()

        # Create a new license
        result = manager.create_license(
            full_name="MIT License",
            short_name="MIT",
            text="Permission is hereby granted...",
            osi_approved=True
        )
    """

    def __init__(
        self,
        url: str = "http://localhost:5984",
        username: str = "admin",
        password: str = "password",
        database: str = "sw360db"
    ):
        """
        Initialize the SW360 License Manager.

        Args:
            url: CouchDB server URL (default: http://localhost:5984)
            username: CouchDB username (default: admin)
            password: CouchDB password (default: password)
            database: Database name (default: sw360db)
        """
        self.url = url.rstrip('/')
        self.database = database
        self.db_url = f"{self.url}/{self.database}"

        # Create basic auth header
        credentials = f"{username}:{password}"
        encoded_credentials = b64encode(credentials.encode('utf-8')).decode('ascii')
        self.auth_header = f"Basic {encoded_credentials}"

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to CouchDB.

        Args:
            endpoint: API endpoint (e.g., "/_find", "/document_id")
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request body data (will be JSON encoded)

        Returns:
            Response data as dictionary

        Raises:
            Exception: If request fails
        """
        url = f"{self.db_url}{endpoint}"

        headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json"
        }

        request_data = None
        if data:
            request_data = json.dumps(data).encode('utf-8')

        request = urllib.request.Request(
            url,
            data=request_data,
            headers=headers,
            method=method
        )

        try:
            with urllib.request.urlopen(request) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
        except urllib.error.HTTPError as e:
            error_data = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code} Error: {error_data}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to CouchDB server.

        Returns:
            Server information
        """
        request = urllib.request.Request(
            self.url,
            headers={"Authorization": self.auth_header}
        )
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode('utf-8'))

    def list_databases(self) -> List[str]:
        """
        List all databases on the CouchDB server.

        Returns:
            List of database names
        """
        request = urllib.request.Request(
            f"{self.url}/_all_dbs",
            headers={"Authorization": self.auth_header}
        )
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode('utf-8'))

    def list_licenses(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all licenses in the database.

        Args:
            limit: Maximum number of licenses to return (None = all)

        Returns:
            List of license documents
        """
        query = {"selector": {"type": "license"}}
        if limit:
            query["limit"] = limit

        result = self._make_request("/_find", method="POST", data=query)
        return result.get("docs", [])

    def create_license(
        self,
        full_name: str,
        short_name: str,
        text: str = "",
        osi_approved: bool = False,
        checked: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new license in the database.

        Args:
            full_name: Full license name (e.g., "MIT License")
            short_name: SPDX identifier (e.g., "MIT")
            text: Full license text
            osi_approved: Whether the license is OSI approved
            checked: Whether the license has been reviewed
            **kwargs: Additional fields to include

        Returns:
            Response containing 'ok', 'id', and 'rev'

        Example:
            result = manager.create_license(
                full_name="BSD 3-Clause License",
                short_name="BSD-3-Clause",
                text="Redistribution and use in source and binary forms...",
                osi_approved=True,
                checked=False
            )
            print(f"Created license with ID: {result['id']}")
        """
        license_doc = {
            "type": "license",
            "fullName": full_name,
            "shortName": short_name,
            "text": text,
            "OSIApproved": osi_approved,
            "checked": checked,
            **kwargs
        }

        return self._make_request("", method="POST", data=license_doc)

    def get_license(self, license_id: str) -> Dict[str, Any]:
        """
        Get a specific license by ID.

        Args:
            license_id: The license document ID

        Returns:
            License document
        """
        return self._make_request(f"/{license_id}")

    def update_license(
        self,
        license_id: str,
        rev: str,
        full_name: str,
        short_name: str,
        text: str = "",
        osi_approved: bool = False,
        checked: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing license.

        Args:
            license_id: The license document ID
            rev: Current revision number (required by CouchDB)
            full_name: Full license name
            short_name: SPDX identifier
            text: Full license text
            osi_approved: Whether the license is OSI approved
            checked: Whether the license has been reviewed
            **kwargs: Additional fields to include

        Returns:
            Response containing 'ok', 'id', and 'rev'

        Example:
            license = manager.get_license("license_id_here")
            result = manager.update_license(
                license_id=license["_id"],
                rev=license["_rev"],
                full_name=license["fullName"],
                short_name=license["shortName"],
                text=license["text"],
                checked=True  # Mark as reviewed
            )
        """
        license_doc = {
            "_rev": rev,
            "type": "license",
            "fullName": full_name,
            "shortName": short_name,
            "text": text,
            "OSIApproved": osi_approved,
            "checked": checked,
            **kwargs
        }

        return self._make_request(f"/{license_id}", method="PUT", data=license_doc)

    def delete_license(self, license_id: str, rev: str) -> Dict[str, Any]:
        """
        Delete a license from the database.

        Args:
            license_id: The license document ID
            rev: Current revision number (required by CouchDB)

        Returns:
            Response containing 'ok', 'id', and 'rev'

        Warning:
            This permanently deletes the license document!
        """
        return self._make_request(f"/{license_id}?rev={rev}", method="DELETE")

    def find_by_short_name(self, short_name: str) -> List[Dict[str, Any]]:
        """
        Find licenses by short name (SPDX identifier).

        Args:
            short_name: License short name (e.g., "MIT", "Apache-2.0")

        Returns:
            List of matching license documents
        """
        query = {
            "selector": {
                "type": "license",
                "shortName": short_name
            }
        }
        result = self._make_request("/_find", method="POST", data=query)
        return result.get("docs", [])

    def get_osi_approved_licenses(self) -> List[Dict[str, Any]]:
        """
        Get all OSI approved licenses.

        Returns:
            List of OSI approved license documents
        """
        query = {
            "selector": {
                "type": "license",
                "OSIApproved": True
            }
        }
        result = self._make_request("/_find", method="POST", data=query)
        return result.get("docs", [])

    def get_checked_licenses(self) -> List[Dict[str, Any]]:
        """
        Get all reviewed/checked licenses.

        Returns:
            List of checked license documents
        """
        query = {
            "selector": {
                "type": "license",
                "checked": True
            }
        }
        result = self._make_request("/_find", method="POST", data=query)
        return result.get("docs", [])

    def get_unchecked_licenses(self) -> List[Dict[str, Any]]:
        """
        Get all unreviewed/unchecked licenses.

        Returns:
            List of unchecked license documents
        """
        query = {
            "selector": {
                "type": "license",
                "checked": False
            }
        }
        result = self._make_request("/_find", method="POST", data=query)
        return result.get("docs", [])

    def count_licenses(self) -> int:
        """
        Count total number of licenses.

        Returns:
            Number of licenses in database
        """
        query = {
            "selector": {"type": "license"},
            "fields": ["_id"]
        }
        result = self._make_request("/_find", method="POST", data=query)
        return len(result.get("docs", []))

    def search_licenses(self, search_text: str, fields: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for licenses by text in specified fields.

        Args:
            search_text: Text to search for
            fields: List of fields to search in (default: ["fullName", "shortName", "text"])

        Returns:
            List of matching license documents

        Note:
            This performs a case-sensitive substring search.
            For case-insensitive search, convert search_text to lowercase
            and search in lowercase versions of fields.
        """
        if fields is None:
            fields = ["fullName", "shortName", "text"]

        # Get all licenses and filter in Python (CouchDB has limited text search)
        all_licenses = self.list_licenses()
        results = []

        for license in all_licenses:
            for field in fields:
                if field in license and search_text.lower() in str(license[field]).lower():
                    results.append(license)
                    break

        return results


# Convenience functions for quick operations

def print_license(license: Dict[str, Any], detailed: bool = False):
    """
    Pretty print a license document.

    Args:
        license: License document
        detailed: If True, print all fields; if False, print summary
    """
    print(f"\n{'='*60}")
    print(f"Short Name: {license.get('shortName', 'N/A')}")
    print(f"Full Name:  {license.get('fullName', 'N/A')}")
    print(f"ID:         {license.get('_id', 'N/A')}")
    print(f"Revision:   {license.get('_rev', 'N/A')}")
    print(f"OSI Approved: {license.get('OSIApproved', False)}")
    print(f"Checked:    {license.get('checked', False)}")

    if detailed:
        text = license.get('text', '')
        if text:
            print(f"\nLicense Text:")
            print(f"{'-'*60}")
            print(text[:500] + ('...' if len(text) > 500 else ''))
    print(f"{'='*60}\n")


def main():
    """
    Example usage and interactive testing.
    """
    print("SW360 License Manager - Python Interface")
    print("=" * 60)

    # Initialize manager
    manager = SW360LicenseManager()

    try:
        # Test connection
        print("\n1. Testing CouchDB connection...")
        info = manager.test_connection()
        print(f"[OK] Connected to CouchDB {info.get('version', 'unknown')}")

        # List databases
        print("\n2. Listing databases...")
        databases = manager.list_databases()
        print(f"[OK] Found {len(databases)} databases")
        if "sw360db" in databases:
            print("[OK] sw360db database exists")

        # Count licenses
        print("\n3. Counting licenses...")
        count = manager.count_licenses()
        print(f"[OK] Found {count} licenses in database")

        # List licenses
        print("\n4. Listing all licenses...")
        licenses = manager.list_licenses(limit=10)
        print(f"[OK] Retrieved {len(licenses)} licenses")

        for license in licenses:
            print(f"  - {license.get('shortName', 'N/A')}: {license.get('fullName', 'N/A')}")

        # Example: Create a new license (commented out to avoid duplicates)
        """
        print("\n5. Creating a new license...")
        result = manager.create_license(
            full_name="GNU General Public License v3.0",
            short_name="GPL-3.0",
            text="This program is free software: you can redistribute it...",
            osi_approved=True,
            checked=False
        )
        print(f"[OK] Created license with ID: {result['id']}")
        """

        # Example: Search for MIT license
        print("\n5. Searching for MIT license...")
        mit_licenses = manager.find_by_short_name("MIT")
        if mit_licenses:
            print(f"[OK] Found {len(mit_licenses)} MIT license(s)")
            print_license(mit_licenses[0])
        else:
            print("[WARN] No MIT license found")

        # Get OSI approved licenses
        print("\n6. Getting OSI approved licenses...")
        osi_licenses = manager.get_osi_approved_licenses()
        print(f"[OK] Found {len(osi_licenses)} OSI approved licenses")

        # Get checked licenses
        print("\n7. Getting checked licenses...")
        checked_licenses = manager.get_checked_licenses()
        print(f"[OK] Found {len(checked_licenses)} checked licenses")

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
