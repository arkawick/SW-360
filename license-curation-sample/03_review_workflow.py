#!/usr/bin/env python3
"""
License Curation Sample - Review Workflow

This script demonstrates a license review workflow where you:
1. View all unchecked licenses
2. Display license details for review
3. Mark licenses as checked after review
4. Track review progress

This simulates a real-world license curation process where
licenses need to be reviewed and approved before use.

Usage:
    python 03_review_workflow.py [--auto-approve]

Options:
    --auto-approve    Automatically approve all unchecked licenses (demo mode)
"""

import sys
import os
import time

# Add parent directory to path to import sw360_license_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sw360_license_manager import SW360LicenseManager


def print_separator(title="", char="="):
    """Print a visual separator"""
    if title:
        print(f"\n{char*70}")
        print(f"  {title}")
        print(f"{char*70}\n")
    else:
        print(char * 70)


def display_license_for_review(license_data, index, total):
    """Display license details in a review-friendly format"""
    print_separator(f"License {index} of {total}", "-")

    print(f"  Short Name:    {license_data.get('shortName', 'N/A')}")
    print(f"  Full Name:     {license_data.get('fullName', 'N/A')}")
    print(f"  OSI Approved:  {license_data.get('OSIApproved', False)}")
    print(f"  Checked:       {license_data.get('checked', False)}")
    print(f"\n  License Text:")
    print(f"  {'-'*66}")

    # Display license text with proper wrapping
    text = license_data.get('text', 'No text available')
    lines = text.split('\n')
    for line in lines[:15]:  # Show first 15 lines
        print(f"  {line[:66]}")

    if len(lines) > 15:
        print(f"  ... ({len(lines) - 15} more lines)")

    print(f"  {'-'*66}")
    print(f"\n  Document ID:   {license_data.get('_id', 'N/A')}")
    print(f"  Revision:      {license_data.get('_rev', 'N/A')}")


def review_license_interactive(manager, license_data, index, total):
    """Interactively review a license"""
    display_license_for_review(license_data, index, total)

    while True:
        print("\n  Review Options:")
        print("    [A] Approve (mark as checked)")
        print("    [S] Skip (review later)")
        print("    [Q] Quit review process")

        choice = input("\n  Your choice: ").strip().upper()

        if choice == 'A':
            # Approve the license
            result = manager.update_license(
                license_id=license_data['_id'],
                rev=license_data['_rev'],
                full_name=license_data['fullName'],
                short_name=license_data['shortName'],
                text=license_data['text'],
                osi_approved=license_data['OSIApproved'],
                checked=True
            )

            if result and result.get('ok'):
                print(f"\n  [OK] License '{license_data['shortName']}' approved!")
                return 'approved'
            else:
                print(f"\n  [ERROR] Failed to approve license")
                return 'error'

        elif choice == 'S':
            print(f"\n  [SKIP] License '{license_data['shortName']}' skipped")
            return 'skipped'

        elif choice == 'Q':
            print("\n  [QUIT] Exiting review process...")
            return 'quit'

        else:
            print("  [ERROR] Invalid choice. Please enter A, S, or Q.")


def auto_approve_license(manager, license_data):
    """Automatically approve a license (for demo purposes)"""
    result = manager.update_license(
        license_id=license_data['_id'],
        rev=license_data['_rev'],
        full_name=license_data['fullName'],
        short_name=license_data['shortName'],
        text=license_data['text'],
        osi_approved=license_data['OSIApproved'],
        checked=True
    )

    return result and result.get('ok')


