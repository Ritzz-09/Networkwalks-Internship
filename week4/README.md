# Mediroza General Hospital – Penetration Testing & Forensic Assessment

[![Target](https://img.shields.io/badge/Target-medirozahospital.com-blue?logo=firefox&logoColor=white)](https://medirozahospital.com)
[![Classification](https://img.shields.io/badge/Classification-CONFIDENTIAL-red)](#01-cover-page)
[![Framework](https://img.shields.io/badge/Engagement-Networkwalks_Week_4-brightgreen)](#engagement-overview)
[![Compliance](https://img.shields.io/badge/Compliance-POPIA_Act_4_of_2013-orange)](#regulatory--legal-compliance-liabilities-popia-act-4-of-2013)

This directory contains the complete technical assessment records, forensic evidence, cryptanalysis scripts, analytical tables, and formal consulting deliverables for the **Mediroza General Hospital Black-Box Penetration Test** completed during **Week 4 (Batch B083)** of the Networkwalks Cybersecurity Internship.

---

## 📋 Table of Contents
- [🎯 Engagement Overview](#-engagement-overview)
- [⚔️ Attack Chain Summary](#️-attack-chain-summary)
- [📂 Directory Architecture](#-directory-architecture)
- [🔍 Milestone Breakdown](#-milestone-breakdown)
  - [Reconnaissance](#-reconnaissance)
  - [M1 – Initial Access](#-m1--initial-access)
  - [M2 – Cryptanalysis & Data Recovery](#-m2--cryptanalysis--data-recovery)
  - [M3 – Critical Data Exposure](#-m3--critical-data-exposure)
  - [M4 – Professional Reporting](#-m4--professional-reporting)
- [📊 Consolidated Vulnerability Register](#-consolidated-vulnerability-register)
- [📄 Deliverable Suite (`M4_Report/`)](#-deliverable-suite-m4_report)
- [👤 Author & Acknowledgments](#-author--acknowledgments)

---

## 🎯 Engagement Overview
* **Target Entity:** Mediroza General Hospital (14 Cedar Avenue, Johannesburg, South Africa)
* **Target Domain:** `https://medirozahospital.com` (Host IP: `199.188.201.16` / `server274-1.web-hosting.com`)
* **Testing Type:** Black-Box Web Application Penetration Test & Digital Forensic Investigation
* **Assessment Framework:** Networkwalks Cybersecurity Internship (Week 4, Batch B083)
* **Lead Security Analyst:** Rithish S P ([@Ritzz-09](https://github.com/Ritzz-09))

---

## ⚔️ Attack Chain Summary

```
[Phase 1: External Reconnaissance]
  ├── DNS Enumeration (dig): 199.188.201.16
  ├── Port Scanning (nmap): Ports 80 & 443 Open (HAProxy Reverse Proxy 2.0.0+)
  └── Technology Fingerprinting (whatweb / curl): LiteSpeed Web Server, HTTP 403 on root
         │
         ▼
[Phase 2: Milestone M1 – Initial Access]
  ├── Target: Patient Authentication Portal (https://medirozahospital.com/patient/login.php)
  ├── Vulnerability: SQL Injection via unparameterized Username input
  ├── Exploit Payload: admin' -- 
  └── Outcome: Bypassed login, accessed dashboard (/patient/portal.php), exfiltrated 3 locked patient reports
         │
         ▼
[Phase 3: Milestone M2 – PDF Cryptanalysis & Forensics]
  ├── Hash Extraction (pdf2john): Extracted $pdf$2*3*128* hashes
  ├── Dictionary Attack (John the Ripper + rockyou.txt): Cracked all 3 passwords in < 1 second
  ├── Decryption: Unlocked 3 pathology reports (Full Blood Count, Lipid Profile, Anaemia markers)
  └── Forensic Metadata (ExifTool): Disclosed comment by IT Admin j.malik:
      "DB backup moved to /old before site migration, do not delete"
         │
         ▼
[Phase 4: Milestone M3 – Critical Data Exposure]
  ├── Target: https://medirozahospital.com/old/mediroza_db_backup_2019.sql
  ├── Exfiltration: Unauthenticated HTTP download of full 6.3 KB MySQL database dump (mediroza_hr)
  ├── Schema: Two relational tables: `staff` (30 employees) and `shareholders` (10 investors)
  └── Intelligence Recovered:
      - 30 Employee South African National IDs, private phone numbers, emails, and monthly salaries
      - Total Monthly Hospital Payroll: ZAR 2,027,000.00 (ZAR 24,324,000.00 annualized)
      - Complete Shareholder Capitalization: 1,000,000 shares (88% Ordinary, 12% Preferential)
         │
         ▼
[Phase 5: Milestone M4 – Professional Penetration Testing Deliverables]
  └── Formatted 21-page PDF Report, editable DOCX Report, Excel Evidence Register, Gap Checklist & Summary
```

---

## 📂 Directory Architecture

```
week4/
├── README.md                                    # This master runbook & documentation
├── Recon/                                       # Reconnaissance & intelligence gathering
│   ├── dns.txt                                  # dig DNS A-record lookup
│   ├── headers.txt                              # HTTP/2 response headers (LiteSpeed)
│   ├── nmap.txt                                 # Nmap service scan (ports 80 & 443)
│   └── whatweb.txt                              # Web technology fingerprinting
├── M1/                                          # Milestone 1: Initial Access & Portal Bypass
│   ├── login bypass.png                         # Screenshot: SQLi entry (admin' -- ) at /patient/login.php
│   ├── proof of bypass.png                      # Screenshot: Authenticated dashboard at /patient/portal.php
│   ├── patient_report_1.pdf                     # Exfiltrated encrypted report (Sipho Dlamini)
│   ├── patient_report_2.pdf                     # Exfiltrated encrypted report (Priya Reddy)
│   └── patient_report_3.pdf                     # Exfiltrated encrypted report (Emily Thompson)
├── M2/                                          # Milestone 2: Cryptanalysis & Data Recovery
│   ├── hash.txt                                 # Extracted $pdf$2*3*128* hashes
│   ├── recovered passwords.txt                  # Recovered user credentials (file1, file2, file3)
│   ├── patient_report_{1,2,3}_unlocked.pdf      # Decrypted pathology laboratory reports
│   └── all_reports_metadata.txt                 # ExifTool output showing administrative comment leak
├── M3/                                          # Milestone 3: Critical Data Exposure & HR Intelligence
│   ├── mediroza_db_backup_2019.sql              # Exfiltrated MySQL database dump (6,346 bytes)
│   ├── backup_hash.txt                          # SHA-256 verification hash
│   ├── backup_file_info.txt                     # File stat metadata
│   ├── employee_salary_details.txt              # Extracted personnel roster (30 staff, monthly ZAR)
│   ├── department_salary_analysis.txt           # Departmental payroll breakdown across 17 departments
│   ├── salary_statistics.txt / summary.txt      # Payroll summary (ZAR 2,027,000/mo; min/max/avg)
│   └── shareholder_{details,distribution,statistics}.txt # Cap table (10 shareholders, 1,000,000 shares)
├── M4_Report/                                   # Dedicated M4 Deliverable Package
│   ├── Mediroza_Penetration_Test_Report.docx    # Formatted, editable Microsoft Word report (1.0 MB)
│   ├── Mediroza_Penetration_Test_Report.pdf     # Print-ready, 21-page WeasyPrint publication PDF (1.1 MB)
│   ├── Mediroza_Penetration_Test_Report.md      # Master Markdown report source (16 sections)
│   ├── Evidence_Register.xlsx                   # 3-sheet formatted Excel cross-reference workbook
│   ├── Missing_Evidence_Checklist.txt           # Evidence inventory audit & required screenshot index
│   ├── Report_Summary.txt                       # High-level executive briefing document
│   └── images/                                  # Professionally redacted screenshots (PII/passwords masked)
│       ├── M1-01_login_bypass.png
│       ├── M1-02_proof_of_bypass.png
│       ├── M2-02_password_cracking.png
│       ├── M2-03_patient1.png
│       ├── M2-04_patient2.png
│       ├── M2-05_patient3.png
│       └── M3-01_exposed_db.png
├── Screenshots/                                 # Original unedited evidence screenshots
│   ├── exposed db.png                           # Direct browser access to /old backup
│   ├── password cracking.png                    # JTR dictionary attack terminal session
│   └── patient{1,2,3}.png                       # Decrypted pathology reports in document viewer
└── scripts/                                     # Automated report generation & sanitization tooling
    ├── sanitize_images.py                       # Non-destructive PII/password redaction tool
    ├── generate_docx_report.py                  # python-docx technical report generator
    ├── generate_pdf_report.py                   # WeasyPrint HTML/CSS PDF compiler
    └── generate_evidence_register.py            # openpyxl multi-sheet workbook generator
```

---

## 📊 Consolidated Vulnerability Register

| Finding ID | Vulnerability Title | Affected Asset | Severity | CVSS v3.1 | Primary Business Impact |
|:---:|---|---|:---:|:---:|---|
| **F-01** | Unauthorized Access to Confidential Patient Reports | `/patient/login.php` | **CRITICAL** | **9.1** | Unauthenticated authentication bypass via SQL Injection; full compromise of patient reporting dashboard and exfiltration of clinical diagnostic records. |
| **F-02** | Weak Password Protection on Confidential PDF Documents | Mediroza CMS Lab Module | **HIGH** | **7.5** | Trivial user passphrases under Adobe Standard 128-bit RC4 encryption; instant offline dictionary recovery exposing special personal health information. |
| **F-03** | Publicly Accessible SQL Database Backup in Web Root | `/old/mediroza_db_backup_2019.sql` | **CRITICAL** | **9.8** | Architectural storage misconfiguration; unauthenticated downloading of complete internal MySQL database dump. |
| **F-04** | Exposure of Employee Salary and Shareholder Information | `mediroza_hr` Database Schema | **HIGH** | **7.5** | Breach of POPIA Act 4 of 2013; exposure of 30 employee National IDs, phone numbers, emails, salaries (ZAR 2M/mo), and proprietary shareholder equity cap table. |

---

## 📄 Deliverable Suite (`M4_Report/`)

The final consulting deliverables are located in [`M4_Report/`](M4_Report/):

1. 📄 [**Mediroza_Penetration_Test_Report.docx**](M4_Report/Mediroza_Penetration_Test_Report.docx): Fully formatted Microsoft Word deliverable featuring corporate color palettes, styled tables, callout blocks, and embedded redacted evidence screenshots.
2. 📑 [**Mediroza_Penetration_Test_Report.pdf**](M4_Report/Mediroza_Penetration_Test_Report.pdf): 21-page, print-ready PDF compiled via WeasyPrint with sophisticated `@page` CSS rules, running headers, running footers, and page numbers (`Page X of 21`).
3. 📊 [**Evidence_Register.xlsx**](M4_Report/Evidence_Register.xlsx): Three-sheet Excel workbook mapping Evidence IDs to file hashes, paths, sections, and findings.
4. 📋 [**Missing_Evidence_Checklist.txt**](M4_Report/Missing_Evidence_Checklist.txt): Detailed inventory gap audit documenting verified items and cataloging `[SCREENSHOT REQUIRED]` placeholders.
5. 📝 [**Report_Summary.txt**](M4_Report/Report_Summary.txt): High-level executive debriefing covering key findings, compliance impact, and immediate remediation actions.

---

## 👤 Author & Acknowledgments

* **Author:** Rithish S P  
* **GitHub Profile:** [@Ritzz-09](https://github.com/Ritzz-09)  
* **Repository:** [Networkwalks-Internship](https://github.com/Ritzz-09/Networkwalks-Internship)  
* **Framework:** Networkwalks Cybersecurity Internship (Week 4, Batch B083)
