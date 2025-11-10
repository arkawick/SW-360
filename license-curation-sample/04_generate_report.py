#!/usr/bin/env python3
"""
License Curation Sample - Generate Report

This script generates reports about licenses in the database:
1. Summary statistics
2. License lists (all, OSI-approved, checked, etc.)
3. Export to JSON/CSV formats

Usage:
    python 04_generate_report.py [--format json|csv|text]
"""

import sys
import os
import json
from datetime import datetime

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


def generate_text_report(manager):
    """Generate a text-based report"""
    print_separator("SW360 License Curation Report")

    # Report metadata
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  Generated: {now}")
    print(f"  Database:  sw360db")
    print(f"  Source:    http://localhost:5984\n")

    # ========================================================================
    # Summary Statistics
    # ========================================================================
    print_separator("Summary Statistics", "-")

    total = manager.count_licenses()
    osi_approved_licenses = manager.get_osi_approved_licenses()
    checked_licenses = manager.get_checked_licenses()
    unchecked_licenses = manager.get_unchecked_licenses()

    print(f"  Total Licenses:           {total}")
    print(f"  OSI Approved:             {len(osi_approved_licenses)}")
    print(f"  Checked/Reviewed:         {len(checked_licenses)}")
    print(f"  Pending Review:           {len(unchecked_licenses)}")

    if total > 0:
        osi_percent = (len(osi_approved_licenses) / total * 100)
        checked_percent = (len(checked_licenses) / total * 100)

        print(f"\n  OSI Approval Rate:        {osi_percent:.1f}%")
        print(f"  Review Completion Rate:   {checked_percent:.1f}%")

    # ========================================================================
    # All Licenses List
    # ========================================================================
    print_separator("All Licenses", "-")

    all_licenses = manager.list_licenses()
    sorted_licenses = sorted(all_licenses, key=lambda x: x.get('shortName', ''))

    print(f"  Total: {len(sorted_licenses)} license(s)\n")

    print(f"  {'#':<4} {'Short Name':<20} {'Full Name':<30} {'OSI':<5} {'Checked':<8}")
    print(f"  {'-'*4} {'-'*20} {'-'*30} {'-'*5} {'-'*8}")

    for idx, lic in enumerate(sorted_licenses, 1):
        short_name = lic.get('shortName', 'N/A')[:20]
        full_name = lic.get('fullName', 'N/A')[:30]
        osi = 'Yes' if lic.get('OSIApproved') else 'No'
        checked = 'Yes' if lic.get('checked') else 'No'

        print(f"  {idx:<4} {short_name:<20} {full_name:<30} {osi:<5} {checked:<8}")

    # ========================================================================
    # OSI Approved Licenses
    # ========================================================================
    print_separator("OSI Approved Licenses", "-")

    print(f"  Total: {len(osi_approved_licenses)} license(s)\n")

    for idx, lic in enumerate(sorted(osi_approved_licenses, key=lambda x: x.get('shortName', '')), 1):
        short_name = lic.get('shortName', 'N/A')
        full_name = lic.get('fullName', 'N/A')[:40]
        checked_mark = '[X]' if lic.get('checked') else '[ ]'

        print(f"  {idx:2d}. {checked_mark} {short_name:<20} - {full_name}")

    # ========================================================================
    # Unchecked Licenses (Pending Review)
    # ========================================================================
    print_separator("Pending Review", "-")

    if unchecked_licenses:
        print(f"  Total: {len(unchecked_licenses)} license(s) pending review\n")

        for idx, lic in enumerate(sorted(unchecked_licenses, key=lambda x: x.get('shortName', '')), 1):
            short_name = lic.get('shortName', 'N/A')
            full_name = lic.get('fullName', 'N/A')[:40]
            osi_mark = '[OSI]' if lic.get('OSIApproved') else '     '

            print(f"  {idx:2d}. {osi_mark} {short_name:<20} - {full_name}")

        print("\n  [ACTION REQUIRED] Run: python 03_review_workflow.py")
    else:
        print("  [OK] No licenses pending review!")

    # ========================================================================
    # Checked Licenses
    # ========================================================================
    print_separator("Checked/Reviewed Licenses", "-")

    print(f"  Total: {len(checked_licenses)} license(s) reviewed and approved\n")

    for idx, lic in enumerate(sorted(checked_licenses, key=lambda x: x.get('shortName', '')), 1):
        short_name = lic.get('shortName', 'N/A')
        full_name = lic.get('fullName', 'N/A')[:40]
        osi_mark = '[OSI]' if lic.get('OSIApproved') else '     '

        print(f"  {idx:2d}. {osi_mark} {short_name:<20} - {full_name}")

    print_separator("End of Report")


