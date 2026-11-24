# Networkwalks Cybersecurity Internship

[![Internship](https://img.shields.io/badge/Internship-Networkwalks-blue?logo=cisco&logoColor=white)](https://github.com/Ritzz-09/Networkwalks-Internship)
[![Author](https://img.shields.io/badge/Author-Rithish_S_P-black?logo=github)](https://github.com/Ritzz-09)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#internship-modules)
[![Workstation](https://img.shields.io/badge/Workstation-Lenovo_IdeaPad_Slim_3_i5--13420H-blue)](week1/#1-host-machine-specifications)

This repository serves as the official portfolio and technical documentation for the **Networkwalks Cybersecurity Internship**. It contains hands-on laboratory setups, technical configurations, network topology models, verification tests, and security assessments completed across each weekly project module.

---

## 📚 Internship Modules

| Week | Project Module & Topic | Environment & Focus | Documentation Link | Status |
|:---:|---|---|:---:|:---:|
| **Week 1** | **Cybersecurity Laboratory Environment Setup** | Oracle VirtualBox, Kali Linux, NAT Network (`10.0.0.0/24`), Routing, ICMP & DNS Verification | [📁 Week 1 Documentation](week1/) | ✅ Completed |
| **Week 2** | **Information Gathering, Footprinting & Network Scanning** | OSINT, WHOIS, WhatWeb, nslookup, cURL, WAFW00F, DNSRecon, Zenmap / Nmap (`192.168.1.0/24`) | [📁 Week 2 Documentation](week2/) | ✅ Completed |
| **Week 3** | **Password Cracking, Hash Extraction & Cryptanalysis** | John the Ripper (JTR), RockYou wordlist, PDF Hash Extraction (`$pdf$4*4*128*...`), Networkwalks Online Tools | [📁 Week 3 Documentation](week3/) | ✅ Completed |
| **Week 4** | **Web Application Penetration Testing & Forensic Assessment** | Black-box Pentest, SQL Injection Auth Bypass, Cryptanalysis, ExifTool Metadata Leaks, MySQL Dump Analysis, Professional Report | [📁 Week 4 Documentation](week4/) | ✅ Completed |

---

## 🚀 Quick Navigation

### [Week 1: Cybersecurity Laboratory Environment Setup](week1/)

* **Host Machine:** Lenovo IdeaPad Slim 3 15IRH10 (Model 83K1), 13th Gen Intel Core i5-13420H (2.10 GHz), 16.0 GB RAM, Windows 11 Home Single Language
* **Virtualization:** Oracle VirtualBox 7.2.22
* **Security Workstation:** Kali Linux 2026.2 (amd64)
* **Network Mode:** Isolated NAT Network (`Cyberlab-NAT`) on `10.0.0.0/24`
* **Routing:** Virtual Gateway `10.0.0.1`, Initial dynamic DHCP baseline (`10.0.0.3`), Static addressing (`10.0.0.2/24`)
* **Automation Suite:** `verify_lab.sh`, `troubleshoot_network.sh`, `configure_static_ip.sh`
* **Verification Milestones:** Desktop deployment, adapter configuration, baseline routing, static IP configuration, gateway ICMP reachability, outbound Internet connectivity, and DNS resolution.

👉 **Read the full module runbook and evidence report:** [**week1/README.md**](week1/)

### [Week 2: Information Gathering, Footprinting & Network Scanning](week2/)

* **External Target:** `networkwalks.com` (Resolved IP: `192.232.216.135`)
* **Internal Subnet:** `192.168.1.0/24` (Gateway: `192.168.1.1` - Syrotech Networks)
* **Reconnaissance Modules:**
  * **PM1 — Web Application & Domain Footprinting:** WHOIS, WhatWeb, nslookup, cURL, WAFW00F, and DNSRecon (Identified WordPress 7.1.4, Apache, ModSecurity WAF, BIND nameservers, MX/SPF/SRV records).
  * **PM5 — Zenmap Network Scanning:** Ping sweep (`nmap -sn 192.168.1.0/24`), 8 live hosts discovered, Layer 2 MAC resolution, radial topology graph generation, and ARP mitigation analysis.
* **Automation Suite:** `ping_sweep.sh` (Automated LAN discovery and ARP resolution tool).
* **Formal Submission Deliverables:**
  * 📄 [**Week2-Final-Report.docx**](week2/final-report/Week2-Final-Report.docx) — Formatted Microsoft Word Technical Report
  * 📑 [**Week2-Final-Report.pdf**](week2/final-report/Week2-Final-Report.pdf) — Print-ready 11-page publication-grade PDF report
  * 📝 [**Week2-Final-Report.md**](week2/final-report/Week2-Final-Report.md) — Source Technical Report in Markdown

👉 **Read the full module runbook and evidence report:** [**week2/README.md**](week2/)

### [Week 3: Password Cracking, Hash Extraction & Cryptanalysis](week3/)

* **Target Documents:** Encrypted PDF archives (`My Locked PDF1.pdf`, `My Locked PDF1 (for NW Tools Lab WK3-PM2).pdf`)
* **Encryption Format:** PDF Revision 4, 128-bit key length (`$pdf$4*4*128*...`)
* **Cryptanalysis Modules:**
  * **PM1 — Password Cracking with John the Ripper (JTR):** Extracted hash targeting `hash1.txt`, dictionary attack executed using `/usr/share/wordlists/rockyou.txt` on Kali Linux. Password cracked: `good-luck`. Flag captured: `nw{cybersecurity_flag_captured_2608}`.
  * **PM2 — Password Cracking with Networkwalks Web Tools:** Extracted `$pdf$` hash via Networkwalks online Hash Calculator, dictionary attack performed via Networkwalks Password Cracker suite. Password cracked: `password1`. Flag captured: `nw{networkwalks_flag1_jtr_270521_1}`.
* **Captured Flags:**
  * 🚩 Flag 1: `nw{cybersecurity_flag_captured_2608}`
  * 🚩 Flag 2: `nw{networkwalks_flag1_jtr_270521_1}`

👉 **Read the full module runbook and evidence report:** [**week3/README.md**](week3/)

### [Week 4: Web Application Penetration Testing & Forensic Assessment (Mediroza General Hospital)](week4/)

* **Target Organization:** Mediroza General Hospital (14 Cedar Avenue, Johannesburg, South Africa)
* **Target Domain:** `https://medirozahospital.com` (Resolved Host IP: `199.188.201.16` / `server274-1.web-hosting.com`)
* **Engagement Milestones:**
  * **Reconnaissance:** DNS A-record enumeration (`dig`), Nmap port 80/443 detection (HAProxy 2.0.0+), WhatWeb LiteSpeed fingerprinting, and HTTP/2 header inspection.
  * **M1 — Initial Access:** Identified patient login portal (`/patient/login.php`), executed SQL Injection authentication bypass (`admin' -- `), accessed portal dashboard (`/patient/portal.php`), and exfiltrated 3 locked patient pathology reports.
  * **M2 — Cryptanalysis & Forensics:** Analyzed 128-bit RC4 PDF encryption, executed offline dictionary attack with John the Ripper (`rockyou.txt`) cracking all 3 passwords in under 1 second, unlocked diagnostic reports, and extracted ExifTool metadata revealing comment leak by IT Admin `j.malik` referencing `/old`.
  * **M3 — Critical Data Exposure:** Discovered publicly accessible database dump at `https://medirozahospital.com/old/mediroza_db_backup_2019.sql`, parsed `mediroza_hr` schema, extracted records for 30 employees (National IDs, salaries totaling ZAR 2,027,000/mo), and mapped 10 corporate shareholders (1,000,000 shares).
  * **M4 — Professional Reporting & Remediation:** Authored formal 21-page publication-grade PDF and DOCX penetration testing reports, Excel evidence register, missing evidence checklist, and executive summary.
* **Formal Submission Deliverables:**
  * 📄 [**Mediroza_Penetration_Test_Report.docx**](week4/M4_Report/Mediroza_Penetration_Test_Report.docx) — Formatted Microsoft Word Consulting Report (1.0 MB)
  * 📑 [**Mediroza_Penetration_Test_Report.pdf**](week4/M4_Report/Mediroza_Penetration_Test_Report.pdf) — Print-ready 21-page WeasyPrint Publication PDF (1.1 MB)
  * 📊 [**Evidence_Register.xlsx**](week4/M4_Report/Evidence_Register.xlsx) — Three-sheet Excel Evidence Cross-Reference Register
  * 📋 [**Missing_Evidence_Checklist.txt**](week4/M4_Report/Missing_Evidence_Checklist.txt) — Evidence Inventory Gap Audit
  * 📝 [**Report_Summary.txt**](week4/M4_Report/Report_Summary.txt) — High-Level Executive Debriefing Document

👉 **Read the full module runbook and evidence report:** [**week4/README.md**](week4/)

---

## 📂 Repository Structure

```
Networkwalks-Internship/
├── README.md                                     # Main repository overview & syllabus
├── week1/                                        # Week 1: Cybersecurity Lab Environment Setup
│   ├── README.md                                 # Week 1 technical report & operational runbook
│   ├── verify_lab.sh                             # Automated 5-point verification test suite
│   ├── troubleshoot_network.sh                   # Network diagnostic & auto-remediation tool
│   ├── configure_static_ip.sh                    # Static IP & persistent gateway configuration script
│   └── images/                                   # Empirical screenshots & network diagrams
│       ├── kali-linux-desktop.png                # Kali Linux desktop interface
│       ├── network-topology.png                  # Lab network topology infographic
│       ├── nat-network-configuration.png         # Cyberlab-NAT (10.0.0.0/24) configuration
│       ├── virtualbox-adapter-configuration.png  # VM Adapter 1 attached to Cyberlab-NAT
│       ├── initial-routing-table.png             # Initial routing table & DHCP baseline
│       ├── kali-ip-address.png                   # Static IP configuration (10.0.0.2/24) on eth0
│       ├── default-gateway.png                   # Default gateway (10.0.0.1) routing verification
│       ├── ping-gateway.png                      # Gateway (10.0.0.1) & Internet (8.8.8.8) ping tests
│       ├── ping-internet.png                     # Kernel route persistence & reachability
│       └── virtualbox-default-nat.png            # Default NAT reference (troubleshooting)
├── week2/                                        # Week 2: Information Gathering & Network Scanning
    ├── README.md                                 # Master Week 2 report & operational runbook
    ├── final-report/                             # Week 2 Formal Technical Report Deliverables
    │   ├── Week2-Final-Report.docx               # Formatted Word Document Report
    │   ├── Week2-Final-Report.pdf                # Print-Ready 11-Page PDF Technical Report
    │   └── Week2-Final-Report.md                 # Complete Markdown Report Source
    ├── PM1-footprinting/                         # Passive & active OSINT footprinting suite
    │   ├── tool1-whois/                          # WHOIS domain registration intelligence
    │   │   ├── whois-output.txt                  # Raw WHOIS query response
    │   │   └── whois.png                         # CLI execution screenshot
    │   ├── tool2-whatweb/                        # Web technology stack fingerprinting
    │   │   ├── whatweb-output.txt                # CMS, server & component details
    │   │   └── whatweb.png                       # CLI execution screenshot
    │   ├── tool3-nslookup/                       # DNS address resolution
    │   │   ├── nslookup-output.txt               # DNS A-record query result
    │   │   └── nslookup.png                      # CLI execution screenshot
    │   ├── tool4-curl/                           # HTTP response header analysis
    │   │   ├── curl-output.txt                   # HTTP headers & cookie inspection
    │   │   └── curl.png                          # CLI execution screenshot
    │   ├── tool5-waf/                            # Web Application Firewall detection
    │   │   ├── waf-output.txt                    # WAFW00F ModSecurity detection output
    │   │   └── waf.png                           # CLI execution screenshot
    │   └── tool6-dnsrecon/                       # DNS zone & service enumeration
    │       ├── dnsrecon-output.txt               # SOA, NS, MX, TXT, and SRV records
    │       └── dnsrecon.png                      # CLI execution screenshot
    └── PM5-zenmap-network-scanning/              # LAN host discovery & topology mapping
        ├── README.md                             # PM5 dedicated module report
        ├── zenmap-ping-scan-output.txt           # Formatted Nmap ping sweep log (8 hosts)
        ├── scripts/
        │   └── ping_sweep.sh                     # Automated LAN ping sweep & ARP tool
        ├── reports/
        │   ├── PM5_Task_Answers_and_Evidence_RITHISH_SP.pdf # Practical answers & evidence PDF
        │   └── topology.pdf                      # Exported Zenmap vector topology PDF
        └── images/
            ├── evidence-1-ping-scan-overview.png # Zenmap ping sweep target & output
            ├── evidence-2-scan-summary.png       # Execution metrics & host count
            ├── evidence-3-localhost-selection.png# Selected localhost (192.168.1.36) view
            ├── evidence-4-topology-layout.png    # Initial topology graph layout
            ├── evidence-5-topology-detail.png    # Adjusted ring topology graph
            └── topology-diagram.png              # High-resolution rendered topology map
└── week3/                                        # Week 3: Password Cracking & Cryptanalysis
    ├── README.md                                 # Master Week 3 technical report & lab guide
    ├── PM1- password cracking with JTR/          # Module PM1: Offline cryptanalysis with JTR
    │   ├── flag.txt                              # Captured CTF flag 1 (nw{cybersecurity_flag_captured_2608})
    │   ├── hash1.txt                             # Extracted PDF crackable hash ($pdf$4*4*128*...)
    │   ├── cracked pdf.png                       # Evidence: Unlocked PDF with flag display
    │   └── password cracked with JTR.png         # Evidence: JTR dictionary attack completion
    └── PM2- password cracking with nw tools/     # Module PM2: Online cryptanalysis with NW tools
        ├── flag.txt                              # Captured CTF flag 2 (nw{networkwalks_flag1_jtr_270521_1})
        ├── hash2.txt                             # Extracted PDF crackable hash
        ├── hash-calculator.png                   # Evidence: Networkwalks hash extraction
        ├── password-cracker.png                  # Evidence: Web dictionary attack match
        └── opened pdf.png                        # Evidence: Unlocked PDF with flag display
└── week4/                                        # Week 4: Mediroza Penetration Test & Forensics
    ├── README.md                                 # Master Mediroza report & operational runbook
    ├── Recon/                                    # Target reconnaissance & service enumeration logs
    ├── M1/                                       # Milestone 1: Initial access & SQLi login bypass
    ├── M2/                                       # Milestone 2: PDF hash cracking & metadata forensics
    ├── M3/                                       # Milestone 3: Exposed MySQL backup & salary analysis
    ├── Screenshots/                              # Original unedited empirical evidence captures
    ├── scripts/                                  # Report generation & redaction automation suite
    └── M4_Report/                                # Formal Week 4 Technical Submission Deliverables
        ├── Mediroza_Penetration_Test_Report.docx # Formatted Word Document Report (1.0 MB)
        ├── Mediroza_Penetration_Test_Report.pdf  # Publication-Grade 21-Page PDF Report (1.1 MB)
        ├── Mediroza_Penetration_Test_Report.md   # Source Technical Report in Markdown
        ├── Evidence_Register.xlsx                # Formatted Excel Cross-Reference Register
        ├── Missing_Evidence_Checklist.txt        # Evidence Gap Audit & Placeholder Register
        └── Report_Summary.txt                    # Executive Debriefing & Remediation Roadmap
```

---

## 👤 Author

**Rithish S P**  
* GitHub: [@Ritzz-09](https://github.com/Ritzz-09)
* Repository: [Networkwalks-Internship](https://github.com/Ritzz-09/Networkwalks-Internship)
