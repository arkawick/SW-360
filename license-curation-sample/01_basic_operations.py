#!/usr/bin/env python3
"""
License Curation Sample - Basic Operations

This script demonstrates basic license curation operations:
1. Connecting to CouchDB
2. Creating a new license
3. Searching for licenses
4. Retrieving license details
5. Updating a license
6. Deleting a license (optional)

Prerequisites:
- SW360 backend running (docker compose up -d)
- CouchDB accessible at http://localhost:5984
"""

import sys
import os

# Add parent directory to path to import sw360_license_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sw360_license_manager import SW360LicenseManager


def print_separator(title=""):
    """Print a visual separator"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print("-" * 60)


def print_license_info(license_data):
    """Print license information in a formatted way"""
    print(f"  ID:           {license_data.get('_id', 'N/A')}")
    print(f"  Revision:     {license_data.get('_rev', 'N/A')}")
    print(f"  Short Name:   {license_data.get('shortName', 'N/A')}")
    print(f"  Full Name:    {license_data.get('fullName', 'N/A')}")
    print(f"  OSI Approved: {license_data.get('OSIApproved', False)}")
    print(f"  Checked:      {license_data.get('checked', False)}")
    print(f"  Text Preview: {license_data.get('text', '')[:80]}...")


def main():
    print_separator("License Curation - Basic Operations Demo")

    # Initialize the license manager
    print("[1] Initializing SW360 License Manager...")
    manager = SW360LicenseManager()

    # Test connection
    if not manager.test_connection():
        print("[ERROR] Could not connect to CouchDB. Please ensure:")
        print("  - Docker containers are running: docker ps")
        print("  - CouchDB is accessible at http://localhost:5984")
        return 1

    print("[OK] Connected to CouchDB successfully!\n")

    # ========================================================================
    # STEP 1: Check if license already exists
    # ========================================================================
    print_separator("STEP 1: Checking for existing license")

    license_short_name = "BSD-2-Clause"
    existing_licenses = manager.find_by_short_name(license_short_name)

    if existing_licenses:
        print(f"[INFO] License '{license_short_name}' already exists in database")
        print(f"[INFO] Found {len(existing_licenses)} matching license(s)")
        license = existing_licenses[0]
        print_license_info(license)
        license_id = license['_id']
    else:
        print(f"[INFO] License '{license_short_name}' not found")

        # ====================================================================
        # STEP 2: Create a new license
        # ====================================================================
        print_separator("STEP 2: Creating new license")

        license_data = {
            "full_name": "BSD 2-Clause 'Simplified' License",
            "short_name": "BSD-2-Clause",
            "text": "Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\n1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n\n2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.",
            "osi_approved": True,
            "checked": False
        }

        print(f"[*] Creating license: {license_data['short_name']}")
        result = manager.create_license(
            full_name=license_data['full_name'],
            short_name=license_data['short_name'],
            text=license_data['text'],
            osi_approved=license_data['osi_approved'],
            checked=license_data['checked']
        )

        if result and result.get('ok'):
            print(f"[OK] License created successfully!")
            print(f"    ID: {result.get('id')}")
            print(f"    Revision: {result.get('rev')}")
            license_id = result.get('id')
        else:
            print("[ERROR] Failed to create license")
            return 1

    # ========================================================================
    # STEP 3: Retrieve the license details
    # ========================================================================
    print_separator("STEP 3: Retrieving license details")

    print(f"[*] Fetching license by ID: {license_id}")
    license = manager.get_license(license_id)

    if license:
        print("[OK] License retrieved successfully!")
        print_license_info(license)
    else:
        print("[ERROR] Could not retrieve license")
        return 1

    # ========================================================================
    # STEP 4: Search for license by short name
    # ========================================================================
    print_separator("STEP 4: Searching licenses by short name")

    search_term = "BSD-2-Clause"
    print(f"[*] Searching for: {search_term}")
    results = manager.find_by_short_name(search_term)

    print(f"[OK] Found {len(results)} matching license(s)")
    for idx, lic in enumerate(results, 1):
        print(f"\n  Result {idx}:")
        print_license_info(lic)

    # ========================================================================
    # STEP 5: Update the license (mark as checked/reviewed)
    # ========================================================================
    print_separator("STEP 5: Updating license (marking as checked)")

    # First, get the current revision
    current_license = manager.get_license(license_id)

    print(f"[*] Current status: Checked = {current_license.get('checked', False)}")
    print(f"[*] Marking license as checked/reviewed...")

    update_result = manager.update_license(
        license_id=current_license['_id'],
        rev=current_license['_rev'],
        full_name=current_license['fullName'],
        short_name=current_license['shortName'],
        text=current_license['text'],
        osi_approved=current_license['OSIApproved'],
        checked=True  # Mark as checked
    )

    if update_result and update_result.get('ok'):
        print("[OK] License updated successfully!")
        print(f"    New Revision: {update_result.get('rev')}")

        # Verify the update
        updated_license = manager.get_license(license_id)
        print(f"[OK] Verified: Checked = {updated_license.get('checked', False)}")
    else:
        print("[ERROR] Failed to update license")
        return 1

    # ========================================================================
    # STEP 6: View statistics
    # ========================================================================
    print_separator("STEP 6: Database Statistics")

    total = manager.count_licenses()
    osi_approved = manager.get_osi_approved_licenses()
    checked = manager.get_checked_licenses()
    unchecked = manager.get_unchecked_licenses()

    print(f"  Total Licenses:        {total}")
    print(f"  OSI Approved:          {len(osi_approved)}")
    print(f"  Checked/Reviewed:      {len(checked)}")
    print(f"  Pending Review:        {len(unchecked)}")

    # ========================================================================
    # OPTIONAL: Delete the license (commented out by default)
    # ========================================================================
    print_separator("OPTIONAL: License Deletion")
    print("[INFO] License deletion is available but commented out in this demo")
    print("[INFO] To delete a license, uncomment the following code:")
    print(f"[INFO]   manager.delete_license('{license_id}', '<current_rev>')")

    # Uncomment to actually delete:
    # current_license = manager.get_license(license_id)
    # delete_result = manager.delete_license(license_id, current_license['_rev'])
    # if delete_result and delete_result.get('ok'):
    #     print("[OK] License deleted successfully!")

    print_separator("Demo Completed Successfully!")
    print("\n[SUMMARY] You've learned how to:")
    print("  1. Connect to CouchDB")
    print("  2. Check if a license exists")
    print("  3. Create a new license")
    print("  4. Retrieve license details")
    print("  5. Search for licenses")
    print("  6. Update license metadata")
    print("  7. View database statistics")
    print("\nNext steps:")
    print("  - Run: python 02_bulk_import.py")
    print("  - Run: python 03_review_workflow.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