def main():
    print_separator("License Curation - Review Workflow")

    # Check for auto-approve mode
    auto_approve = '--auto-approve' in sys.argv

    if auto_approve:
        print("[INFO] Running in AUTO-APPROVE mode (demo)")
        print("[INFO] All unchecked licenses will be automatically approved\n")

    # Initialize the license manager
    print("[*] Initializing SW360 License Manager...")
    manager = SW360LicenseManager()

    # Test connection
    if not manager.test_connection():
        print("[ERROR] Could not connect to CouchDB")
        return 1

    print("[OK] Connected to CouchDB successfully!\n")

    # ========================================================================
    # Get unchecked licenses
    # ========================================================================
    print_separator("Finding Unchecked Licenses")

    unchecked_licenses = manager.get_unchecked_licenses()

    if not unchecked_licenses:
        print("[INFO] No unchecked licenses found!")
        print("[INFO] All licenses have been reviewed.\n")

        # Show statistics
        total = manager.count_licenses()
        checked = manager.get_checked_licenses()
        print(f"  Total Licenses:    {total}")
        print(f"  Checked:           {len(checked)}")

        print("\n[SUCCESS] License review process is complete!")
        return 0

    print(f"[OK] Found {len(unchecked_licenses)} unchecked license(s) pending review\n")

    # ========================================================================
    # Review each license
    # ========================================================================
    stats = {
        'total': len(unchecked_licenses),
        'approved': 0,
        'skipped': 0,
        'errors': 0
    }

    for idx, license_data in enumerate(unchecked_licenses, 1):
        if auto_approve:
            # Auto-approve mode
            display_license_for_review(license_data, idx, len(unchecked_licenses))
            print(f"\n  [AUTO] Approving license: {license_data['shortName']}...")

            if auto_approve_license(manager, license_data):
                print(f"  [OK] Approved successfully!")
                stats['approved'] += 1
            else:
                print(f"  [ERROR] Failed to approve")
                stats['errors'] += 1

            time.sleep(0.5)  # Small delay for readability

        else:
            # Interactive mode
            result = review_license_interactive(manager, license_data, idx, len(unchecked_licenses))

            if result == 'approved':
                stats['approved'] += 1
            elif result == 'skipped':
                stats['skipped'] += 1
            elif result == 'error':
                stats['errors'] += 1
            elif result == 'quit':
                print("\n[INFO] Review process terminated by user")
                stats['skipped'] = len(unchecked_licenses) - stats['approved'] - stats['errors']
                break

    # ========================================================================
    # Display review summary
    # ========================================================================
    print_separator("Review Summary")

    print(f"  Total Reviewed:   {stats['total']}")
    print(f"  Approved:         {stats['approved']}")
    print(f"  Skipped:          {stats['skipped']}")
    print(f"  Errors:           {stats['errors']}")

    # ========================================================================
    # Show updated database state
    # ========================================================================
    print_separator("Updated Database State")

    total = manager.count_licenses()
    osi_approved = manager.get_osi_approved_licenses()
    checked = manager.get_checked_licenses()
    unchecked = manager.get_unchecked_licenses()

    print(f"  Total Licenses:       {total}")
    print(f"  OSI Approved:         {len(osi_approved)}")
    print(f"  Checked/Reviewed:     {len(checked)}")
    print(f"  Pending Review:       {len(unchecked)}")

    completion_rate = (len(checked) / total * 100) if total > 0 else 0
    print(f"\n  Review Progress:      {completion_rate:.1f}% complete")

    # ========================================================================
    # Show completion status
    # ========================================================================
    print_separator("Review Workflow Completed!")

    if len(unchecked) == 0:
        print("[SUCCESS] All licenses have been reviewed!")
    else:
        print(f"[INFO] {len(unchecked)} license(s) still pending review")
        print("[INFO] Run this script again to continue the review process")

    print("\n[NEXT STEPS]")
    print("  - View checked licenses: python 04_generate_report.py")
    print("  - Access web UI: http://localhost:5984/_utils/#database/sw360db/_all_docs")
    print("  - View license details in Python:")
    print("      from sw360_license_manager import SW360LicenseManager")
    print("      manager = SW360LicenseManager()")
    print("      license = manager.find_by_short_name('MIT')[0]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
