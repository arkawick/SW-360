#!/usr/bin/env python3
"""
Quick Examples for SW360 License Manager
Run this file to see common operations
"""

from sw360_license_manager import SW360LicenseManager, print_license

def main():
    # Initialize the manager
    print("Initializing SW360 License Manager...")
    manager = SW360LicenseManager()
    print()

    # Example 1: List all licenses
    print("=" * 60)
    print("EXAMPLE 1: List All Licenses")
    print("=" * 60)
    licenses = manager.list_licenses()
    print(f"Total licenses in database: {len(licenses)}\n")

    for license in licenses:
        print(f"  {license['shortName']:15} - {license['fullName']}")
    print()

    # Example 2: Get details of a specific license
    print("=" * 60)
    print("EXAMPLE 2: Get MIT License Details")
    print("=" * 60)
    mit_licenses = manager.find_by_short_name("MIT")
    if mit_licenses:
        print_license(mit_licenses[0], detailed=True)
    else:
        print("MIT license not found\n")

    # Example 3: Create a new license
    print("=" * 60)
    print("EXAMPLE 3: Create a New License (GPL-3.0)")
    print("=" * 60)

    # Check if GPL-3.0 already exists
    existing = manager.find_by_short_name("GPL-3.0")

    if existing:
        print("GPL-3.0 already exists in database")
        print(f"  ID: {existing[0]['_id']}")
        print(f"  Revision: {existing[0]['_rev']}\n")
    else:
        try:
            result = manager.create_license(
                full_name="GNU General Public License v3.0",
                short_name="GPL-3.0",
                text="This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.",
                osi_approved=True,
                checked=False
            )
            print("[OK] Created GPL-3.0 license")
            print(f"  ID: {result['id']}")
            print(f"  Revision: {result['rev']}\n")
        except Exception as e:
            print(f"[ERROR] Failed to create license: {e}\n")

    # Example 4: Search and statistics
    print("=" * 60)
    print("EXAMPLE 4: License Statistics")
    print("=" * 60)

    total = manager.count_licenses()
    osi_approved = len(manager.get_osi_approved_licenses())
    checked = len(manager.get_checked_licenses())
    unchecked = len(manager.get_unchecked_licenses())

    print(f"Total licenses:       {total}")
    print(f"OSI approved:         {osi_approved}")
    print(f"Reviewed (checked):   {checked}")
    print(f"Pending review:       {unchecked}\n")

    # Example 5: List licenses pending review
    print("=" * 60)
    print("EXAMPLE 5: Licenses Pending Review")
    print("=" * 60)

    unchecked_licenses = manager.get_unchecked_licenses()
    if unchecked_licenses:
        print(f"Found {len(unchecked_licenses)} license(s) pending review:\n")
        for license in unchecked_licenses:
            print(f"  [ ] {license['shortName']:15} - {license['fullName']}")
    else:
        print("All licenses have been reviewed!")
    print()

    # Example 6: Update a license (mark as checked)
    print("=" * 60)
    print("EXAMPLE 6: Mark a License as Reviewed")
    print("=" * 60)

    if unchecked_licenses:
        # Get the first unchecked license
        license_to_update = unchecked_licenses[0]

        print(f"Marking '{license_to_update['shortName']}' as reviewed...")

        try:
            result = manager.update_license(
                license_id=license_to_update['_id'],
                rev=license_to_update['_rev'],
                full_name=license_to_update['fullName'],
                short_name=license_to_update['shortName'],
                text=license_to_update.get('text', ''),
                osi_approved=license_to_update.get('OSIApproved', False),
                checked=True  # Mark as checked
            )
            print(f"[OK] License updated successfully")
            print(f"  New revision: {result['rev']}\n")
        except Exception as e:
            print(f"[ERROR] Failed to update: {e}\n")
    else:
        print("No unchecked licenses to update\n")

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTo learn more, check PYTHON-USAGE-GUIDE.md")
    print("or read the docstrings in sw360_license_manager.py")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
