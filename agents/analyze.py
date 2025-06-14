# agents/analyze.py

import os
import subprocess
from datetime import datetime
from core.llm_interface import ask_llm

ANALYZE_PROMPT = """
You are a cybersecurity forensic analyst.
You help analyze logs, network captures, and system events to identify potential security threats or unusual behavior.

Based on the data provided, explain any suspicious entries, anomalies, or indicators of compromise (IoC). Provide context and recommended follow-up actions.

Keep it short and practical. Focus on forensic clarity.
"""

SUPPORTED_TYPES = {
    ".pcap": "PCAP (Network Traffic Capture)",
    ".evtx": "Windows Event Log",
    ".log": "Plaintext Log File"
}

REPORTS_DIR = "reports"

def parse_evtx(file_path):
    try:
        from Evtx.Evtx import Evtx
        from xml.etree import ElementTree as ET

        records = []
        with Evtx(file_path) as log:
            for record in log.records():
                xml_str = record.xml()
                try:
                    root = ET.fromstring(xml_str)
                    timestamp = root.findtext(".//TimeCreated")
                    msg = root.findtext(".//Data")
                    records.append(f"[{timestamp}] {msg}")
                except:
                    continue
        return "\n".join(records[-50:])  # Only last 50 for brevity

    except ImportError:
        return "[!] python-evtx not installed. Run: pip install python-evtx"

def classify_lines(lines):
    """
    Very simple classification by keywords.
    Returns dict of {classification: [lines]}
    """
    categories = {
        "Failed Login": [],
        "Error": [],
        "Suspicious": [],
        "Info": []
    }

    for line in lines:
        lower = line.lower()
        if any(x in lower for x in ["failed login", "authentication failure", "login failed", "invalid user"]):
            categories["Failed Login"].append(line)
        elif any(x in lower for x in ["error", "fail", "denied", "unauthorized"]):
            categories["Error"].append(line)
        elif any(x in lower for x in ["suspicious", "malware", "attack", "exploit", "ransomware", "trojan"]):
            categories["Suspicious"].append(line)
        else:
            categories["Info"].append(line)
    return categories

def save_report(file_path, analysis_text, classified_lines):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    base_name = os.path.basename(file_path)
    report_name = f"{timestamp} - {base_name}.md"
    report_path = os.path.join(REPORTS_DIR, report_name)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Analysis Report for `{base_name}`\n")
        f.write(f"**Generated on:** {timestamp}\n\n")
        f.write("## AI Analysis Summary\n")
        f.write(analysis_text + "\n\n")

        f.write("## Classified Log Entries\n")
        for category, lines in classified_lines.items():
            f.write(f"### {category} ({len(lines)})\n")
            if lines:
                for line in lines[:20]:  # max 20 lines per category to avoid huge reports
                    f.write(f"- {line.strip()}\n")
            else:
                f.write("- None found\n")
            f.write("\n")

    print(f"[+] Report saved: {report_path}")

def analyze_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    print(f"[*] Analyzing: {file_path} [{SUPPORTED_TYPES.get(ext, 'Unknown Format')}]")

    if not os.path.isfile(file_path):
        print("[!] File not found.")
        return

    try:
        if ext == ".pcap":
            result = subprocess.run(
                ["tshark", "-r", file_path, "-q", "-z", "io,phs"],
                capture_output=True,
                text=True
            )
            data = result.stdout or "[No summary data returned from tshark.]"
            lines = data.splitlines()

        elif ext == ".evtx":
            print("[*] Parsing EVTX file...")
            data = parse_evtx(file_path)
            lines = data.splitlines()

        elif ext == ".log":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[-100:]
            data = "".join(lines)

        else:
            print("[!] Unsupported file type.")
            return

        print("\n[>] Sending file excerpt to AI for analysis...\n")
        analysis_response = ask_llm(f"Analyze the following content:\n\n{data}", system_prompt=ANALYZE_PROMPT)
        print(analysis_response)

        classified = classify_lines(lines)
        save_report(file_path, analysis_response, classified)

    except Exception as e:
        print(f"[!] Error during analysis: {e}")
