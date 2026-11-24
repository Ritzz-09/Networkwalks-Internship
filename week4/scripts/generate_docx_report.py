#!/usr/bin/env python3
"""
Generates the professional, fully-styled editable Word document
deliverable: Mediroza_Penetration_Test_Report.docx
Using python-docx with custom styling, tables, callout boxes, and embedded images.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCX_OUT = os.path.join(BASE_DIR, "M4_Report", "Mediroza_Penetration_Test_Report.docx")
IMG_DIR = os.path.join(BASE_DIR, "M4_Report", "images")

# Color Palette Constants
COLOR_NAVY = RGBColor(26, 54, 93)      # #1A365D - Primary Headings
COLOR_STEEL = RGBColor(43, 108, 176)   # #2B6CB0 - Subheadings
COLOR_CHARCOAL = RGBColor(45, 55, 72)  # #2D3748 - Body Text
COLOR_MUTED = RGBColor(113, 128, 150)  # #718096 - Metadata & Footers
COLOR_CRITICAL = RGBColor(155, 44, 44) # #9B2C2C - Critical Badge
COLOR_HIGH = RGBColor(221, 107, 32)    # #DD6B20 - High Badge

HEX_NAVY = "1A365D"
HEX_LIGHT_BG = "F7FAFC"
HEX_BORDER = "E2E8F0"
HEX_CRITICAL_BG = "FFF5F5"
HEX_CRITICAL_BORDER = "E53E3E"
HEX_NOTE_BG = "EBF8FF"
HEX_NOTE_BORDER = "3182CE"

def set_cell_background(cell, hex_color):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def style_table(table, col_widths, headers, data, alt_shading=True):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg = HEX_LIGHT_BG if (alt_shading and row_idx % 2 == 1) else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].text = str(val)
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=90, bottom=90, left=130, right=130)
            p = row_cells[col_idx].paragraphs[0]
            # Alignment logic
            if col_idx in (0, 1) and len(str(val)) < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = COLOR_CHARCOAL
                if "CRITICAL" in str(val):
                    run.font.bold = True
                    run.font.color.rgb = COLOR_CRITICAL
                elif "HIGH" in str(val):
                    run.font.bold = True
                    run.font.color.rgb = COLOR_HIGH
                elif "Verified Present" in str(val):
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(34, 84, 61)
                elif "REQUIRED" in str(val):
                    run.font.italic = True
                    run.font.color.rgb = RGBColor(116, 42, 42)

    # Set column widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

def add_callout(doc, text, title="NOTE", alert_type="note"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    bg_color = HEX_CRITICAL_BG if alert_type == "critical" else HEX_NOTE_BG
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"[{title}] ")
    run_t.font.name = "Calibri"
    run_t.font.bold = True
    run_t.font.size = Pt(9.5)
    run_t.font.color.rgb = COLOR_CRITICAL if alert_type == "critical" else COLOR_STEEL
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9)
    run_b.font.color.rgb = COLOR_CHARCOAL
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_STEEL
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_CHARCOAL
    return h

def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_CHARCOAL
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_CHARCOAL
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_image_with_caption(doc, img_filename, caption_text, evidence_id):
    img_path = os.path.join(IMG_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(f"Figure ({evidence_id}): {caption_text}")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = COLOR_MUTED
    else:
        add_callout(doc, f"Image {img_filename} not found on disk at {img_path}", title="MISSING ASSET", alert_type="critical")

def generate_report():
    doc = docx.Document()
    
    # Page setup
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "NETWORKWALKS CYBERSECURITY // MEDIROZA PENETRATION TEST REPORT"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.runs[0].font.name = "Calibri"
        p_hdr.runs[0].font.size = Pt(8)
        p_hdr.runs[0].font.color.rgb = COLOR_MUTED
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.text = "CONFIDENTIAL // RESTRICTED DISTRIBUTION - SUBJECT TO POPIA ACT 4 OF 2013"
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ftr.runs[0].font.name = "Calibri"
        p_ftr.runs[0].font.size = Pt(8)
        p_ftr.runs[0].font.color.rgb = COLOR_MUTED

    # ----------------------------------------------------
    # SECTION 01: COVER PAGE
    # ----------------------------------------------------
    p_cov_pre = doc.add_paragraph()
    p_cov_pre.paragraph_format.space_before = Pt(36)
    p_cov_pre.paragraph_format.space_after = Pt(12)
    r = p_cov_pre.add_run("NETWORKWALKS SECURITY SERVICES // TECHNICAL ASSESSMENT")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_STEEL

    p_cov_title = doc.add_paragraph()
    p_cov_title.paragraph_format.space_after = Pt(6)
    r_title = p_cov_title.add_run("PENETRATION TESTING &\nSECURITY ASSESSMENT REPORT")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_cov_sub.add_run("Comprehensive Black-box Web Application, Cryptanalysis & Digital Forensics Evaluation")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_CHARCOAL

    # Meta Table
    tbl_cov = doc.add_table(rows=1, cols=2)
    tbl_cov.rows[0].cells[0].width = Inches(2.2)
    tbl_cov.rows[0].cells[1].width = Inches(4.3)
    cov_meta = [
        ("Target Entity", "Mediroza General Hospital (Johannesburg, South Africa)"),
        ("Target URL / Host", "https://medirozahospital.com (IP: 199.188.201.16)"),
        ("Project Framework", "Networkwalks Cybersecurity Internship (Week 4, Batch B083)"),
        ("Assessment Type", "Black-Box Web Application Penetration Test"),
        ("Authorized Testing Period", "5 Days (Milestones M1 – M4)"),
        ("Lead Security Analyst", "Rithish S P (Security Consultant & Forensic Analyst)"),
        ("Portfolio Repository", "https://github.com/Ritzz-09/Networkwalks-Internship"),
        ("Deliverable Version", "1.0 (Final Formal Deliverable)"),
        ("Classification", "CONFIDENTIAL // RESTRICTED DISTRIBUTION")
    ]
    style_table(tbl_cov, [Inches(2.2), Inches(4.3)], ["Metadata Attribute", "Assessment Details"], cov_meta, alt_shading=True)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 02: TABLE OF CONTENTS
    # ----------------------------------------------------
    add_heading_1(doc, "02. Table of Contents")
    toc_items = [
        ("01. Cover Page", "Page 1"),
        ("02. Table of Contents", "Page 2"),
        ("03. Executive Summary", "Page 3"),
        ("04. Engagement Overview", "Page 5"),
        ("05. Scope and Rules of Engagement", "Page 6"),
        ("06. Written Authorization", "Page 7"),
        ("07. Reconnaissance and Information Gathering", "Page 8"),
        ("08. Milestone M1 – Initial Access", "Page 10"),
        ("09. Milestone M2 – PDF Encryption and Data Recovery", "Page 13"),
        ("10. Milestone M3 – Critical Data Exposure", "Page 16"),
        ("11. Consolidated Vulnerability Findings", "Page 21"),
        ("12. Risk Assessment", "Page 25"),
        ("13. Recommendations and Remediation", "Page 27"),
        ("14. Overall Conclusion", "Page 30"),
        ("15. Appendices", "Page 31"),
        ("16. Evidence Register", "Page 32")
    ]
    tbl_toc = doc.add_table(rows=1, cols=2)
    style_table(tbl_toc, [Inches(5.0), Inches(1.5)], ["Report Section", "Location"], toc_items, alt_shading=True)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 03: EXECUTIVE SUMMARY
    # ----------------------------------------------------
    add_heading_1(doc, "03. Executive Summary")
    add_body_p(doc, "During the authorized 5-day assessment period for Week 4 of the Networkwalks Cybersecurity Internship (Batch B083), Networkwalks Security Services conducted a black-box cybersecurity penetration test against Mediroza General Hospital's public digital presence (https://medirozahospital.com). Mediroza General Hospital operates clinical diagnostic facilities and specialized pathology laboratories based in Johannesburg, South Africa.")
    add_body_p(doc, "The primary objective of this assessment was to rigorously evaluate the confidentiality, integrity, and availability of patient and corporate data, test access controls on web-facing interfaces, and determine whether an external, unauthenticated attacker could compromise protected electronic health information (ePHI) or proprietary hospital records.")
    
    add_heading_2(doc, "3.1 Assessment Posture & Key Highlights")
    add_body_p(doc, "The assessment revealed a critical security deficit across Mediroza General Hospital's public perimeter. Multiple high-severity architectural and implementation flaws allow an unauthenticated attacker to completely breach the patient confidentiality boundary and compromise hospital corporate governance data within minutes. The testing team uncovered an unbroken, compounding attack chain:")
    
    add_bullet_p(doc, "Authentication Bypass (M1): The public patient portal (/patient/login.php) is vulnerable to SQL Injection, enabling unauthenticated access to the patient results dashboard via a trivial comment payload (admin' -- ).", "Initial Access: ")
    add_bullet_p(doc, "Confidential Document Exfiltration (M1): Three locked patient pathology reports containing sensitive diagnostic evaluations were retrieved directly from the compromised portal session.", "Data Exfiltration: ")
    add_bullet_p(doc, "Trivial Password Cracking (M2): The exfiltrated PDF documents used weak, common passphrases under Adobe Standard 128-bit RC4 encryption. All three passwords were recovered offline in under one second using standard wordlists.", "Cryptanalytic Failure: ")
    add_bullet_p(doc, "Digital Forensics & Metadata Leak (M2): Inspection of decrypted PDF metadata using ExifTool exposed an internal administrative comment by IT Systems Administrator 'j.malik', revealing an unmapped database backup directory (/old).", "Information Disclosure: ")
    add_bullet_p(doc, "Critical Corporate Database Exposure (M3): Browsing to the leaked path (https://medirozahospital.com/old/mediroza_db_backup_2019.sql) allowed the unauthenticated download of a full MySQL database dump (mediroza_hr).", "Critical Data Exposure: ")
    add_bullet_p(doc, "Total Remuneration & Equity Compromise (M3): The database backup contained unencrypted records for 30 staff members (including South African National IDs, phone numbers, emails, and monthly salaries totaling ZAR 2,027,000/month) and complete capitalization records for 10 corporate shareholders.", "Sensitive PII Breach: ")

    add_heading_2(doc, "3.2 High-Level Risk & Vulnerability Summary")
    tbl_exec_vulns = doc.add_table(rows=1, cols=5)
    exec_vuln_data = [
        ("F-01", "Unauthorized Access to Confidential Patient Reports", "/patient/login.php", "9.1", "CRITICAL"),
        ("F-02", "Weak Password Protection on Confidential PDFs", "CMS Lab Module (PDFs)", "7.5", "HIGH"),
        ("F-03", "Publicly Accessible SQL Database Backup in Web Root", "/old/mediroza_db_backup_2019.sql", "9.8", "CRITICAL"),
        ("F-04", "Exposure of Staff Salary and Shareholder Information", "mediroza_hr Database Schema", "7.5", "HIGH")
    ]
    style_table(tbl_exec_vulns, [Inches(1.0), Inches(2.7), Inches(1.6), Inches(1.1), Inches(1.1)], ["Finding ID", "Vulnerability Title", "Affected Asset", "CVSS v3.1", "Severity"], exec_vuln_data)

    add_heading_2(doc, "3.3 Legal & Regulatory Implications (POPIA Act 4 of 2013)")
    add_body_p(doc, "Mediroza General Hospital operates under the statutory requirements of the South African Protection of Personal Information Act (POPIA Act No. 4 of 2013). The empirical findings established during this assessment represent catastrophic compliance failures:")
    add_bullet_p(doc, "Section 26 & 32 (Special Personal Information): Patient medical laboratory reports constitute highly protected health information. Unauthorized disclosure triggers severe regulatory penalties.", "Medical Privacy: ")
    add_bullet_p(doc, "Section 19 (Security Safeguards): The failure to apply basic input sanitization and leaving production database backups in public web directories constitutes non-compliance with the duty to establish reasonable technical measures.", "Duty of Care: ")
    add_bullet_p(doc, "Section 107 (Penalties): Administrative fines of up to ZAR 10,000,000, mandatory public breach notifications, and exposure to civil litigation by impacted employees and patients.", "Financial Liability: ")

    # ----------------------------------------------------
    # SECTION 04: ENGAGEMENT OVERVIEW
    # ----------------------------------------------------
    add_heading_1(doc, "04. Engagement Overview")
    add_body_p(doc, "This technical report documents the outcomes of an authorized black-box penetration testing and digital forensic engagement conducted for Mediroza General Hospital under the Networkwalks Cybersecurity Internship framework (Batch B083, Week 4).")
    
    add_heading_2(doc, "4.1 Organizational Profile")
    add_body_p(doc, "Mediroza General Hospital is a regional healthcare provider and pathology diagnostics institution located at 14 Cedar Avenue, Johannesburg, South Africa. Its online footprint supports patient results delivery, clinician referral communications, and institutional brand presence.")

    add_heading_2(doc, "4.2 Assessment Methodology")
    add_body_p(doc, "Testing followed the Penetration Testing Execution Standard (PTES) and the OWASP Top 10 Web Application Security Framework. The engagement spanned five days and was executed strictly through black-box techniques, meaning no preliminary architecture diagrams, source code access, or internal credentials were provided.")

    # ----------------------------------------------------
    # SECTION 05: SCOPE AND RULES OF ENGAGEMENT
    # ----------------------------------------------------
    add_heading_1(doc, "05. Scope and Rules of Engagement")
    add_body_p(doc, "Strict adherence to scope and operational boundaries was maintained throughout the engagement to prevent any disruption to hospital clinical services.")
    
    add_heading_2(doc, "5.1 In-Scope Assets")
    add_bullet_p(doc, "https://medirozahospital.com (Base Application URL)", "Target Domain: ")
    add_bullet_p(doc, "199.188.201.16 (Resolved Host IP on shared server server274-1.web-hosting.com)", "Target IP Address: ")
    add_bullet_p(doc, "Patient Authentication Portal (/patient/login.php), Dashboard (/patient/portal.php), and related subdirectories.", "Web Applications: ")

    add_heading_2(doc, "5.2 Explicit Rules of Engagement")
    add_bullet_p(doc, "Testing was strictly confined to the authorized domain name. Third-party cloud infrastructure and unassociated co-located systems were excluded.", "Boundary Limitation: ")
    add_bullet_p(doc, "Denial-of-Service (DoS) and Distributed Denial-of-Service (DDoS) testing were strictly prohibited.", "No DoS Testing: ")
    add_bullet_p(doc, "Social engineering, phishing, or spear-phishing of hospital medical staff, administrative employees, or patients was strictly prohibited.", "No Social Engineering: ")
    add_bullet_p(doc, "No destruction, deletion, or malicious alteration of production data or diagnostic patient telemetry was permitted.", "Data Integrity: ")

    # ----------------------------------------------------
    # SECTION 06: WRITTEN AUTHORIZATION
    # ----------------------------------------------------
    add_heading_1(doc, "06. Written Authorization")
    add_body_p(doc, "Written authorization for this cybersecurity assessment was formally established under the Networkwalks Project Brief for Week 4 (Batch B083). The project brief serves as the legal authorization granting security consultants explicit permission to perform penetration testing, cryptanalysis, and forensic exfiltration against https://medirozahospital.com within the specified constraints.")
    add_callout(doc, "In accordance with professional cybersecurity reporting integrity, this document reflects authorization granted by the Networkwalks Project Brief. No hypothetical executive signatures, artificial client representatives, or fictional sign-off dates have been fabricated.", title="AUTHORIZATION INTEGRITY STATEMENT", alert_type="note")

    # ----------------------------------------------------
    # SECTION 07: RECONNAISSANCE
    # ----------------------------------------------------
    add_heading_1(doc, "07. Reconnaissance and Information Gathering")
    add_body_p(doc, "Reconnaissance was performed to enumerate DNS records, open ports, web server technologies, and HTTP response headers without generating disruptive traffic.")
    
    add_heading_2(doc, "7.1 Active DNS Enumeration (dig)")
    add_body_p(doc, "A standard DNS query was executed against the primary target domain: dig medirozahospital.com. The authoritative response returned a single A record pointing to IP 199.188.201.16. Reverse DNS lookup resolved to server274-1.web-hosting.com, indicating that the target utilizes managed enterprise cloud hosting.")
    add_callout(doc, "[SCREENSHOT REQUIRED – DNS Enumeration Output (dig medirozahospital.com)] | Evidence Source: Recon/dns.txt | Evidence ID: RECON-01", title="EVIDENCE PLACEHOLDER: RECON-01", alert_type="note")

    add_heading_2(doc, "7.2 Port and Service Fingerprinting (nmap)")
    add_body_p(doc, "An Nmap version detection scan was conducted targeting web ports 80 and 443: nmap --privileged -sV -p 80,443 -oN nmap.txt medirozahospital.com. The scan determined that both Port 80/tcp (HTTP) and Port 443/tcp (HTTPS) are open and operated by an HAProxy reverse proxy (version 2.0.0 or later), functioning as an edge load balancer.")
    add_callout(doc, "[SCREENSHOT REQUIRED – Nmap Port and Service Scan (nmap -sV -p 80,443)] | Evidence Source: Recon/nmap.txt | Evidence ID: RECON-02", title="EVIDENCE PLACEHOLDER: RECON-02", alert_type="note")

    add_heading_2(doc, "7.3 Web Technology Fingerprinting (whatweb)")
    add_body_p(doc, "Technology stack fingerprinting was executed using whatweb https://medirozahospital.com. The scan identified LiteSpeed Web Server as the web daemon, accelerated by the LiteSpeed caching module (x-turbo-charged-by: LiteSpeed). Direct GET requests to the root URL returned HTTP 403 Forbidden, indicating that directory browsing was restricted at the root level.")
    add_callout(doc, "[SCREENSHOT REQUIRED – Web Technology Fingerprinting (whatweb https://medirozahospital.com)] | Evidence Source: Recon/whatweb.txt | Evidence ID: RECON-03", title="EVIDENCE PLACEHOLDER: RECON-03", alert_type="note")

    add_heading_2(doc, "7.4 HTTP Response Header Inspection (curl)")
    add_body_p(doc, "Header analysis was performed using curl -I https://medirozahospital.com. The response confirmed HTTP/2 protocol support over TLS and corroborated the LiteSpeed server identification. Standard defensive HTTP security headers—such as Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), and X-Frame-Options—were entirely missing.")
    add_callout(doc, "[SCREENSHOT REQUIRED – HTTP Response Header Inspection (curl -I https://medirozahospital.com)] | Evidence Source: Recon/headers.txt | Evidence ID: RECON-04", title="EVIDENCE PLACEHOLDER: RECON-04", alert_type="note")

    # ----------------------------------------------------
    # SECTION 08: MILESTONE M1 – INITIAL ACCESS
    # ----------------------------------------------------
    add_heading_1(doc, "08. Milestone M1 – Initial Access")
    add_heading_2(doc, "8.1 Milestone Objective")
    add_body_p(doc, "The objective of Milestone M1 was to identify an external authentication entry point, evaluate its input validation controls, bypass authentication mechanisms, and exfiltrate three confidential patient pathology laboratory reports.")

    add_heading_2(doc, "8.2 M1 Written Authorization")
    add_body_p(doc, "The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written authorization to identify access flaws in the Mediroza patient portal and exfiltrate three confidential PDF patient reports to demonstrate initial access risk.")

    add_heading_2(doc, "8.3 Entry Point Identification & SQL Injection Bypass")
    add_body_p(doc, "Directory enumeration identified the Patient Portal login page at https://medirozahospital.com/patient/login.php. The interface prompted patients for a Username and Password. The form was found to be vulnerable to classic SQL Injection due to unsafe string concatenation in the back-end authentication query.")
    add_body_p(doc, "By injecting the payload admin' -- into the Username field, the query's password check was commented out. The application processed the command, verified the existence of an administrative account, and established an authenticated session without requiring a valid password.")
    
    add_image_with_caption(doc, "M1-01_login_bypass.png", "Mediroza Patient Portal login form showing the SQL Injection authentication bypass entry (admin' -- ) in the Username field.", "M1-01")

    add_heading_2(doc, "8.4 Portal Access & Exfiltration of Patient PDF Reports")
    add_body_p(doc, "Upon submitting the exploit, the application redirected the session to https://medirozahospital.com/patient/portal.php. The dashboard displayed: 'My lab reports - Your reports are password protected. Use the password sent to you by the laboratory to open each file.'")
    add_body_p(doc, "The dashboard exposed three confidential patient pathology reports. The testing team clicked each download link and exfiltrated all three files:")
    add_bullet_p(doc, "Pathology Report - S. Dlamini (Lab Ref: LR-2024-1187, Date: 2024-11-04, Encrypted PDF, 2,846 bytes)", "Report 1: ")
    add_bullet_p(doc, "Pathology Report - P. Reddy (Lab Ref: LR-2024-1192, Date: 2024-11-05, Encrypted PDF, 2,848 bytes)", "Report 2: ")
    add_bullet_p(doc, "Pathology Report - E. Thompson (Lab Ref: LR-2024-1205, Date: 2024-11-06, Encrypted PDF, 2,881 bytes)", "Report 3: ")

    add_image_with_caption(doc, "M1-02_proof_of_bypass.png", "Authenticated patient dashboard exposing three locked patient laboratory reports available for download.", "M1-02")
    add_callout(doc, "[SCREENSHOT REQUIRED – Local CLI/Directory verification showing downloaded encrypted patient reports] | Evidence Source: Local disk inventory (M1/patient_report_*.pdf) | Evidence ID: M1-03", title="EVIDENCE PLACEHOLDER: M1-03", alert_type="note")

    # ----------------------------------------------------
    # SECTION 09: MILESTONE M2 – PDF ENCRYPTION AND DATA RECOVERY
    # ----------------------------------------------------
    add_heading_1(doc, "09. Milestone M2 – PDF Encryption and Data Recovery")
    add_heading_2(doc, "9.1 Milestone Objective")
    add_body_p(doc, "The objective of Milestone M2 was to inspect the encryption mechanisms applied to the exfiltrated patient reports, execute offline cryptanalysis to recover access to the files, analyze the decrypted medical findings, and perform digital forensics on document metadata.")

    add_heading_2(doc, "9.2 M2 Written Authorization")
    add_body_p(doc, "The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written authorization to analyze the cryptographic protections of the retrieved PDF files, perform password hash cracking, and inspect metadata.")

    add_heading_2(doc, "9.3 Cryptographic Analysis & Hash Cracking")
    add_body_p(doc, "The exfiltrated PDF files utilized Adobe Standard Security Revision 3 (128-bit key length, RC4 cipher). While 128-bit keys resist raw mathematical key exhaustion, the security of the document is entirely dependent on user passphrase entropy.")
    add_body_p(doc, "Hashes were extracted using pdf2john.pl into hash.txt. A dictionary attack was executed using John the Ripper and rockyou.txt: john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt. John the Ripper cracked all three password hashes in under one second (rate: ~126,989 candidates/sec).")
    add_callout(doc, "In accordance with professional ethical standards, the specific cracked cleartext passwords are intentionally omitted from this text and redacted in the evidence screenshot.", title="ETHICAL REDACTION NOTICE", alert_type="note")

    add_image_with_caption(doc, "M2-02_password_cracking.png", "John the Ripper dictionary attack session recovering all three PDF passwords in under one second (passwords redacted).", "M2-02")

    add_heading_2(doc, "9.4 Decrypted Pathology Reports & Clinical Impact")
    add_body_p(doc, "Using the recovered credentials, all three documents were unlocked and examined, exposing sensitive diagnostic medical evaluations:")
    add_bullet_p(doc, "Full Blood Count: White Cell Count elevated at 11.8 x10^9/L (Flagged: HIGH). Normal Haemoglobin (13.9 g/dL) and Creatinine (88 umol/L). Reported by Dr. Rajesh Naidoo.", "Patient 1 (LR-2024-1187): ")
    add_bullet_p(doc, "Lipid Profile: Severely elevated cardiovascular risk markers: Total Cholesterol 6.4 mmol/L (HIGH), LDL Cholesterol 4.1 mmol/L (HIGH), Triglycerides 1.8 mmol/L (HIGH). Reported by Dr. Susan Botha.", "Patient 2 (LR-2024-1192): ")
    add_bullet_p(doc, "Haematology & Deficiency Screen: Low Haemoglobin (11.4 g/dL, LOW), Ferritin (9 ug/L, LOW), Vitamin D (42 nmol/L, LOW), indicating iron-deficiency anaemia. Reported by Dr. Rajesh Naidoo.", "Patient 3 (LR-2024-1205): ")

    add_image_with_caption(doc, "M2-03_patient1.png", "Decrypted pathology report for Patient 1 displaying clinical blood count values (patient PII redacted).", "M2-03")
    add_image_with_caption(doc, "M2-04_patient2.png", "Decrypted pathology report for Patient 2 displaying elevated lipid profile diagnostics (patient PII redacted).", "M2-04")
    add_image_with_caption(doc, "M2-05_patient3.png", "Decrypted pathology report for Patient 3 displaying abnormal haematology and deficiency markers (patient PII redacted).", "M2-05")

    add_heading_2(doc, "9.5 Forensic Metadata Leak: Discovery of Database Backup")
    add_body_p(doc, "Digital forensic metadata inspection was conducted using exiftool across the decrypted files. Inspection of patient_report_3_unlocked.pdf revealed an administrative comment embedded within the PDF stream metadata:")
    add_bullet_p(doc, "j.malik (Jameel Malik, IT Systems Administrator)", "Document Author: ")
    add_bullet_p(doc, "DB backup moved to /old before site migration, do not delete", "Metadata Comment: ")
    add_callout(doc, "[SCREENSHOT REQUIRED – ExifTool Metadata Inspection Output] | Evidence Source: week4/M2/all_reports_metadata.txt (Line 70) | Evidence ID: M2-01", title="EVIDENCE PLACEHOLDER: M2-01", alert_type="critical")

    # ----------------------------------------------------
    # SECTION 10: MILESTONE M3 – CRITICAL DATA EXPOSURE
    # ----------------------------------------------------
    add_heading_1(doc, "10. Milestone M3 – Critical Data Exposure")
    add_heading_2(doc, "10.1 Milestone Objective")
    add_body_p(doc, "The objective of Milestone M3 was to trace the forensic lead discovered in M2, locate the exposed database backup archive, download the SQL dump, and analyze hospital staff remuneration, departmental payroll distributions, and shareholder capitalization structures.")

    add_heading_2(doc, "10.2 M3 Written Authorization")
    add_body_p(doc, "The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written authorization to locate exposed database backups, retrieve the database dump, and extract employee salary and shareholder equity information.")

    add_heading_2(doc, "10.3 Discovery & Exfiltration of Exposed Database Backup")
    add_body_p(doc, "Navigating to the disclosed path—https://medirozahospital.com/old/mediroza_db_backup_2019.sql—confirmed that the web server failed to enforce authentication or restrict access to database archives. The browser immediately rendered the raw, unencrypted MySQL database backup.")
    
    add_image_with_caption(doc, "M3-01_exposed_db.png", "Direct web browser access to publicly exposed SQL database backup at /old/mediroza_db_backup_2019.sql (employee PII redacted).", "M3-01")

    add_body_p(doc, "The SQL backup (6,346 bytes) was downloaded and cryptographically verified:")
    add_bullet_p(doc, "15d8b49ae104b073d5b0a7289189bdc3940bbab96168e9bdac882ac59feed257", "SHA-256 Checksum: ")
    add_bullet_p(doc, "2019-08-27 02:14:03 (Generated by Mediroza CMS 1.4.2 backup module)", "Archive Date: ")
    add_bullet_p(doc, "mediroza_hr (Tables: staff, shareholders)", "Database Name: ")
    add_callout(doc, "[SCREENSHOT REQUIRED – Cryptographic SHA-256 Hash Verification] | Evidence Source: week4/M3/backup_hash.txt | Evidence ID: M3-02", title="EVIDENCE PLACEHOLDER: M3-02", alert_type="note")

    add_heading_2(doc, "10.4 Staff Table & Salary Analysis (30 Employees)")
    add_body_p(doc, "The staff table contained records for 30 hospital employees, complete with Full Names, Job Titles, Departments, Email Addresses, Mobile Phone Numbers, South African National ID Numbers, Monthly Salaries in ZAR, and Employment Start Dates.")
    add_callout(doc, "In strict compliance with POPIA Act 4 of 2013 data minimization and ethical reporting guidelines, individual National ID numbers, telephone numbers, and email addresses have been completely omitted from this report.", title="PRIVACY & PII REDACTION STATEMENT", alert_type="note")

    # Salary Summary Table
    tbl_salary = doc.add_table(rows=1, cols=4)
    salary_summary_data = [
        ("30 Active Staff", "ZAR 19,000.00", "ZAR 160,000.00", "ZAR 67,566.67")
    ]
    style_table(tbl_salary, [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)], ["Total Employees", "Minimum Monthly", "Maximum Monthly", "Average Monthly Salary"], salary_summary_data)

    add_body_p(doc, "Key Payroll Metrics:")
    add_bullet_p(doc, "ZAR 2,027,000.00 per month (ZAR 24,324,000.00 annualized).", "Total Hospital Payroll: ")
    add_bullet_p(doc, "Dr. Johan van der Merwe (Medical Director, Management) at ZAR 160,000.00/month, followed by Sarah Botha (CFO, Finance) at ZAR 152,000.00/month.", "Highest Earners: ")
    add_bullet_p(doc, "Linda Fourie (Receptionist, Front Office) at ZAR 19,000.00/month.", "Lowest Earner: ")
    add_callout(doc, "[SCREENSHOT REQUIRED – MariaDB Salary Analysis Output] | Evidence Source: week4/M3/salary_statistics.txt & salary_summary.txt | Evidence ID: M3-03", title="EVIDENCE PLACEHOLDER: M3-03", alert_type="note")

    add_heading_2(doc, "10.5 Departmental Payroll Breakdown (17 Departments)")
    tbl_dept = doc.add_table(rows=1, cols=5)
    dept_data = [
        ("Radiology", "3", "R 43,000", "R 130,000", "R 217,000.00"),
        ("Diagnostics Lab", "3", "R 35,000", "R 138,000", "R 214,000.00"),
        ("Finance", "2", "R 29,000", "R 152,000", "R 181,000.00"),
        ("Theatre", "2", "R 42,000", "R 135,000", "R 177,000.00"),
        ("Cardiology", "2", "R 35,000", "R 132,000", "R 167,000.00"),
        ("Management", "1", "R 160,000", "R 160,000", "R 160,000.00"),
        ("Pediatrics", "2", "R 33,000", "R 118,000", "R 151,000.00"),
        ("Internal Medicine", "1", "R 128,000", "R 128,000", "R 128,000.00"),
        ("Human Resources", "2", "R 32,000", "R 96,000", "R 128,000.00"),
        ("Emergency & Trauma", "2", "R 34,000", "R 74,000", "R 108,000.00"),
        ("IT", "2", "R 46,000", "R 58,000", "R 104,000.00"),
        ("Pharmacy", "2", "R 26,000", "R 61,000", "R 87,000.00"),
        ("Operations", "2", "R 27,000", "R 52,000", "R 79,000.00"),
        ("Rehabilitation", "1", "R 48,000", "R 48,000", "R 48,000.00"),
        ("Supply Chain", "1", "R 38,000", "R 38,000", "R 38,000.00"),
        ("Administration", "1", "R 21,000", "R 21,000", "R 21,000.00"),
        ("Front Office", "1", "R 19,000", "R 19,000", "R 19,000.00")
    ]
    style_table(tbl_dept, [Inches(1.8), Inches(0.8), Inches(1.2), Inches(1.2), Inches(1.5)], ["Department", "Staff", "Min Salary", "Max Salary", "Monthly Payroll"], dept_data)

    add_heading_2(doc, "10.6 Shareholder Equity & Capitalization Table (10 Shareholders)")
    add_body_p(doc, "The shareholders table exposed the complete private equity ownership structure of the hospital, totaling 1,000,000 shares (100.00% equity):")
    tbl_sh = doc.add_table(rows=1, cols=4)
    sh_data = [
        ("Dr. Rajesh Naidoo", "Ordinary", "180,000", "18.00%"),
        ("Cedar Health Holdings (Pty) Ltd", "Ordinary", "150,000", "15.00%"),
        ("Dr. Johan van der Merwe", "Ordinary", "120,000", "12.00%"),
        ("Reddy Family Trust", "Ordinary", "110,000", "11.00%"),
        ("Thabo Molefe", "Ordinary", "100,000", "10.00%"),
        ("Sarah Botha", "Ordinary", "90,000", "9.00%"),
        ("Dr. Ahmed Kara", "Preferential", "80,000", "8.00%"),
        ("Naledi Zulu", "Ordinary", "70,000", "7.00%"),
        ("Michael Roberts", "Ordinary", "60,000", "6.00%"),
        ("Dr. Vikram Chetty", "Preferential", "40,000", "4.00%")
    ]
    style_table(tbl_sh, [Inches(2.8), Inches(1.3), Inches(1.2), Inches(1.2)], ["Shareholder Entity", "Class", "Shares Held", "Equity %"], sh_data)
    add_callout(doc, "[SCREENSHOT REQUIRED – MariaDB Shareholder Analysis Output] | Evidence Source: week4/M3/shareholder_details.txt & shareholder_distribution.txt | Evidence ID: M3-04", title="EVIDENCE PLACEHOLDER: M3-04", alert_type="note")

    add_heading_2(doc, "10.7 Contextual Note: 2019 Archive Caveat vs. Ongoing Risk")
    add_body_p(doc, "The SQL backup header indicates that the dump was created on 2019-08-27. While current salaries and staffing may have evolved over subsequent years, South African National ID numbers and employee birth dates are permanent identifiers that do not expire. Leaving historical database dumps in public web directories represents an ongoing catastrophic compliance violation under POPIA.")

    # ----------------------------------------------------
    # SECTION 11: CONSOLIDATED VULNERABILITY FINDINGS
    # ----------------------------------------------------
    add_heading_1(doc, "11. Consolidated Vulnerability Findings")
    
    findings = [
        ("F-01", "Unauthorized Access to Confidential Patient Reports", "CRITICAL", "9.1", "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N", "CWE-89 / OWASP A03:2021", "https://medirozahospital.com/patient/login.php",
         "The patient login portal is vulnerable to SQL injection via the Username parameter. Injecting standard comment delimiters (admin' -- ) completely bypasses authentication logic, granting unauthenticated external users access to the patient portal dashboard and enabling the exfiltration of confidential patient laboratory reports.",
         "M1-01, M1-02, M1-03, M2-03, M2-04, M2-05",
         "Refactor authentication routines to implement parameterized queries (Prepared Statements) using PHP PDO or MySQLi. Discontinue dynamic SQL string concatenation entirely."),
        
        ("F-02", "Weak Password Protection on Confidential PDF Documents", "HIGH", "7.5", "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", "CWE-521 / OWASP A02:2021", "Mediroza CMS Laboratory Reporting Module (PDFs)",
         "Patient pathology laboratory reports are distributed using outdated Adobe Standard Encryption (Revision 3, 128-bit RC4) protected by weak, predictable user passphrases. A dictionary attack using John the Ripper and rockyou.txt successfully recovered all document passwords in under one second.",
         "M2-02, M2-03, M2-04, M2-05",
         "Upgrade document cryptography to AES-256 (PDF Revision 6). Enforce minimum 16-character cryptographically random passphrases or transition to authenticated, in-portal viewing over TLS 1.3 without static-password downloadable PDFs."),
         
        ("F-03", "Publicly Accessible SQL Database Backup in Web Root", "CRITICAL", "9.8", "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "CWE-552 / OWASP A05:2021", "https://medirozahospital.com/old/mediroza_db_backup_2019.sql",
         "An unencrypted production MySQL database backup archive was left accessible within an unmapped web root directory (/old). The web server failed to enforce authentication or restrict access to .sql files, allowing any external internet user to download the full internal database dump.",
         "M2-01, M3-01, M3-02",
         "Immediately purge the /old directory from the web server. Configure web server rules to deny HTTP access to .sql, .bak, and archive extensions. Store automated backups in isolated, non-web-accessible off-site storage."),
         
        ("F-04", "Exposure of Employee Salary and Shareholder Information", "HIGH", "7.5", "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N", "CWE-200 / OWASP A01:2021", "mediroza_hr Database Schema (staff & shareholders)",
         "Directly resulting from the architectural failure identified in F-03, the exfiltrated database archive exposed confidential human resource payroll data (30 employees, ZAR 2,027,000 monthly payroll, National IDs, phones, emails) and complete proprietary shareholder equity capitalization records.",
         "M3-01, M3-03, M3-04",
         "Implement encryption at rest for all database tables containing PII and salary figures. Enforce strict least-privilege database user access controls and execute automated data retention policies to purge legacy backups.")
    ]

    for fid, ftitle, fsev, fcvss, fvec, fcwe, fasset, fdesc, fevid, frem in findings:
        add_heading_2(doc, f"Finding {fid}: {ftitle}")
        tbl_f = doc.add_table(rows=1, cols=2)
        tbl_f.rows[0].cells[0].width = Inches(1.8)
        tbl_f.rows[0].cells[1].width = Inches(4.7)
        fdata = [
            ("Finding ID & Title", f"{fid}: {ftitle}"),
            ("Severity & CVSS", f"{fsev} (Base Score: {fcvss})"),
            ("CVSS v3.1 Vector", fvec),
            ("CWE / OWASP Category", fcwe),
            ("Affected Asset", fasset),
            ("Associated Evidence", fevid)
        ]
        style_table(tbl_f, [Inches(1.8), Inches(4.7)], ["Attribute", "Assessment Details"], fdata, alt_shading=True)
        add_body_p(doc, fdesc, bold_prefix="Vulnerability Description: ")
        add_body_p(doc, frem, bold_prefix="Remediation Guidance: ")

    # ----------------------------------------------------
    # SECTION 12: RISK ASSESSMENT
    # ----------------------------------------------------
    add_heading_1(doc, "12. Risk Assessment")
    add_body_p(doc, "Risks were scored using the Common Vulnerability Scoring System (CVSS v3.1). The qualitative risk matrix cross-references Exploit Likelihood against Business Impact:")
    
    tbl_matrix = doc.add_table(rows=1, cols=4)
    m_data = [
        ("Critical Impact", "F-01 (SQLi Bypass), F-03 (Exposed Backup)", "--", "--"),
        ("High Impact", "F-02 (Weak PDF Encryption), F-04 (HR Data Exposure)", "--", "--"),
        ("Medium Impact", "--", "--", "--"),
        ("Low Impact", "--", "--", "--")
    ]
    style_table(tbl_matrix, [Inches(1.8), Inches(1.8), Inches(1.4), Inches(1.5)], ["Impact Tier", "High Likelihood", "Medium Likelihood", "Low Likelihood"], m_data)

    # ----------------------------------------------------
    # SECTION 13: RECOMMENDATIONS AND REMEDIATION
    # ----------------------------------------------------
    add_heading_1(doc, "13. Recommendations and Remediation")
    add_body_p(doc, "Remediation should follow a prioritized, three-phase defense-in-depth architecture:")
    add_bullet_p(doc, "Purge the /old directory from web servers immediately. Implement rewrite rules blocking direct HTTP requests to .sql, .bak, and database extensions. Temporarily patch /patient/login.php to eliminate SQL injection.", "Phase 1: Immediate Containment (Within 24 Hours): ")
    add_bullet_p(doc, "Refactor authentication routines to implement Prepared Statements (PDO/MySQLi). Upgrade PDF generation to AES-256 and strip metadata comments. Deploy ModSecurity WAF rules.", "Phase 2: Application Hardening (Within 7 Days): ")
    add_bullet_p(doc, "Implement automated encrypted off-site backup storage decoupled from web roots. Execute a formal POPIA Section 22 incident review and institute recurring penetration tests.", "Phase 3: Governance & Compliance (Within 30 Days): ")

    # ----------------------------------------------------
    # SECTION 14: OVERALL CONCLUSION
    # ----------------------------------------------------
    add_heading_1(doc, "14. Overall Conclusion")
    add_body_p(doc, "The black-box penetration testing assessment of Mediroza General Hospital demonstrated that multiple critical security vulnerabilities compromise patient diagnostic confidentiality and hospital corporate records. By exploiting a straightforward SQL injection authentication bypass in the patient portal (M1), recovering weak PDF passwords and discovering metadata leaks (M2), and downloading an unauthenticated database backup (M3), full access was obtained to clinical pathology reports, 30 employee personnel records with monthly salaries totaling ZAR 2,027,000, and corporate shareholder equity structures.")
    add_body_p(doc, "Implementing the phased remediation plan outlined in this report will enable Mediroza General Hospital to effectively neutralize these vulnerabilities, protect patient confidentiality, and achieve compliance with statutory data protection standards.")

    # ----------------------------------------------------
    # SECTION 15: APPENDICES
    # ----------------------------------------------------
    add_heading_1(doc, "15. Appendices")
    add_heading_2(doc, "Appendix A: Tool Suite & Versions")
    add_bullet_p(doc, "Kali Linux 2026.2 (Kernel 6.6+)", "Operating System: ")
    add_bullet_p(doc, "DiG 9.20.30, Nmap 7.991, WhatWeb 0.5.5, cURL 8.8.0", "Reconnaissance Suite: ")
    add_bullet_p(doc, "John the Ripper 1.9.0-jumbo-1, pdf2john.pl, rockyou.txt", "Cryptanalysis Suite: ")
    add_bullet_p(doc, "ExifTool 13.55, Poppler pdftotext 24.02.0, MariaDB Client 10.11", "Forensics Suite: ")

    add_heading_2(doc, "Appendix B: Standards & Regulatory References")
    add_bullet_p(doc, "Open Web Application Security Project (2021 Classification)", "OWASP Top 10: ")
    add_bullet_p(doc, "FIRST Common Vulnerability Scoring System v3.1", "CVSS v3.1: ")
    add_bullet_p(doc, "Protection of Personal Information Act (Act No. 4 of 2013, Republic of South Africa)", "POPIA: ")

    # ----------------------------------------------------
    # SECTION 16: EVIDENCE REGISTER
    # ----------------------------------------------------
    add_heading_1(doc, "16. Evidence Register")
    add_body_p(doc, "The table below cross-references all visual screenshots, text logs, and binary artifacts evaluated during this penetration test:")
    
    tbl_ev = doc.add_table(rows=1, cols=5)
    ev_data = [
        ("RECON-01", "Recon/dns.txt", "DNS query resolving target domain to 199.188.201.16", "Informational", "[SCREENSHOT REQUIRED]"),
        ("RECON-02", "Recon/nmap.txt", "Nmap scan identifying open ports 80/443 and HAProxy", "Informational", "[SCREENSHOT REQUIRED]"),
        ("RECON-03", "Recon/whatweb.txt", "WhatWeb fingerprinting LiteSpeed web server & 403 probe", "Informational", "[SCREENSHOT REQUIRED]"),
        ("RECON-04", "Recon/headers.txt", "cURL HTTP/2 response headers inspection (LiteSpeed)", "Informational", "[SCREENSHOT REQUIRED]"),
        ("M1-01", "M1-01_login_bypass.png", "Web login interface showing SQLi auth bypass payload", "F-01", "Verified Present"),
        ("M1-02", "M1-02_proof_of_bypass.png", "Authenticated portal session exposing 3 locked reports", "F-01", "Verified Present"),
        ("M1-03", "M1/patient_report_*.pdf", "Local CLI directory listing showing 3 downloaded PDFs", "F-01", "[SCREENSHOT REQUIRED]"),
        ("M2-01", "M2/all_reports_metadata.txt", "ExifTool metadata inspection showing author j.malik & leak", "F-03", "[SCREENSHOT REQUIRED]"),
        ("M2-02", "M2-02_password_cracking.png", "John the Ripper dictionary attack on PDF hashes (redacted)", "F-02", "Verified Present"),
        ("M2-03", "M2-03_patient1.png", "Decrypted pathology report for S. Dlamini (LR-2024-1187)", "F-01, F-02", "Verified Present"),
        ("M2-04", "M2-04_patient2.png", "Decrypted pathology report for P. Reddy (LR-2024-1192)", "F-01, F-02", "Verified Present"),
        ("M2-05", "M2-05_patient3.png", "Decrypted pathology report for E. Thompson (LR-2024-1205)", "F-01, F-02", "Verified Present"),
        ("M3-01", "M3-01_exposed_db.png", "Direct browser access to SQL backup at /old/...", "F-03, F-04", "Verified Present"),
        ("M3-02", "M3/backup_hash.txt", "Cryptographic SHA-256 hash verification of SQL dump", "F-03", "[SCREENSHOT REQUIRED]"),
        ("M3-03", "M3/salary_statistics.txt", "Local database import & staff salary aggregation queries", "F-04", "[SCREENSHOT REQUIRED]"),
        ("M3-04", "M3/shareholder_details.txt", "Local database shareholder distribution query results", "F-04", "[SCREENSHOT REQUIRED]")
    ]
    style_table(tbl_ev, [Inches(1.0), Inches(1.8), Inches(2.2), Inches(0.9), Inches(1.1)], ["Evidence ID", "Source Asset", "Description", "Finding", "Status"], ev_data)

    doc.save(DOCX_OUT)
    print(f"Report successfully generated and saved to {DOCX_OUT}")

if __name__ == "__main__":
    generate_report()
