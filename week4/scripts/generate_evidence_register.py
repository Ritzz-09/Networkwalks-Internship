#!/usr/bin/env python3
"""
Generates Evidence_Register.xlsx with professional styling using openpyxl.
Contains:
1. Screenshot & Image Evidence Register
2. Digital Forensic Artifacts Register
3. Vulnerability Findings & Evidence Cross-Reference
"""

import os
import hashlib
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_PATH = os.path.join(BASE_DIR, "M4_Report", "Evidence_Register.xlsx")

def get_file_sha256(filepath):
    if not os.path.exists(filepath):
        return "N/A"
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def build_workbook():
    wb = openpyxl.Workbook()
    # Sheet 1: Screenshot Register
    ws1 = wb.active
    ws1.title = "Screenshot_Register"
    
    # Styles
    navy_header = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    alt_row_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=10, bold=True)
    regular_font = Font(name="Calibri", size=10)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )
    
    headers1 = [
        "Evidence ID", "Milestone", "Filename", "Original Path", 
        "Report Asset Path", "Description", "Associated Finding", "Verification Status"
    ]
    ws1.append(headers1)
    for col_num in range(1, len(headers1) + 1):
        cell = ws1.cell(row=1, column=col_num)
        cell.fill = navy_header
        cell.font = header_font
        cell.alignment = center_align

    evidence_data = [
        ("RECON-01", "Reconnaissance", "N/A (CLI Dig log)", "Recon/dns.txt", "N/A", "DNS A-record query resolving medirozahospital.com to 199.188.201.16", "Informational", "[SCREENSHOT REQUIRED - CLI DNS Output]"),
        ("RECON-02", "Reconnaissance", "N/A (CLI Nmap log)", "Recon/nmap.txt", "N/A", "Nmap v7.991 scan identifying open ports 80/443 and HAProxy 2.0.0+", "Informational", "[SCREENSHOT REQUIRED - CLI Nmap Output]"),
        ("RECON-03", "Reconnaissance", "N/A (CLI WhatWeb log)", "Recon/whatweb.txt", "N/A", "WhatWeb technology fingerprinting LiteSpeed web server and 403 Forbidden probe", "Informational", "[SCREENSHOT REQUIRED - CLI WhatWeb Output]"),
        ("RECON-04", "Reconnaissance", "N/A (CLI cURL log)", "Recon/headers.txt", "N/A", "cURL HTTP/2 response headers inspection revealing LiteSpeed server header", "Informational", "[SCREENSHOT REQUIRED - CLI cURL Header Output]"),
        ("M1-01", "M1 - Initial Access", "login bypass.png", "M1/login bypass.png", "M4_Report/images/M1-01_login_bypass.png", "Web login interface showing SQL Injection authentication bypass entry (admin' -- ) at /patient/login.php", "F-01", "Verified Present (Embedded)"),
        ("M1-02", "M1 - Initial Access", "proof of bypass.png", "M1/proof of bypass.png", "M4_Report/images/M1-02_proof_of_bypass.png", "Authenticated patient portal session at /patient/portal.php exposing 3 locked patient reports", "F-01", "Verified Present (Embedded)"),
        ("M1-03", "M1 - Initial Access", "patient_report_{1,2,3}.pdf", "M1/patient_report_*.pdf", "N/A", "Local CLI directory listing showing 3 downloaded encrypted patient PDF reports", "F-01", "[SCREENSHOT REQUIRED - Local File Listing]"),
        ("M2-01", "M2 - Data Recovery", "all_reports_metadata.txt", "M2/all_reports_metadata.txt", "N/A", "ExifTool metadata inspection showing author j.malik and /old DB backup leak comment", "F-03", "[SCREENSHOT REQUIRED - ExifTool CLI Output]"),
        ("M2-02", "M2 - Data Recovery", "password cracking.png", "Screenshots/password cracking.png", "M4_Report/images/M2-02_password_cracking.png", "John the Ripper dictionary attack on PDF hashes using rockyou.txt (passwords redacted)", "F-02", "Verified Present (Embedded & Redacted)"),
        ("M2-03", "M2 - Data Recovery", "patient1.png", "Screenshots/patient1.png", "M4_Report/images/M2-03_patient1.png", "Decrypted pathology report for Sipho Dlamini (LR-2024-1187, Full Blood Count) in viewer", "F-01, F-02", "Verified Present (Embedded & Redacted)"),
        ("M2-04", "M2 - Data Recovery", "patient2.png", "Screenshots/patient2.png", "M4_Report/images/M2-04_patient2.png", "Decrypted pathology report for Priya Reddy (LR-2024-1192, Lipid Profile) in viewer", "F-01, F-02", "Verified Present (Embedded & Redacted)"),
        ("M2-05", "M2 - Data Recovery", "patient3.png", "Screenshots/patient3.png", "M4_Report/images/M2-05_patient3.png", "Decrypted pathology report for Emily Thompson (LR-2024-1205, FBC & Ferritin) in viewer", "F-01, F-02", "Verified Present (Embedded & Redacted)"),
        ("M3-01", "M3 - Data Exposure", "exposed db.png", "Screenshots/exposed db.png", "M4_Report/images/M3-01_exposed_db.png", "Direct web browser HTTP access to publicly exposed SQL backup at /old/mediroza_db_backup_2019.sql", "F-03, F-04", "Verified Present (Embedded & Redacted)"),
        ("M3-02", "M3 - Data Exposure", "backup_hash.txt", "M3/backup_hash.txt", "N/A", "Cryptographic SHA-256 hash verification of downloaded database dump", "F-03", "[SCREENSHOT REQUIRED - CLI SHA256 Output]"),
        ("M3-03", "M3 - Data Exposure", "employee_salary_details.txt", "M3/employee_salary_details.txt", "N/A", "Local database import and staff salary aggregation query results", "F-04", "[SCREENSHOT REQUIRED - SQL Salary Query Output]"),
        ("M3-04", "M3 - Data Exposure", "shareholder_details.txt", "M3/shareholder_details.txt", "N/A", "Local database shareholder distribution and equity ownership query results", "F-04", "[SCREENSHOT REQUIRED - SQL Shareholder Query Output]")
    ]

    for row_idx, row_data in enumerate(evidence_data, start=2):
        ws1.append(row_data)
        fill = alt_row_fill if row_idx % 2 == 0 else PatternFill(fill_type=None)
        for col_idx in range(1, len(row_data) + 1):
            cell = ws1.cell(row=row_idx, column=col_idx)
            cell.font = regular_font
            cell.border = thin_border
            if fill.fill_type: cell.fill = fill
            if col_idx in (1, 2, 7, 8):
                cell.alignment = center_align
            else:
                cell.alignment = left_align
            # Highlight status
            if "Verified Present" in str(row_data[7]):
                cell.font = Font(name="Calibri", size=10, color="22543D", bold=True)
            elif "REQUIRED" in str(row_data[7]):
                cell.font = Font(name="Calibri", size=10, color="742A2A", italic=True)

    # Sheet 2: Artifacts Register
    ws2 = wb.create_sheet(title="Forensic_Artifacts")
    headers2 = ["Artifact Name", "Milestone", "Relative Path", "File Type", "Size (Bytes)", "SHA-256 Hash", "Description & Significance"]
    ws2.append(headers2)
    for col_num in range(1, len(headers2) + 1):
        cell = ws2.cell(row=1, column=col_num)
        cell.fill = navy_header
        cell.font = header_font
        cell.alignment = center_align

    artifacts_data = [
        ("patient_report_1.pdf", "M1", "M1/patient_report_1.pdf", "PDF (Encrypted)", "2846", "3a520268153406f97ef9ff35b9183ecdfbb21b0e9db1951950d992f8ce6b0a68", "Exfiltrated locked pathology report (Sipho Dlamini)"),
        ("patient_report_2.pdf", "M1", "M1/patient_report_2.pdf", "PDF (Encrypted)", "2848", "9df4a32332c916422d32cfb5faae4e84b8f5ea0e7041496eaeb3ad3c29ee2d65", "Exfiltrated locked pathology report (Priya Reddy)"),
        ("patient_report_3.pdf", "M1", "M1/patient_report_3.pdf", "PDF (Encrypted)", "2881", "87556f874bc05658e434f0c4d293cfd81b4f455122e23d706eb86a9d9e48f76d", "Exfiltrated locked pathology report (Emily Thompson)"),
        ("hash.txt", "M2", "M2/hash.txt", "Text / Hash", "690", "e73f4439c299c0cf04975549887713f044237eb5f08518e3845b4125b292e92c", "Extracted pdf2john hashes ($pdf$2*3*128*...) for reports 1, 2, and 3"),
        ("recovered passwords.txt", "M2", "M2/recovered passwords.txt", "Text", "42", "6459341c2c31758e5f22e8ec530188ef7e7bbfdd0d05bf0f498c39e2469a473b", "Recovered PDF user passwords (stored securely, not published)"),
        ("patient_report_1_unlocked.pdf", "M2", "M2/patient_report_1_unlocked.pdf", "PDF (Decrypted)", "2827", "4b0b1341c2333cfc2d3ca65fc5333f2cf19e99277f09fbb34f664c3c3a992ff4", "Decrypted PDF report confirming successful credential recovery"),
        ("patient_report_2_unlocked.pdf", "M2", "M2/patient_report_2_unlocked.pdf", "PDF (Decrypted)", "2829", "a78d8a571a3e62f0254c46f3454792613d9412111feeb9b68ad93b2a091e92d6", "Decrypted PDF report confirming successful credential recovery"),
        ("patient_report_3_unlocked.pdf", "M2", "M2/patient_report_3_unlocked.pdf", "PDF (Decrypted)", "2862", "4cb60f64c6dc9da7b0037a54a7cb45dcf85b2e38c92a95c9629b35b6c2c39e08", "Decrypted PDF report confirming successful credential recovery"),
        ("all_reports_metadata.txt", "M2", "M2/all_reports_metadata.txt", "Text", "3420", "78b776269df738b556b20641aaec5658933b868e7ec89f257127bcfb9265f24f", "ExifTool metadata extraction revealing DB backup path comment by j.malik"),
        ("mediroza_db_backup_2019.sql", "M3", "M3/mediroza_db_backup_2019.sql", "SQL Dump", "6346", "15d8b49ae104b073d5b0a7289189bdc3940bbab96168e9bdac882ac59feed257", "Exfiltrated MySQL backup containing staff and shareholders tables"),
        ("backup_hash.txt", "M3", "M3/backup_hash.txt", "Text", "94", "501a350eb9385ef222f7b8893d5be4f2fe5dbd0aaee338787f73c683b5849880", "SHA-256 verification hash of mediroza_db_backup_2019.sql"),
        ("backup_file_info.txt", "M3", "M3/backup_file_info.txt", "Text", "393", "2c4aa029f60cb7132e49c7161b9a9fb9be54c5520e53a992e1ce3f898a4d4681", "Stat file metadata for downloaded SQL backup archive"),
        ("employee_salary_details.txt", "M3", "M3/employee_salary_details.txt", "Text", "1984", "997b6a15db3b977759a29633e6fba0a9f5d17c76891142f1f6d35bf9b6b907c1", "Extracted employee salary table (30 employees, monthly ZAR)"),
        ("department_salary_analysis.txt", "M3", "M3/department_salary_analysis.txt", "Text", "813", "da00cf2dca58c148c3ae55ccebb161109a96e2a229fc8c03e67c823021f144ec", "Departmental payroll aggregation across 17 hospital departments"),
        ("salary_statistics.txt", "M3", "M3/salary_statistics.txt", "Text", "148", "67049cf1a774972ff27541fc11054b41fb45a499318b7654ec7796d11f6c449c", "High-level salary summary (Total, Min, Max, Average monthly/annual)"),
        ("shareholder_details.txt", "M3", "M3/shareholder_details.txt", "Text", "476", "e3d097c27181f7d45a753a81a1795ee8cba8bf50428d011505cbe046dc54e601", "Full equity cap table (10 shareholders, share percentages, share count)"),
        ("shareholder_distribution.txt", "M3", "M3/shareholder_distribution.txt", "Text", "116", "f96d07d1a5525ce08c356e7aaae1316b1e5502c11438914b4335e39eb143715c", "Share class equity distribution (Ordinary vs Preferential)"),
        ("shareholder_statistics.txt", "M3", "M3/shareholder_statistics.txt", "Text", "77", "b8c3858f7a9ea15291410fa88047913cf0d216fe8d3615ea89b9148d2b904d96", "Shareholder total equity and share count verification")
    ]

    for row_idx, row_data in enumerate(artifacts_data, start=2):
        ws2.append(row_data)
        fill = alt_row_fill if row_idx % 2 == 0 else PatternFill(fill_type=None)
        for col_idx in range(1, len(row_data) + 1):
            cell = ws2.cell(row=row_idx, column=col_idx)
            cell.font = regular_font
            cell.border = thin_border
            if fill.fill_type: cell.fill = fill
            if col_idx in (2, 4, 5):
                cell.alignment = center_align
            elif col_idx == 6:
                cell.font = Font(name="Consolas", size=9)
                cell.alignment = left_align
            else:
                cell.alignment = left_align

    # Sheet 3: Vulnerability Findings Map
    ws3 = wb.create_sheet(title="Vulnerability_Findings")
    headers3 = ["Finding ID", "Title", "Severity", "CVSS v3.1", "CWE / OWASP", "Affected Asset", "Primary Impact", "Associated Evidence"]
    ws3.append(headers3)
    for col_num in range(1, len(headers3) + 1):
        cell = ws3.cell(row=1, column=col_num)
        cell.fill = navy_header
        cell.font = header_font
        cell.alignment = center_align

    findings_data = [
        ("F-01", "Unauthorized Access to Confidential Patient Reports", "Critical", "9.1 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)", "CWE-89 / OWASP A03:2021-Injection", "https://medirozahospital.com/patient/login.php", "Complete compromise of patient portal authentication, exfiltration of medical lab reports", "M1-01, M1-02, M1-03, M2-03, M2-04, M2-05"),
        ("F-02", "Weak Password Protection on Confidential PDF Documents", "High", "7.5 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)", "CWE-521 / OWASP A02:2021-Cryptographic Failures", "Patient Pathology Reports (CMS Lab Module)", "Immediate brute-force recovery of medical laboratory test results using common wordlists", "M2-02, M2-03, M2-04, M2-05"),
        ("F-03", "Publicly Accessible SQL Database Backup in Web Root", "Critical", "9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)", "CWE-552 / OWASP A05:2021-Security Misconfiguration", "https://medirozahospital.com/old/mediroza_db_backup_2019.sql", "Unauthenticated public downloading of full internal hospital MySQL database dump", "M2-01, M3-01, M3-02"),
        ("F-04", "Exposure of Employee Salary and Shareholder Information", "High", "7.5 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)", "CWE-200 / OWASP A01:2021-Broken Access Control", "mediroza_hr Database Schema (staff & shareholders tables)", "Breach of POPIA Act 4 of 2013, leak of National IDs, payroll (ZAR 2M/mo), and equity cap table", "M3-01, M3-03, M3-04")
    ]

    for row_idx, row_data in enumerate(findings_data, start=2):
        ws3.append(row_data)
        fill = alt_row_fill if row_idx % 2 == 0 else PatternFill(fill_type=None)
        for col_idx in range(1, len(row_data) + 1):
            cell = ws3.cell(row=row_idx, column=col_idx)
            cell.font = regular_font
            cell.border = thin_border
            if fill.fill_type: cell.fill = fill
            if col_idx in (1, 3):
                cell.alignment = center_align
                if row_data[2] == "Critical":
                    cell.font = Font(name="Calibri", size=10, color="9B2C2C", bold=True)
                elif row_data[2] == "High":
                    cell.font = Font(name="Calibri", size=10, color="DD6B20", bold=True)
            else:
                cell.alignment = left_align

    # Auto-adjust column widths across all sheets
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    wb.save(OUT_PATH)
    print(f"Evidence Register saved successfully to {OUT_PATH}")

if __name__ == "__main__":
    build_workbook()
