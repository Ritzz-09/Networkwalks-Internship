#!/usr/bin/env python3
"""
Generates the publication-grade, print-ready PDF deliverable:
Mediroza_Penetration_Test_Report.pdf
Using WeasyPrint with sophisticated CSS @page rules, running headers/footers,
corporate styling, risk badges, tables, and embedded screenshots.
"""

import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_OUT = os.path.join(BASE_DIR, "M4_Report", "report_temp.html")
PDF_OUT = os.path.join(BASE_DIR, "M4_Report", "Mediroza_Penetration_Test_Report.pdf")
IMG_DIR = os.path.join(BASE_DIR, "M4_Report", "images")

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mediroza General Hospital - Penetration Testing Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 22mm 18mm 22mm 18mm;
    @top-right {{
      content: "NETWORKWALKS SECURITY // MEDIROZA PENETRATION TEST";
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #718096;
      font-weight: bold;
    }}
    @bottom-center {{
      content: "CONFIDENTIAL - SUBJECT TO POPIA ACT 4 OF 2013";
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #a0aec0;
    }}
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #718096;
      font-weight: bold;
    }}
  }}

  @page:first {{
    margin: 0;
    @top-right {{ content: normal; }}
    @bottom-center {{ content: normal; }}
    @bottom-right {{ content: normal; }}
  }}

  body {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #2d3748;
    line-height: 1.5;
    font-size: 9.5pt;
  }}

  /* Cover Page */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    padding: 70px 50px 40px 50px;
    box-sizing: border-box;
    background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .cover-header {{
    border-bottom: 2px solid #3182ce;
    padding-bottom: 15px;
  }}

  .cover-header .brand {{
    font-size: 13pt;
    font-weight: 800;
    letter-spacing: 2px;
    color: #63b3ed;
    text-transform: uppercase;
  }}

  .cover-header .sub-brand {{
    font-size: 9pt;
    color: #cbd5e0;
    letter-spacing: 1px;
    margin-top: 4px;
  }}

  .cover-title-block {{
    margin-top: 60px;
    margin-bottom: 40px;
  }}

  .cover-badge {{
    display: inline-block;
    background-color: #e53e3e;
    color: #ffffff;
    font-size: 8pt;
    font-weight: bold;
    letter-spacing: 1.5px;
    padding: 4px 10px;
    border-radius: 3px;
    text-transform: uppercase;
    margin-bottom: 20px;
  }}

  .cover-title {{
    font-size: 28pt;
    font-weight: 800;
    line-height: 1.2;
    color: #ffffff;
    margin: 0 0 15px 0;
  }}

  .cover-subtitle {{
    font-size: 13pt;
    color: #e2e8f0;
    font-weight: 300;
    line-height: 1.4;
  }}

  .cover-meta-table {{
    width: 100%;
    border-collapse: collapse;
    background-color: rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    overflow: hidden;
    margin-top: 30px;
  }}

  .cover-meta-table td {{
    padding: 9px 15px;
    font-size: 8.5pt;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }}

  .cover-meta-table td.label {{
    color: #90cdf4;
    font-weight: bold;
    width: 32%;
  }}

  .cover-meta-table td.val {{
    color: #ffffff;
  }}

  .cover-footer {{
    margin-top: 40px;
    font-size: 8pt;
    color: #a0aec0;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 15px;
  }}

  /* Typography & Structure */
  h1 {{
    font-size: 17pt;
    font-weight: 800;
    color: #1a365d;
    border-bottom: 2px solid #2b6cb0;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }}

  h2 {{
    font-size: 12.5pt;
    font-weight: 700;
    color: #2b6cb0;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #2d3748;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 10px;
    padding-left: 20px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  .page-break {{
    page-break-after: always;
  }}

  /* Callout Boxes */
  .callout {{
    padding: 10px 14px;
    margin: 12px 0;
    border-radius: 4px;
    font-size: 9pt;
    line-height: 1.4;
  }}

  .callout-note {{
    background-color: #ebf8ff;
    border-left: 4px solid #3182ce;
    color: #2b6cb0;
  }}

  .callout-critical {{
    background-color: #fff5f5;
    border-left: 4px solid #e53e3e;
    color: #9b2c2c;
  }}

  .callout-placeholder {{
    background-color: #fffaf0;
    border-left: 4px solid #dd6b20;
    color: #9c4221;
    font-style: italic;
  }}

  /* Tables */
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 8.5pt;
  }}

  table.data-table th {{
    background-color: #1a365d;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #1a365d;
  }}

  table.data-table td {{
    padding: 6px 9px;
    border: 1px solid #e2e8f0;
    vertical-align: middle;
  }}

  table.data-table tr:nth-child(even) td {{
    background-color: #f7fafc;
  }}

  /* Severity Badges */
  .badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 3px;
    font-weight: bold;
    font-size: 7.5pt;
    text-transform: uppercase;
    color: #ffffff;
  }}

  .badge-critical {{ background-color: #9b2c2c; }}
  .badge-high {{ background-color: #dd6b20; }}
  .badge-medium {{ background-color: #d69e2e; }}
  .badge-verified {{ background-color: #22543d; }}
  .badge-required {{ background-color: #742a2a; font-style: italic; }}

  /* Images */
  .figure-container {{
    margin: 14px 0;
    text-align: center;
    page-break-inside: avoid;
  }}

  .figure-container img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}

  .figure-caption {{
    font-size: 8pt;
    color: #718096;
    margin-top: 5px;
    font-style: italic;
  }}

  /* Code Blocks */
  pre.code-block {{
    background-color: #1a202c;
    color: #edf2f7;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 10px 0;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-header">
    <div class="brand">Networkwalks Security Consulting</div>
    <div class="sub-brand">Enterprise Cyber Defense, Threat Assessment & Forensics</div>
  </div>

  <div class="cover-title-block">
    <div class="cover-badge">Formal Deliverable // Confidential</div>
    <div class="cover-title">PENETRATION TESTING &amp;<br>SECURITY ASSESSMENT REPORT</div>
    <div class="cover-subtitle">Full-Scope Black-box Web Application, Cryptanalysis &amp; Digital Forensics Evaluation</div>

    <table class="cover-meta-table">
      <tr><td class="label">Target Entity</td><td class="val">Mediroza General Hospital (Johannesburg, South Africa)</td></tr>
      <tr><td class="label">Target Domain / Host</td><td class="val">https://medirozahospital.com (Host IP: 199.188.201.16)</td></tr>
      <tr><td class="label">Engagement Framework</td><td class="val">Networkwalks Cybersecurity Internship (Week 4, Batch B083)</td></tr>
      <tr><td class="label">Assessment Type</td><td class="val">Black-Box Web Application Penetration Test</td></tr>
      <tr><td class="label">Assessment Period</td><td class="val">5 Days (Authorized Testing Window)</td></tr>
      <tr><td class="label">Lead Security Analyst</td><td class="val">Rithish S P (Security Consultant &amp; Forensics Analyst)</td></tr>
      <tr><td class="label">Portfolio Repository</td><td class="val">https://github.com/Ritzz-09/Networkwalks-Internship</td></tr>
      <tr><td class="label">Document Classification</td><td class="val">CONFIDENTIAL // STRICT PROPRIETARY DISTRIBUTION ONLY</td></tr>
      <tr><td class="label">Deliverable Version</td><td class="val">1.0 (Final Formal Technical Deliverable)</td></tr>
    </table>
  </div>

  <div class="cover-footer">
    Notice: This document contains proprietary security assessment findings and vulnerability intelligence. Unauthorized distribution, copying, or dissemination is strictly prohibited under the South African Protection of Personal Information Act (POPIA Act 4 of 2013).
  </div>
</div>

<!-- SECTION 02: TABLE OF CONTENTS -->
<div class="page-break">
  <h1>02. Table of Contents</h1>
  <table class="data-table">
    <tr><th>Section Title</th><th style="width: 15%; text-align: center;">Section ID</th></tr>
    <tr><td>Cover Page</td><td style="text-align: center;">Section 01</td></tr>
    <tr><td>Table of Contents</td><td style="text-align: center;">Section 02</td></tr>
    <tr><td>Executive Summary</td><td style="text-align: center;">Section 03</td></tr>
    <tr><td>Engagement Overview</td><td style="text-align: center;">Section 04</td></tr>
    <tr><td>Scope and Rules of Engagement</td><td style="text-align: center;">Section 05</td></tr>
    <tr><td>Written Authorization</td><td style="text-align: center;">Section 06</td></tr>
    <tr><td>Reconnaissance and Information Gathering</td><td style="text-align: center;">Section 07</td></tr>
    <tr><td>Milestone M1 – Initial Access</td><td style="text-align: center;">Section 08</td></tr>
    <tr><td>Milestone M2 – PDF Encryption and Data Recovery</td><td style="text-align: center;">Section 09</td></tr>
    <tr><td>Milestone M3 – Critical Data Exposure</td><td style="text-align: center;">Section 10</td></tr>
    <tr><td>Consolidated Vulnerability Findings (F-01 to F-04)</td><td style="text-align: center;">Section 11</td></tr>
    <tr><td>Risk Assessment &amp; Severity Matrix</td><td style="text-align: center;">Section 12</td></tr>
    <tr><td>Recommendations and Remediation Roadmap</td><td style="text-align: center;">Section 13</td></tr>
    <tr><td>Overall Conclusion</td><td style="text-align: center;">Section 14</td></tr>
    <tr><td>Appendices (Tool Suite &amp; Regulatory Standards)</td><td style="text-align: center;">Section 15</td></tr>
    <tr><td>Evidence Register &amp; Forensic Artifacts Register</td><td style="text-align: center;">Section 16</td></tr>
  </table>
</div>

<!-- SECTION 03: EXECUTIVE SUMMARY -->
<div>
  <h1>03. Executive Summary</h1>
  <p>During the scheduled 5-day assessment window for Week 4 of the Networkwalks Cybersecurity Internship (Batch B083), Networkwalks Security Services conducted an authorized black-box penetration test against <strong>Mediroza General Hospital</strong>'s public web presence (<strong>https://medirozahospital.com</strong>). Mediroza General Hospital operates medical diagnostic facilities and SANAS-accredited pathology laboratories located in Johannesburg, South Africa.</p>
  
  <p>The primary objective was to rigorously assess the security controls protecting confidential patient health records, test access boundaries on internet-facing web interfaces, and evaluate whether an external, unauthenticated attacker could breach the perimeter to acquire Electronic Protected Health Information (ePHI) or sensitive hospital administrative assets.</p>

  <h2>3.1 Key Findings &amp; Compounding Attack Chain</h2>
  <p>The assessment established an alarming overall security deficit. Multiple architectural and implementation vulnerabilities allow an external attacker to execute an unbroken attack chain that completely compromises patient confidentiality and internal corporate records in under 30 minutes:</p>

  <ul>
    <li><strong>Authentication Bypass (M1):</strong> The patient login portal (<code>/patient/login.php</code>) is vulnerable to SQL Injection. Submitting a SQL comment sequence (<code>admin' -- </code>) completely bypassed authentication, providing administrative access to the patient dashboard without valid credentials.</li>
    <li><strong>Patient Laboratory Report Exfiltration (M1):</strong> From the compromised portal session, the tester exfiltrated three locked patient pathology reports containing confidential diagnostic evaluations.</li>
    <li><strong>Trivial Password Cracking (M2):</strong> The exfiltrated reports were protected with Adobe Standard Encryption (128-bit RC4), but utilized trivial user passphrases. A dictionary attack using John the Ripper cracked all three documents in under one second.</li>
    <li><strong>Forensic Metadata Information Disclosure (M2):</strong> ExifTool inspection of decrypted PDF metadata revealed an unauthorized administrative comment by IT Systems Administrator "j.malik" disclosing that a database backup had been moved to <code>/old</code> before site migration.</li>
    <li><strong>Critical Public Database Backup Exposure (M3):</strong> Navigating to the disclosed path (<code>https://medirozahospital.com/old/mediroza_db_backup_2019.sql</code>) confirmed that an unencrypted MySQL database dump (<code>mediroza_hr</code>) was publicly accessible over HTTP without authentication.</li>
    <li><strong>Mass Personnel, Payroll &amp; Shareholder Equity Compromise (M3):</strong> Ingesting the database dump exposed complete records for 30 hospital employees (including South African National IDs, mobile phone numbers, emails, and monthly salaries totaling ZAR 2,027,000/month) and complete capitalization records for 10 corporate shareholders.</li>
  </ul>

  <h2>3.2 Consolidated Vulnerability Summary</h2>
  <table class="data-table">
    <tr><th>ID</th><th>Vulnerability Title</th><th>Affected Asset</th><th style="text-align: center;">CVSS v3.1</th><th style="text-align: center;">Severity</th></tr>
    <tr><td><strong>F-01</strong></td><td>Unauthorized Access to Confidential Patient Reports</td><td>/patient/login.php</td><td style="text-align: center;">9.1</td><td style="text-align: center;"><span class="badge badge-critical">CRITICAL</span></td></tr>
    <tr><td><strong>F-02</strong></td><td>Weak Password Protection on Confidential PDFs</td><td>Mediroza CMS Lab Module</td><td style="text-align: center;">7.5</td><td style="text-align: center;"><span class="badge badge-high">HIGH</span></td></tr>
    <tr><td><strong>F-03</strong></td><td>Publicly Accessible SQL Database Backup in Web Root</td><td>/old/mediroza_db_backup_2019.sql</td><td style="text-align: center;">9.8</td><td style="text-align: center;"><span class="badge badge-critical">CRITICAL</span></td></tr>
    <tr><td><strong>F-04</strong></td><td>Exposure of Staff Salary &amp; Shareholder Information</td><td>mediroza_hr Database Schema</td><td style="text-align: center;">7.5</td><td style="text-align: center;"><span class="badge badge-high">HIGH</span></td></tr>
  </table>

  <h2>3.3 Regulatory &amp; Legal Compliance Liabilities (POPIA Act 4 of 2013)</h2>
  <p>Mediroza General Hospital's operations in Johannesburg fall under the strict statutory purview of South Africa's <strong>Protection of Personal Information Act (POPIA Act No. 4 of 2013)</strong>. The empirical findings establish direct statutory violations:</p>
  <ul>
    <li><strong>Special Personal Information (Sections 26 &amp; 32):</strong> Medical diagnostic results are legally categorized as special personal information. Exposing patient health evaluations constitutes a grave compliance breach.</li>
    <li><strong>Security Safeguards Duty (Section 19):</strong> The hospital failed to establish reasonable technical safeguards to secure the integrity and confidentiality of personal information, evidenced by SQL injection vulnerabilities and publicly accessible database dumps.</li>
    <li><strong>Financial Penalties (Section 107):</strong> The Information Regulator is empowered to impose administrative fines of up to <strong>ZAR 10 Million</strong>, alongside severe reputational exposure and civil damages from impacted patients and staff.</li>
  </ul>
</div>

<div class="page-break">
  <!-- SECTION 04: ENGAGEMENT OVERVIEW -->
  <h1>04. Engagement Overview</h1>
  <p>Networkwalks Security Services was formally engaged to conduct a black-box cybersecurity assessment of Mediroza General Hospital's internet-facing digital infrastructure under the Networkwalks Cybersecurity Internship framework (Batch B083, Week 4).</p>
  
  <h2>4.1 Organizational Profile</h2>
  <p>Mediroza General Hospital is an established medical center located at 14 Cedar Avenue, Johannesburg, South Africa (Tel: +27 11 555 0100). The facility operates specialized clinical departments and an on-site SANAS-accredited pathology laboratory (Ref M0417) providing laboratory reporting services to referring clinicians and patients.</p>

  <h2>4.2 Assessment Methodology</h2>
  <p>The assessment adhered to the <strong>Penetration Testing Execution Standard (PTES)</strong> and evaluated target assets against the <strong>OWASP Top 10 Web Application Security Risks (2021)</strong>. Testing was conducted strictly through black-box techniques, meaning no source code, architectural blueprints, or credentials were provided in advance.</p>

  <!-- SECTION 05: SCOPE AND RULES OF ENGAGEMENT -->
  <h1>05. Scope and Rules of Engagement</h1>
  <p>Testing was strictly restricted to authorized web assets. The defined scope and rules of engagement were rigorously maintained:</p>
  
  <h2>5.1 In-Scope Assets</h2>
  <ul>
    <li><strong>Target Domain:</strong> <code>medirozahospital.com</code></li>
    <li><strong>Target URL:</strong> <code>https://medirozahospital.com</code></li>
    <li><strong>Target IP Address:</strong> <code>199.188.201.16</code> (Shared hosting node: <code>server274-1.web-hosting.com</code>)</li>
    <li><strong>Web Applications:</strong> Mediroza CMS (v1.4.2), Patient Authentication Portal (<code>/patient/login.php</code>), Results Dashboard (<code>/patient/portal.php</code>), and associated directories.</li>
  </ul>

  <h2>5.2 Strict Rules of Engagement</h2>
  <ul>
    <li>Testing was strictly restricted to the authorized domain name. Third-party cloud systems were excluded.</li>
    <li>No Denial-of-Service (DoS) or Distributed Denial-of-Service (DDoS) testing was conducted.</li>
    <li>No social engineering, phishing, or pretexting attacks targeting hospital staff or patients were permitted.</li>
    <li>No testing was conducted outside the agreed scope. No data corruption or malicious destruction of records was performed.</li>
  </ul>

  <!-- SECTION 06: WRITTEN AUTHORIZATION -->
  <h1>06. Written Authorization</h1>
  <p>Written authorization for this engagement was explicitly granted under the <strong>Networkwalks Project Brief (Week 4, Batch B083)</strong>. The project brief legally authorized testing teams to assess the target environment, execute exploit payloads, and exfiltrate proof-of-concept evidence within defined rules of engagement.</p>
  
  <div class="callout callout-note">
    <strong>WRITTEN AUTHORIZATION INTEGRITY STATEMENT:</strong> This report strictly reflects the explicit authorization granted by the Networkwalks Project Brief. In compliance with professional ethics, no hypothetical client signature, artificial corporate officer, or fabricated approval date has been invented.
  </div>
</div>

<div class="page-break">
  <!-- SECTION 07: RECONNAISSANCE -->
  <h1>07. Reconnaissance and Information Gathering</h1>
  <p>Reconnaissance was executed using non-disruptive footprinting tools to map target infrastructure, DNS records, services, and web technologies.</p>

  <h2>7.1 DNS Interrogation (dig)</h2>
  <p>Active DNS queries were performed against <code>medirozahospital.com</code>. The query resolved to IP address <code>199.188.201.16</code>, with reverse DNS identifying <code>server274-1.web-hosting.com</code>, indicating an enterprise shared-hosting cloud node.</p>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – DNS Enumeration Output (dig medirozahospital.com)]</strong><br>
    Evidence Source: <code>week4/Recon/dns.txt</code> | Evidence ID: RECON-01
  </div>

  <h2>7.2 Port and Service Detection (nmap)</h2>
  <p>A targeted port scan (<code>nmap -sV -p 80,443 medirozahospital.com</code>) identified open web ports operated by an edge load balancer:</p>
  <ul>
    <li><strong>Port 80/tcp:</strong> Open - <code>http-proxy</code> (HAProxy http proxy 2.0.0 or later)</li>
    <li><strong>Port 443/tcp:</strong> Open - <code>ssl/http-proxy</code> (HAProxy http proxy 2.0.0 or later)</li>
  </ul>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – Nmap Port and Service Scan (nmap -sV -p 80,443)]</strong><br>
    Evidence Source: <code>week4/Recon/nmap.txt</code> | Evidence ID: RECON-02
  </div>

  <h2>7.3 Web Fingerprinting &amp; HTTP Response Headers (whatweb &amp; curl)</h2>
  <p>Technology stack fingerprinting (<code>whatweb https://medirozahospital.com</code>) revealed that the application is powered by <strong>LiteSpeed Web Server</strong> with LiteSpeed caching enabled (<code>x-turbo-charged-by: LiteSpeed</code>). Direct requests to the web root yielded an HTTP 403 Forbidden status.</p>
  <p>Header inspection via <code>curl -I</code> corroborated HTTP/2 protocol support over TLS and verified the complete absence of defensive security headers (HSTS, CSP, X-Frame-Options).</p>
  
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – Web Technology Fingerprinting (whatweb)]</strong><br>
    Evidence Source: <code>week4/Recon/whatweb.txt</code> | Evidence ID: RECON-03
  </div>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – HTTP Response Header Inspection (curl -I)]</strong><br>
    Evidence Source: <code>week4/Recon/headers.txt</code> | Evidence ID: RECON-04
  </div>
</div>

<div class="page-break">
  <!-- SECTION 08: MILESTONE M1 -->
  <h1>08. Milestone M1 – Initial Access</h1>
  
  <h2>8.1 Objective &amp; Written Authorization</h2>
  <p>The objective of Milestone M1 was to discover an external entry point on the hospital's web perimeter, bypass authentication controls, and retrieve three confidential patient pathology reports.</p>
  <div class="callout callout-note">
    <strong>M1 WRITTEN AUTHORIZATION:</strong> The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written permission to identify an entry point on the patient portal and exfiltrate three confidential PDF reports to prove initial unauthorized access.
  </div>

  <h2>8.2 Application Entry Point &amp; SQL Injection Exploitation</h2>
  <p>The testing team identified the Patient Portal login interface at <code>https://medirozahospital.com/patient/login.php</code>. Input handling analysis revealed that the Username parameter was concatenated directly into an unparameterized database query.</p>
  <p>Entering the payload <code>admin' -- </code> in the Username field caused the SQL parser to evaluate the username while commenting out the remainder of the query, including the password check:</p>

  <pre class="code-block">
-- Conceptual Vulnerable Back-End Query:
SELECT * FROM users WHERE username = 'admin' -- ' AND password = '$password' LIMIT 1;
  </pre>

  <p>Submitting this payload successfully bypassed authentication, granting immediate administrative access to the patient portal dashboard at <code>/patient/portal.php</code> without valid credentials.</p>

  <div class="figure-container">
    <img src="images/M1-01_login_bypass.png" alt="Login Bypass">
    <div class="figure-caption">Figure M1-01 (Evidence ID: M1-01): Patient Portal login form showing the SQL Injection authentication bypass entry (admin' -- ).</div>
  </div>

  <h2>8.3 Exfiltration of Three Confidential Patient Reports</h2>
  <p>The authenticated portal exposed three locked patient laboratory reports available for immediate download. The testing team downloaded all three target files:</p>
  <ul>
    <li><code>patient_report_1.pdf</code>: Sipho Dlamini | Lab Ref: LR-2024-1187 (2,846 bytes | SHA-256: <code>3a520268...</code>)</li>
    <li><code>patient_report_2.pdf</code>: Priya Reddy | Lab Ref: LR-2024-1192 (2,848 bytes | SHA-256: <code>9df4a323...</code>)</li>
    <li><code>patient_report_3.pdf</code>: Emily Thompson | Lab Ref: LR-2024-1205 (2,881 bytes | SHA-256: <code>87556f87...</code>)</li>
  </ul>

  <div class="figure-container">
    <img src="images/M1-02_proof_of_bypass.png" alt="Proof of Bypass">
    <div class="figure-caption">Figure M1-02 (Evidence ID: M1-02): Authenticated portal dashboard exposing three locked patient laboratory reports available for download.</div>
  </div>

  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – Local CLI/Directory verification showing downloaded encrypted patient reports]</strong><br>
    Evidence Source: Local disk inventory (<code>M1/patient_report_*.pdf</code>) | Evidence ID: M1-03
  </div>
</div>

<div class="page-break">
  <!-- SECTION 09: MILESTONE M2 -->
  <h1>09. Milestone M2 – PDF Encryption and Data Recovery</h1>
  
  <h2>9.1 Objective &amp; Written Authorization</h2>
  <p>The objective of Milestone M2 was to inspect document encryption on the exfiltrated PDF files, perform password recovery, verify document decryption, and conduct digital forensic metadata analysis.</p>
  <div class="callout callout-note">
    <strong>M2 WRITTEN AUTHORIZATION:</strong> The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written permission to analyze document cryptography, execute password hash recovery, and inspect metadata across the retrieved patient files.
  </div>

  <h2>9.2 Cryptanalysis &amp; Offline Password Cracking</h2>
  <p>Inspection established that the files were protected using Adobe Standard Security Revision 3 (128-bit RC4 encryption). Hashes were extracted via <code>pdf2john.pl</code> into <code>hash.txt</code>. A dictionary attack was launched using <strong>John the Ripper</strong> and <code>rockyou.txt</code>:</p>
  
  <pre class="code-block">
$ john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
Loaded 3 password hashes with 3 different salts (PDF Revision 3, 128-bit key)
Rate: 126,989 candidates/sec -> 3g 0:00:00:00 DONE
  </pre>

  <p>John the Ripper cracked all three password hashes in less than one second, proving that trivial, predictable passphrases were used to protect clinical data.</p>
  <div class="callout callout-note">
    <strong>ETHICAL REDACTION NOTICE:</strong> In compliance with consulting ethics, cleartext cracked passwords are intentionally omitted from this text and redacted in the evidence screenshot.
  </div>

  <div class="figure-container">
    <img src="images/M2-02_password_cracking.png" alt="Password Cracking">
    <div class="figure-caption">Figure M2-02 (Evidence ID: M2-02): John the Ripper dictionary attack session recovering all three PDF passwords in under one second (passwords redacted).</div>
  </div>

  <h2>9.3 Decrypted Pathology Reports &amp; Diagnostic Findings</h2>
  <p>Using the recovered credentials, the files were unlocked (<code>patient_report_1_unlocked.pdf</code>, <code>2_unlocked.pdf</code>, <code>3_unlocked.pdf</code>), exposing confidential clinical diagnostic data:</p>
  <ul>
    <li><strong>Report 1 (LR-2024-1187):</strong> White Cell Count elevated at 11.8 x10^9/L (HIGH), normal Fasting Glucose (5.4 mmol/L). Reported by Dr. Rajesh Naidoo.</li>
    <li><strong>Report 2 (LR-2024-1192):</strong> Severely elevated cardiovascular markers: Total Cholesterol 6.4 mmol/L (HIGH), LDL Cholesterol 4.1 mmol/L (HIGH), Triglycerides 1.8 mmol/L (HIGH). Reported by Dr. Susan Botha.</li>
    <li><strong>Report 3 (LR-2024-1205):</strong> Abnormal haematology: Low Haemoglobin (11.4 g/dL, LOW), Ferritin (9 ug/L, LOW), Vitamin D (42 nmol/L, LOW). Reported by Dr. Rajesh Naidoo.</li>
  </ul>

  <div class="figure-container">
    <img src="images/M2-03_patient1.png" alt="Patient 1 Report">
    <div class="figure-caption">Figure M2-03 (Evidence ID: M2-03): Decrypted pathology report for Patient 1 displaying clinical blood count values (patient PII redacted).</div>
  </div>
  <div class="figure-container">
    <img src="images/M2-04_patient2.png" alt="Patient 2 Report">
    <div class="figure-caption">Figure M2-04 (Evidence ID: M2-04): Decrypted pathology report for Patient 2 displaying elevated lipid profile diagnostics (patient PII redacted).</div>
  </div>
  <div class="figure-container">
    <img src="images/M2-05_patient3.png" alt="Patient 3 Report">
    <div class="figure-caption">Figure M2-05 (Evidence ID: M2-05): Decrypted pathology report for Patient 3 displaying abnormal haematology and deficiency markers (patient PII redacted).</div>
  </div>

  <h2>9.4 Forensic Metadata Analysis: Critical Lead to Database Backup</h2>
  <p>Metadata inspection with <code>exiftool</code> across the decrypted PDFs uncovered an extraordinary information disclosure embedded within <code>patient_report_3_unlocked.pdf</code>:</p>
  <ul>
    <li><strong>Author:</strong> <code>j.malik</code> (Jameel Malik, IT Systems Administrator)</li>
    <li><strong>Internal Comment:</strong> <code>DB backup moved to /old before site migration, do not delete</code></li>
  </ul>
  <div class="callout callout-critical">
    <strong>[SCREENSHOT REQUIRED – ExifTool Metadata Inspection Output]</strong><br>
    Evidence Source: <code>week4/M2/all_reports_metadata.txt</code> (Line 70) | Evidence ID: M2-01
  </div>
</div>

<div class="page-break">
  <!-- SECTION 10: MILESTONE M3 -->
  <h1>10. Milestone M3 – Critical Data Exposure</h1>
  
  <h2>10.1 Objective &amp; Written Authorization</h2>
  <p>The objective of Milestone M3 was to trace the forensic lead discovered in M2, locate the exposed database backup archive, download the SQL dump, and analyze hospital staff remuneration, departmental payroll distributions, and shareholder capitalization structures.</p>
  <div class="callout callout-note">
    <strong>M3 WRITTEN AUTHORIZATION:</strong> The Networkwalks Project Brief (Week 4, Batch B083) explicitly grants written permission to locate exposed database backups, retrieve the database dump, and extract employee salary and shareholder equity information.
  </div>

  <h2>10.2 Discovery &amp; Exfiltration of Exposed Database Backup</h2>
  <p>Navigating to the disclosed path—<code>https://medirozahospital.com/old/mediroza_db_backup_2019.sql</code>—confirmed that the web server failed to enforce authentication or restrict access to database archives. The browser immediately rendered the raw, unencrypted MySQL database backup:</p>

  <div class="figure-container">
    <img src="images/M3-01_exposed_db.png" alt="Exposed Database">
    <div class="figure-caption">Figure M3-01 (Evidence ID: M3-01): Direct web browser access to publicly exposed SQL database backup at /old/mediroza_db_backup_2019.sql (employee PII redacted).</div>
  </div>

  <p>The SQL backup (6,346 bytes) was downloaded and cryptographically verified:</p>
  <ul>
    <li><strong>SHA-256 Checksum:</strong> <code>15d8b49ae104b073d5b0a7289189bdc3940bbab96168e9bdac882ac59feed257</code></li>
    <li><strong>Backup Timestamp:</strong> <code>2019-08-27 02:14:03</code> (Generated by Mediroza CMS 1.4.2 backup module)</li>
    <li><strong>Database Target:</strong> <code>mediroza_hr</code> (Tables: <code>staff</code>, <code>shareholders</code>)</li>
  </ul>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – Cryptographic SHA-256 Hash Verification]</strong><br>
    Evidence Source: <code>week4/M3/backup_hash.txt</code> | Evidence ID: M3-02
  </div>

  <h2>10.3 Staff Table &amp; Salary Analysis (30 Employees)</h2>
  <p>The <code>staff</code> table contained records for 30 hospital employees, complete with Full Names, Job Titles, Departments, Email Addresses, Mobile Phone Numbers, South African National ID Numbers, Monthly Salaries in ZAR, and Employment Start Dates.</p>
  <div class="callout callout-note">
    <strong>PRIVACY &amp; PII REDACTION STATEMENT:</strong> In strict compliance with POPIA Act 4 of 2013 data minimization and ethical reporting guidelines, individual National ID numbers, telephone numbers, and email addresses have been completely omitted from this report.
  </div>

  <table class="data-table">
    <tr><th>Total Staff Count</th><th>Minimum Monthly Salary</th><th>Maximum Monthly Salary</th><th>Average Monthly Salary</th></tr>
    <tr><td>30 Active Employees</td><td>ZAR 19,000.00</td><td>ZAR 160,000.00</td><td>ZAR 67,566.67</td></tr>
  </table>

  <p><strong>Key Payroll Metrics:</strong></p>
  <ul>
    <li><strong>Total Monthly Hospital Payroll:</strong> <strong>ZAR 2,027,000.00</strong> (ZAR 24,324,000.00 annualized).</li>
    <li><strong>Top Earners:</strong> Dr. Johan van der Merwe (Medical Director, Management) at ZAR 160,000.00/month; Sarah Botha (CFO, Finance) at ZAR 152,000.00/month.</li>
    <li><strong>Entry-Level:</strong> Linda Fourie (Receptionist, Front Office) at ZAR 19,000.00/month.</li>
  </ul>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – MariaDB Salary Analysis Output]</strong><br>
    Evidence Source: <code>week4/M3/salary_statistics.txt</code> &amp; <code>salary_summary.txt</code> | Evidence ID: M3-03
  </div>

  <h2>10.4 Departmental Payroll Breakdown (17 Departments)</h2>
  <table class="data-table">
    <tr><th>Department</th><th style="text-align: center;">Staff Count</th><th>Min Salary</th><th>Max Salary</th><th>Department Monthly Payroll</th></tr>
    <tr><td>Radiology</td><td style="text-align: center;">3</td><td>R 43,000</td><td>R 130,000</td><td><strong>R 217,000.00</strong></td></tr>
    <tr><td>Diagnostics Lab</td><td style="text-align: center;">3</td><td>R 35,000</td><td>R 138,000</td><td><strong>R 214,000.00</strong></td></tr>
    <tr><td>Finance</td><td style="text-align: center;">2</td><td>R 29,000</td><td>R 152,000</td><td><strong>R 181,000.00</strong></td></tr>
    <tr><td>Theatre</td><td style="text-align: center;">2</td><td>R 42,000</td><td>R 135,000</td><td><strong>R 177,000.00</strong></td></tr>
    <tr><td>Cardiology</td><td style="text-align: center;">2</td><td>R 35,000</td><td>R 132,000</td><td><strong>R 167,000.00</strong></td></tr>
    <tr><td>Management</td><td style="text-align: center;">1</td><td>R 160,000</td><td>R 160,000</td><td><strong>R 160,000.00</strong></td></tr>
    <tr><td>Pediatrics</td><td style="text-align: center;">2</td><td>R 33,000</td><td>R 118,000</td><td><strong>R 151,000.00</strong></td></tr>
    <tr><td>Internal Medicine</td><td style="text-align: center;">1</td><td>R 128,000</td><td>R 128,000</td><td><strong>R 128,000.00</strong></td></tr>
    <tr><td>Human Resources</td><td style="text-align: center;">2</td><td>R 32,000</td><td>R 96,000</td><td><strong>R 128,000.00</strong></td></tr>
    <tr><td>Emergency &amp; Trauma</td><td style="text-align: center;">2</td><td>R 34,000</td><td>R 74,000</td><td><strong>R 108,000.00</strong></td></tr>
    <tr><td>IT</td><td style="text-align: center;">2</td><td>R 46,000</td><td>R 58,000</td><td><strong>R 104,000.00</strong></td></tr>
    <tr><td>Pharmacy</td><td style="text-align: center;">2</td><td>R 26,000</td><td>R 61,000</td><td><strong>R 87,000.00</strong></td></tr>
    <tr><td>Operations</td><td style="text-align: center;">2</td><td>R 27,000</td><td>R 52,000</td><td><strong>R 79,000.00</strong></td></tr>
    <tr><td>Rehabilitation</td><td style="text-align: center;">1</td><td>R 48,000</td><td>R 48,000</td><td><strong>R 48,000.00</strong></td></tr>
    <tr><td>Supply Chain</td><td style="text-align: center;">1</td><td>R 38,000</td><td>R 38,000</td><td><strong>R 38,000.00</strong></td></tr>
    <tr><td>Administration</td><td style="text-align: center;">1</td><td>R 21,000</td><td>R 21,000</td><td><strong>R 21,000.00</strong></td></tr>
    <tr><td>Front Office</td><td style="text-align: center;">1</td><td>R 19,000</td><td>R 19,000</td><td><strong>R 19,000.00</strong></td></tr>
  </table>

  <h2>10.5 Shareholder Capitalization Table (10 Shareholders)</h2>
  <p>The <code>shareholders</code> table exposed the private corporate ownership structure of Mediroza General Hospital, totaling 1,000,000 shares (100.00% equity):</p>
  
  <table class="data-table">
    <tr><th>Shareholder Entity</th><th>Share Class</th><th style="text-align: center;">Shares Held</th><th style="text-align: center;">Equity %</th></tr>
    <tr><td>Dr. Rajesh Naidoo</td><td>Ordinary</td><td style="text-align: center;">180,000</td><td style="text-align: center;">18.00%</td></tr>
    <tr><td>Cedar Health Holdings (Pty) Ltd</td><td>Ordinary</td><td style="text-align: center;">150,000</td><td style="text-align: center;">15.00%</td></tr>
    <tr><td>Dr. Johan van der Merwe</td><td>Ordinary</td><td style="text-align: center;">120,000</td><td style="text-align: center;">12.00%</td></tr>
    <tr><td>Reddy Family Trust</td><td>Ordinary</td><td style="text-align: center;">110,000</td><td style="text-align: center;">11.00%</td></tr>
    <tr><td>Thabo Molefe</td><td>Ordinary</td><td style="text-align: center;">100,000</td><td style="text-align: center;">10.00%</td></tr>
    <tr><td>Sarah Botha</td><td>Ordinary</td><td style="text-align: center;">90,000</td><td style="text-align: center;">9.00%</td></tr>
    <tr><td>Dr. Ahmed Kara</td><td>Preferential</td><td style="text-align: center;">80,000</td><td style="text-align: center;">8.00%</td></tr>
    <tr><td>Naledi Zulu</td><td>Ordinary</td><td style="text-align: center;">70,000</td><td style="text-align: center;">7.00%</td></tr>
    <tr><td>Michael Roberts</td><td>Ordinary</td><td style="text-align: center;">60,000</td><td style="text-align: center;">6.00%</td></tr>
    <tr><td>Dr. Vikram Chetty</td><td>Preferential</td><td style="text-align: center;">40,000</td><td style="text-align: center;">4.00%</td></tr>
    <tr><td><strong>TOTAL (10 Shareholders)</strong></td><td>--</td><td style="text-align: center;"><strong>1,000,000</strong></td><td style="text-align: center;"><strong>100.00%</strong></td></tr>
  </table>

  <p><strong>Share Class Distribution:</strong></p>
  <ul>
    <li><strong>Ordinary Shares:</strong> 8 Shareholders | 880,000 Shares | 88.00% Ownership</li>
    <li><strong>Preferential Shares:</strong> 2 Shareholders | 120,000 Shares | 12.00% Ownership</li>
  </ul>
  <div class="callout callout-placeholder">
    <strong>[SCREENSHOT REQUIRED – MariaDB Shareholder Analysis Output]</strong><br>
    Evidence Source: <code>week4/M3/shareholder_details.txt</code> &amp; <code>shareholder_distribution.txt</code> | Evidence ID: M3-04
  </div>

  <h2>10.6 Contextual Note: 2019 Archive Caveat vs. Ongoing Risk</h2>
  <p>The SQL backup header indicates that the dump was generated on <strong>2019-08-27</strong>. While current salaries and staffing may have evolved over subsequent years, South African National ID numbers and employee birth dates are permanent identifiers that do not expire. Leaving historical database dumps in public web directories represents an ongoing catastrophic compliance violation under POPIA.</p>
</div>

<div class="page-break">
  <!-- SECTION 11: CONSOLIDATED FINDINGS -->
  <h1>11. Consolidated Vulnerability Findings</h1>

  <h2>Finding F-01: Unauthorized Access to Confidential Patient Reports</h2>
  <table class="data-table">
    <tr><th style="width: 28%;">Attribute</th><th>Details</th></tr>
    <tr><td><strong>Finding ID &amp; Title</strong></td><td>F-01: Unauthorized Access to Confidential Patient Reports</td></tr>
    <tr><td><strong>Severity &amp; CVSS</strong></td><td><span class="badge badge-critical">CRITICAL</span> (Score: 9.1)</td></tr>
    <tr><td><strong>CVSS v3.1 Vector</strong></td><td>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N</td></tr>
    <tr><td><strong>CWE / OWASP Category</strong></td><td>CWE-89 (SQL Injection) / OWASP A03:2021-Injection</td></tr>
    <tr><td><strong>Affected Asset</strong></td><td><code>https://medirozahospital.com/patient/login.php</code></td></tr>
    <tr><td><strong>Associated Evidence</strong></td><td>M1-01, M1-02, M1-03, M2-03, M2-04, M2-05</td></tr>
  </table>
  <p><strong>Description:</strong> The patient login portal fails to sanitize or parameterize input supplied in the Username parameter. Injecting SQL comment sequences (<code>admin' -- </code>) prematurely truncates the SQL query logic, bypassing credential validation and granting an administrative session cookie to unauthenticated external users.</p>
  <p><strong>Remediation:</strong> Refactor authentication routines to implement parameterized queries (Prepared Statements) using PHP PDO or MySQLi. Discontinue dynamic SQL string concatenation entirely.</p>

  <h2>Finding F-02: Weak Password Protection on Confidential PDF Documents</h2>
  <table class="data-table">
    <tr><th style="width: 28%;">Attribute</th><th>Details</th></tr>
    <tr><td><strong>Finding ID &amp; Title</strong></td><td>F-02: Weak Password Protection on Confidential PDF Documents</td></tr>
    <tr><td><strong>Severity &amp; CVSS</strong></td><td><span class="badge badge-high">HIGH</span> (Score: 7.5)</td></tr>
    <tr><td><strong>CVSS v3.1 Vector</strong></td><td>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N</td></tr>
    <tr><td><strong>CWE / OWASP Category</strong></td><td>CWE-521 (Weak Passwords) / OWASP A02:2021-Cryptographic Failures</td></tr>
    <tr><td><strong>Affected Asset</strong></td><td>Mediroza CMS Laboratory Reporting Module (PDFs)</td></tr>
    <tr><td><strong>Associated Evidence</strong></td><td>M2-02, M2-03, M2-04, M2-05</td></tr>
  </table>
  <p><strong>Description:</strong> Patient laboratory reports are distributed using outdated Adobe Standard Encryption (Revision 3, 128-bit RC4) protected by weak, predictable user passphrases. A dictionary attack using John the Ripper and rockyou.txt successfully recovered all document passwords in under one second.</p>
  <p><strong>Remediation:</strong> Upgrade document cryptography to AES-256 (PDF Revision 6). Enforce minimum 16-character cryptographically random passphrases or transition to authenticated, in-portal viewing over TLS 1.3 without static-password downloadable PDFs.</p>

  <h2>Finding F-03: Publicly Accessible SQL Database Backup in Web Root</h2>
  <table class="data-table">
    <tr><th style="width: 28%;">Attribute</th><th>Details</th></tr>
    <tr><td><strong>Finding ID &amp; Title</strong></td><td>F-03: Publicly Accessible SQL Database Backup in Web Root</td></tr>
    <tr><td><strong>Severity &amp; CVSS</strong></td><td><span class="badge badge-critical">CRITICAL</span> (Score: 9.8)</td></tr>
    <tr><td><strong>CVSS v3.1 Vector</strong></td><td>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H</td></tr>
    <tr><td><strong>CWE / OWASP Category</strong></td><td>CWE-552 (Files in Web Root) / OWASP A05:2021-Security Misconfiguration</td></tr>
    <tr><td><strong>Affected Asset</strong></td><td><code>https://medirozahospital.com/old/mediroza_db_backup_2019.sql</code></td></tr>
    <tr><td><strong>Associated Evidence</strong></td><td>M2-01, M3-01, M3-02</td></tr>
  </table>
  <p><strong>Description:</strong> An unencrypted production MySQL database backup archive was left accessible within an unmapped web root directory (<code>/old</code>). The web server failed to enforce authentication or restrict access to <code>.sql</code> files, allowing any external internet user to download the full internal database dump.</p>
  <p><strong>Remediation:</strong> Immediately purge the <code>/old</code> directory from the web server. Configure web server rules to deny HTTP access to <code>.sql</code>, <code>.bak</code>, and archive extensions. Store automated backups in isolated, non-web-accessible off-site storage.</p>

  <h2>Finding F-04: Exposure of Employee Salary and Shareholder Information</h2>
  <table class="data-table">
    <tr><th style="width: 28%;">Attribute</th><th>Details</th></tr>
    <tr><td><strong>Finding ID &amp; Title</strong></td><td>F-04: Exposure of Employee Salary and Shareholder Information</td></tr>
    <tr><td><strong>Severity &amp; CVSS</strong></td><td><span class="badge badge-high">HIGH</span> (Score: 7.5)</td></tr>
    <tr><td><strong>CVSS v3.1 Vector</strong></td><td>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N</td></tr>
    <tr><td><strong>CWE / OWASP Category</strong></td><td>CWE-200 (Info Exposure) / OWASP A01:2021-Broken Access Control</td></tr>
    <tr><td><strong>Affected Asset</strong></td><td><code>mediroza_hr</code> Database Schema (<code>staff</code> &amp; <code>shareholders</code>)</td></tr>
    <tr><td><strong>Associated Evidence</strong></td><td>M3-01, M3-03, M3-04</td></tr>
  </table>
  <p><strong>Description:</strong> Directly resulting from the architectural failure identified in F-03, the exfiltrated database archive exposed confidential human resource payroll data (30 employees, ZAR 2,027,000 monthly payroll, National IDs, phones, emails) and complete proprietary shareholder equity capitalization records.</p>
  <p><strong>Remediation:</strong> Implement encryption at rest for all database tables containing PII and salary figures. Enforce strict least-privilege database user access controls and execute automated data retention policies to purge legacy backups.</p>
</div>

<div class="page-break">
  <!-- SECTION 12 & 13: RISK ASSESSMENT & REMEDIATION -->
  <h1>12. Risk Assessment</h1>
  <p>Risks were evaluated using CVSS v3.1 and mapped against organizational impact. Both F-01 and F-03 represent Critical risks requiring immediate intervention:</p>

  <table class="data-table">
    <tr><th>Impact Tier</th><th>High Likelihood</th><th>Medium Likelihood</th><th>Low Likelihood</th></tr>
    <tr><td><strong>Critical Impact</strong></td><td><strong>F-01</strong> (SQLi), <strong>F-03</strong> (Exposed Backup)</td><td>--</td><td>--</td></tr>
    <tr><td><strong>High Impact</strong></td><td><strong>F-02</strong> (Weak PDF Crypto), <strong>F-04</strong> (HR Exposure)</td><td>--</td><td>--</td></tr>
    <tr><td><strong>Medium Impact</strong></td><td>--</td><td>--</td><td>--</td></tr>
    <tr><td><strong>Low Impact</strong></td><td>--</td><td>--</td><td>--</td></tr>
  </table>

  <h1>13. Recommendations and Remediation</h1>
  <p>Remediation should follow a prioritized defense-in-depth framework:</p>
  
  <h2>Phase 1: Immediate Containment (Within 24 Hours)</h2>
  <ul>
    <li>Purge the <code>/old</code> directory from the production web server immediately.</li>
    <li>Implement web server configuration rules blocking access to <code>.sql</code>, <code>.bak</code>, and archive extensions.</li>
    <li>Temporarily patch <code>/patient/login.php</code> to eliminate SQL injection vulnerabilities.</li>
  </ul>

  <h2>Phase 2: Application Hardening (Within 7 Days)</h2>
  <ul>
    <li>Refactor patient authentication routines to implement Prepared Statements (PDO/MySQLi).</li>
    <li>Upgrade PDF generation module to AES-256 and strip metadata comments prior to distribution.</li>
    <li>Deploy ModSecurity WAF rules blocking SQL injection patterns and comment tokens.</li>
  </ul>

  <h2>Phase 3: Governance &amp; Compliance (Within 30 Days)</h2>
  <ul>
    <li>Establish automated off-site, encrypted database backup storage decoupled from web serving roots.</li>
    <li>Execute a formal POPIA Section 22 incident assessment to determine regulatory notification obligations.</li>
    <li>Institute recurring quarterly penetration testing and code security reviews.</li>
  </ul>

  <!-- SECTION 14: CONCLUSION -->
  <h1>14. Overall Conclusion</h1>
  <p>The penetration testing assessment of Mediroza General Hospital demonstrated that multiple critical security vulnerabilities compromise patient diagnostic confidentiality and hospital corporate records. By exploiting a straightforward SQL injection authentication bypass in the patient portal (M1), recovering weak PDF passwords and discovering metadata leaks (M2), and downloading an unauthenticated database backup (M3), full access was obtained to clinical pathology reports, 30 employee personnel records with monthly salaries totaling ZAR 2,027,000, and corporate shareholder equity structures.</p>
  <p>Implementing the phased remediation plan outlined in this report will enable Mediroza General Hospital to effectively neutralize these vulnerabilities, protect patient confidentiality, and achieve compliance with statutory data protection standards.</p>
</div>

<div class="page-break">
  <!-- SECTION 15: APPENDICES -->
  <h1>15. Appendices</h1>
  <h2>Appendix A: Assessment Tool Suite &amp; Versions</h2>
  <ul>
    <li><strong>Operating System:</strong> Kali Linux 2026.2 (Kernel 6.6+)</li>
    <li><strong>Reconnaissance Suite:</strong> DiG 9.20.30, Nmap 7.991, WhatWeb 0.5.5, cURL 8.8.0</li>
    <li><strong>Cryptanalysis Suite:</strong> John the Ripper 1.9.0-jumbo-1, pdf2john.pl, rockyou.txt</li>
    <li><strong>Forensics Suite:</strong> ExifTool 13.55, Poppler pdftotext 24.02.0, MariaDB Client 10.11</li>
  </ul>

  <h2>Appendix B: Standards &amp; Regulatory References</h2>
  <ul>
    <li><strong>OWASP Top 10 (2021):</strong> Open Web Application Security Project</li>
    <li><strong>CVSS v3.1:</strong> FIRST Common Vulnerability Scoring System</li>
    <li><strong>POPIA:</strong> Protection of Personal Information Act (Act No. 4 of 2013, Republic of South Africa)</li>
  </ul>

  <!-- SECTION 16: EVIDENCE REGISTER -->
  <h1>16. Evidence Register</h1>
  <table class="data-table">
    <tr><th>ID</th><th>Source Asset</th><th>Description</th><th style="text-align: center;">Finding</th><th style="text-align: center;">Status</th></tr>
    <tr><td><strong>RECON-01</strong></td><td>Recon/dns.txt</td><td>DNS query resolving target domain to 199.188.201.16</td><td style="text-align: center;">Info</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>RECON-02</strong></td><td>Recon/nmap.txt</td><td>Nmap scan identifying open ports 80/443 and HAProxy</td><td style="text-align: center;">Info</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>RECON-03</strong></td><td>Recon/whatweb.txt</td><td>WhatWeb fingerprinting LiteSpeed server &amp; 403 probe</td><td style="text-align: center;">Info</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>RECON-04</strong></td><td>Recon/headers.txt</td><td>cURL HTTP/2 response headers inspection (LiteSpeed)</td><td style="text-align: center;">Info</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>M1-01</strong></td><td>M1-01_login_bypass.png</td><td>Web login interface showing SQLi auth bypass payload</td><td style="text-align: center;">F-01</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M1-02</strong></td><td>M1-02_proof_of_bypass.png</td><td>Authenticated portal session exposing 3 locked reports</td><td style="text-align: center;">F-01</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M1-03</strong></td><td>M1/patient_report_*.pdf</td><td>Local CLI directory listing showing 3 downloaded PDFs</td><td style="text-align: center;">F-01</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>M2-01</strong></td><td>M2/all_reports_metadata.txt</td><td>ExifTool metadata inspection showing author j.malik &amp; leak</td><td style="text-align: center;">F-03</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>M2-02</strong></td><td>M2-02_password_cracking.png</td><td>John the Ripper dictionary attack on PDF hashes (redacted)</td><td style="text-align: center;">F-02</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M2-03</strong></td><td>M2-03_patient1.png</td><td>Decrypted pathology report for S. Dlamini (LR-2024-1187)</td><td style="text-align: center;">F-01, F-02</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M2-04</strong></td><td>M2-04_patient2.png</td><td>Decrypted pathology report for P. Reddy (LR-2024-1192)</td><td style="text-align: center;">F-01, F-02</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M2-05</strong></td><td>M2-05_patient3.png</td><td>Decrypted pathology report for E. Thompson (LR-2024-1205)</td><td style="text-align: center;">F-01, F-02</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M3-01</strong></td><td>M3-01_exposed_db.png</td><td>Direct browser access to SQL backup at /old/...</td><td style="text-align: center;">F-03, F-04</td><td style="text-align: center;"><span class="badge badge-verified">Verified</span></td></tr>
    <tr><td><strong>M3-02</strong></td><td>M3/backup_hash.txt</td><td>Cryptographic SHA-256 hash verification of SQL dump</td><td style="text-align: center;">F-03</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>M3-03</strong></td><td>M3/salary_statistics.txt</td><td>Local database import &amp; staff salary aggregation queries</td><td style="text-align: center;">F-04</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
    <tr><td><strong>M3-04</strong></td><td>M3/shareholder_details.txt</td><td>Local database shareholder distribution query results</td><td style="text-align: center;">F-04</td><td style="text-align: center;"><span class="badge badge-required">[REQ]</span></td></tr>
  </table>
</div>

</body>
</html>
"""

def generate_pdf():
    print("Writing temporary HTML template...")
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    
    print("Executing WeasyPrint...")
    cmd = [
        "weasyprint",
        f"--base-url={os.path.join(BASE_DIR, 'M4_Report')}",
        HTML_OUT,
        PDF_OUT
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"PDF successfully compiled to {PDF_OUT}")
        # Clean up temporary HTML
        if os.path.exists(HTML_OUT):
            os.remove(HTML_OUT)
    else:
        print(f"WeasyPrint failed (exit code {res.returncode}):")
        print(res.stderr)

if __name__ == "__main__":
    generate_pdf()
