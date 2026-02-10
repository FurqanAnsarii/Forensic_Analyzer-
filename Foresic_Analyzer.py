import os
import sys
import hashlib
import subprocess
import re
import binascii
from datetime import datetime

# Ultra Pro Max UI Colors - Furqan Ansari Edition
class Colors:
    R = '\033[91m' # Red
    G = '\033[92m' # Green
    Y = '\033[93m' # Yellow
    B = '\033[94m' # Blue
    M = '\033[95m' # Magenta
    C = '\033[96m' # Cyan
    W = '\033[97m' # White
    END = '\033[0m'
    BOLD = '\033[1m'

class SentinelForensics:
    def __init__(self, target):
        self.target = target
        self.author = "Furqan Ansari"
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report = f"SENTINEL_REPORT_{self.timestamp}.log"

    def banner(self):
        os.system('clear')
        print(f"{Colors.C}{'='*75}")
        print(f"{Colors.BOLD}{Colors.W}   MADE BY: {self.author.upper()}")
        print(f"{Colors.BOLD}{Colors.B}   SYNDICATE ABABIL - THE SENTINEL (UNIVERSAL FORENSIC ENGINE)")
        print(f"{Colors.BOLD}{Colors.R}   WARNING: PRIVATE SCRIPT - DO NOT SHARE WITHOUT CREDIT")
        print(f"{Colors.C}{'='*75}{Colors.END}")

    def get_magic_type(self):
        """File ke asli DNA (Magic Bytes) ko pehchanna."""
        try:
            with open(self.target, 'rb') as f:
                header = f.read(16)
                hex_head = binascii.hexlify(header).upper().decode()
                
                signatures = {
                    "7F454C46": "ELF Binary (Linux Executable)",
                    "89504E47": "PNG Image",
                    "FFD8FF": "JPEG Image",
                    "D4C3B2A1": "PCAP Network Capture (LE)",
                    "A1B2C3D4": "PCAP Network Capture (BE)",
                    "504B0304": "ZIP/Office Document",
                    "25504446": "PDF Document",
                    "4D5A": "PE Executable (Windows EXE/DLL)"
                }
                
                for sig, desc in signatures.items():
                    if hex_head.startswith(sig):
                        return desc
            return "Unknown / Generic Data"
        except: return "Error reading file signature"

    def network_scan(self):
        """Deep PCAP Analysis."""
        print(f"{Colors.Y}[*] Analyzing Network Traffic...{Colors.END}")
        try:
            cmd = f"tcpdump -r {self.target} -n | head -n 15"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return res.stdout if res.stdout else "No standard PCAP traffic found."
        except: return "Network tools (tcpdump) missing."

    def run(self):
        self.banner()
        if not os.path.exists(self.target):
            print(f"{Colors.R}[!] Error: Target file '{self.target}' not found!{Colors.END}")
            return

        # 1. Identity & Hashing
        print(f"{Colors.C}[*] Extracting Core Evidence...{Colors.END}")
        sha256 = hashlib.sha256(open(self.target,'rb').read()).hexdigest()
        m_type = self.get_magic_type()
        
        print(f"{Colors.G}[+] IDENTIFIED AS: {Colors.W}{m_type}")
        print(f"{Colors.G}[+] SHA256 HASH  : {Colors.W}{sha256}")

        # 2. Forensic Logic
        final_data = ""
        if "PCAP" in m_type:
            final_data = self.network_scan()
        else:
            print(f"{Colors.G}[+] Running Global String & Artifact Extraction...")
            cmd = f"strings {self.target} | grep -E 'http|https|[0-9]{{1,3}}\.[0-9]{{1,3}}' | sort -u | head -n 20"
            final_data = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

        # Result Display
        print(f"\n{Colors.M}[ LOGGED ARTIFACTS ]{Colors.END}")
        print(final_data if final_data else "No significant artifacts found.")

        # Save Private Report
        with open(self.report, "w") as f:
            f.write(f"MADE BY: {self.author}\n")
            f.write(f"SENTINEL FORENSIC ANALYSIS - {datetime.now()}\n")
            f.write(f"{'='*40}\nTARGET: {self.target}\nTYPE: {m_type}\nHASH: {sha256}\n\nDATA:\n{final_data}")

        print(f"\n{Colors.C}{'='*75}")
        print(f"{Colors.BOLD}{Colors.G}[✔] MISSION SUCCESS! PRIVATE REPORT: {self.report}")
        print(f"{Colors.C}{'='*75}{Colors.END}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Colors.R}Usage: python3 sentinel.py <file_path>{Colors.END}")
    else:
        engine = SentinelForensics(sys.argv[1])
        engine.run()
