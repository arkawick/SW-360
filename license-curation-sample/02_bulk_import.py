#!/usr/bin/env python3
"""
License Curation Sample - Bulk Import

This script demonstrates bulk importing licenses from a JSON file.
Use this when you need to:
- Import multiple licenses at once
- Migrate licenses from another system
- Set up initial license database

Usage:
    python 02_bulk_import.py [path_to_json_file]

Default: Uses sample_licenses.json in the same directory
"""

import sys
import os
import json

# Add parent directory to path to import sw360_license_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sw360_license_manager import SW360LicenseManager


def print_separator(title=""):
    """Print a visual separator"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print("-" * 70)


def load_licenses_from_json(file_path):
    """Load license data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
        return None


def main():
    print_separator("License Curation - Bulk Import Demo")

    # Determine JSON file path
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = os.path.join(os.path.dirname(__file__), "sample_licenses.json")

    print(f"[INFO] Loading licenses from: {json_file}")

    # Load license data
    licenses_data = load_licenses_from_json(json_file)
    if licenses_data is None:
        return 1

    print(f"[OK] Loaded {len(licenses_data)} license(s) from file\n")

    # Initialize the license manager
    print("[*] Initializing SW360 License Manager...")
    manager = SW360LicenseManager()

    # Test connection
    if not manager.test_connection():
        print("[ERROR] Could not connect to CouchDB")
        return 1

    print("[OK] Connected to CouchDB successfully!\n")

    # ========================================================================
    # Import statistics
    # ========================================================================
    stats = {
        'total': len(licenses_data),
        'created': 0,
        'skipped': 0,
        'failed': 0
    }

    print_separator("Starting Bulk Import")

    # ========================================================================
    # Process each license
    # ========================================================================
    for idx, license_data in enumerate(licenses_data, 1):
        short_name = license_data.get('short_name', 'Unknown')
        full_name = license_data.get('full_name', 'Unknown')

        print(f"[{idx}/{len(licenses_data)}] Processing: {short_name}")

        # Check if license already exists
        existing = manager.find_by_short_name(short_name)

        if existing:
            print(f"  [SKIP] License '{short_name}' already exists (ID: {existing[0]['_id']})")
            stats['skipped'] += 1
            continue

        # Create the license
        try:
            result = manager.create_license(
                full_name=license_data.get('full_name', ''),
                short_name=license_data.get('short_name', ''),
                text=license_data.get('text', ''),
                osi_approved=license_data.get('osi_approved', False),
                checked=license_data.get('checked', False)
            )

            if result and result.get('ok'):
                print(f"  [OK] Created successfully (ID: {result.get('id')})")
                stats['created'] += 1
            else:
                print(f"  [ERROR] Failed to create license")
                stats['failed'] += 1

        except Exception as e:
            print(f"  [ERROR] Exception occurred: {str(e)}")
            stats['failed'] += 1

        print()  # Empty line for readability

    # ========================================================================
    # Display import summary
    # ========================================================================
    print_separator("Import Summary")

    print(f"  Total Processed:  {stats['total']}")
    print(f"  Created:          {stats['created']}")
    print(f"  Skipped:          {stats['skipped']} (already exist)")
    print(f"  Failed:           {stats['failed']}")

    if stats['failed'] > 0:
        print(f"\n  [WARNING] {stats['failed']} license(s) failed to import")

    # ========================================================================
    # Show current database state
    # ========================================================================
    print_separator("Current Database State")

    total = manager.count_licenses()
    osi_approved = manager.get_osi_approved_licenses()
    checked = manager.get_checked_licenses()
    unchecked = manager.get_unchecked_licenses()

    print(f"  Total Licenses:       {total}")
    print(f"  OSI Approved:         {len(osi_approved)}")
    print(f"  Checked/Reviewed:     {len(checked)}")
    print(f"  Pending Review:       {len(unchecked)}")

    # ========================================================================
    # List all license short names
    # ========================================================================
    print_separator("All Licenses in Database")

    all_licenses = manager.list_licenses()
    print(f"  Found {len(all_licenses)} license(s):\n")

    for idx, lic in enumerate(sorted(all_licenses, key=lambda x: x.get('shortName', '')), 1):
        short_name = lic.get('shortName', 'N/A')
        full_name = lic.get('fullName', 'N/A')
        checked_mark = '[X]' if lic.get('checked') else '[ ]'
        osi_mark = '[OSI]' if lic.get('OSIApproved') else '     '

        print(f"  {idx:2d}. {checked_mark} {osi_mark} {short_name:20s} - {full_name[:40]}")

    print_separator("Bulk Import Completed!")

    print("\n[NEXT STEPS]")
    print("  - Review unchecked licenses: python 03_review_workflow.py")
    print("  - View in web UI: http://localhost:5984/_utils/#database/sw360db/_all_docs")
    print("  - Query via Python: from sw360_license_manager import SW360LicenseManager")

    return 0


if __name__ == "__main__":
    sys.exit(main())