def export_to_json(manager, output_file="license_report.json"):
    """Export all licenses to JSON"""
    all_licenses = manager.list_licenses()

    # Prepare data for export
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_licenses": len(all_licenses),
        "licenses": []
    }

    for lic in sorted(all_licenses, key=lambda x: x.get('shortName', '')):
        export_data["licenses"].append({
            "id": lic.get('_id'),
            "short_name": lic.get('shortName'),
            "full_name": lic.get('fullName'),
            "osi_approved": lic.get('OSIApproved', False),
            "checked": lic.get('checked', False),
            "text": lic.get('text', '')
        })

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Report exported to: {output_file}")
    print(f"[OK] {len(all_licenses)} license(s) exported")


def export_to_csv(manager, output_file="license_report.csv"):
    """Export all licenses to CSV"""
    all_licenses = manager.list_licenses()

    # Write CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        # CSV header
        f.write("Short Name,Full Name,OSI Approved,Checked,Document ID\n")

        # CSV rows
        for lic in sorted(all_licenses, key=lambda x: x.get('shortName', '')):
            short_name = lic.get('shortName', 'N/A').replace(',', ';')
            full_name = lic.get('fullName', 'N/A').replace(',', ';')
            osi = 'Yes' if lic.get('OSIApproved') else 'No'
            checked = 'Yes' if lic.get('checked') else 'No'
            doc_id = lic.get('_id', 'N/A')

            f.write(f"{short_name},{full_name},{osi},{checked},{doc_id}\n")

    print(f"[OK] Report exported to: {output_file}")
    print(f"[OK] {len(all_licenses)} license(s) exported")


def main():
    print_separator("License Curation - Generate Report")

    # Parse command line arguments
    output_format = "text"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--format", "-f"] and len(sys.argv) > 2:
            output_format = sys.argv[2].lower()
        elif sys.argv[1].startswith("--format="):
            output_format = sys.argv[1].split("=")[1].lower()

    # Validate format
    if output_format not in ["text", "json", "csv"]:
        print(f"[ERROR] Invalid format: {output_format}")
        print("[INFO] Valid formats: text, json, csv")
        return 1

    print(f"[INFO] Report format: {output_format}\n")

    # Initialize the license manager
    print("[*] Initializing SW360 License Manager...")
    manager = SW360LicenseManager()

    # Test connection
    if not manager.test_connection():
        print("[ERROR] Could not connect to CouchDB")
        return 1

    print("[OK] Connected to CouchDB successfully!\n")

    # ========================================================================
    # Generate report based on format
    # ========================================================================
    if output_format == "text":
        generate_text_report(manager)

    elif output_format == "json":
        output_file = f"license_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        print_separator("Exporting to JSON")
        export_to_json(manager, output_file)
        print(f"\n[INFO] View file: {output_file}")

    elif output_format == "csv":
        output_file = f"license_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        print_separator("Exporting to CSV")
        export_to_csv(manager, output_file)
        print(f"\n[INFO] View file: {output_file}")
        print(f"[INFO] Open in Excel or any spreadsheet application")

    print("\n[SUCCESS] Report generation completed!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
