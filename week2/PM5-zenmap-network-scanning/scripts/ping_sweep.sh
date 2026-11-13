#!/bin/bash
# ==============================================================================
# Networkwalks Cybersecurity Internship - Week 2
# Module: PM5 - Zenmap Network Scanning
# Script: ping_sweep.sh (Automated LAN Host Discovery & MAC Resolution)
# Author: Rithish S P (@Ritzz-09)
# ==============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

TARGET_SUBNET="${1:-192.168.1.0/24}"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}   NETWORKWALKS INTERNSHIP — WEEK 2 LAN DISCOVERY SUITE                ${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "Author        : Rithish S P (@Ritzz-09)"
echo -e "Module        : PM5 Zenmap Network Scanning"
echo -e "Target Subnet : ${CYAN}${TARGET_SUBNET}${NC}"
echo -e "Scan Profile  : Ping Scan (-sn ICMP Echo / ARP Request)"
echo -e "Date/Time     : $(date)"
echo -e "${BLUE}----------------------------------------------------------------------${NC}"
echo ""

if command -v nmap &>/dev/null; then
    echo -e "${YELLOW}[*] Executing Nmap Ping Sweep across ${TARGET_SUBNET}...${NC}"
    echo ""
    nmap -sn "${TARGET_SUBNET}"
else
    echo -e "${YELLOW}[!] Nmap not detected. Falling back to native ARP / ping sweep...${NC}"
    BASE_IP=$(echo "${TARGET_SUBNET}" | cut -d'/' -f1 | cut -d'.' -f1-3)
    echo -e "${CYAN}[*] Scanning range ${BASE_IP}.1 to ${BASE_IP}.254...${NC}"
    
    for i in $(seq 1 254); do
        (
            if ping -c 1 -W 1 "${BASE_IP}.${i}" &>/dev/null; then
                MAC=$(ip neigh show "${BASE_IP}.${i}" 2>/dev/null | awk '{print $5}')
                [ -z "$MAC" ] && MAC="Local / Gateway"
                echo -e "${GREEN}[+] Host UP:${NC} ${BASE_IP}.${i} \t MAC: ${MAC}"
            fi
        ) &
    done
    wait
fi

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}[✓] Scan sweep completed successfully.${NC}"
echo -e "${BLUE}======================================================================${NC}"
