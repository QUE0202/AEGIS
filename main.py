# main.py

import argparse
import sys
import os
from datetime import datetime

from agents.plugins.metasploit_plugin import MetasploitPlugin
from agents.plugins.nmap_plugin import NmapPlugin
from agents.plugins.burp_plugin import BurpPlugin

LOG_FOLDER = "reports"

def ensure_report_folder():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

def save_report(content: str):
    ensure_report_folder()
    now = datetime.now()
    filename = now.strftime("%d.%m.%Y %H.%M.%S") + ".md"
    path = os.path.join(LOG_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Report saved to {path}")

def red_team_mode(target):
    msf = MetasploitPlugin()
    nmap = NmapPlugin()

    print(f"[*] Running Red Team scan on {target}")

    # 1. Nmap scan
    xml_file = nmap.scan(target)
    nmap_result = ""
    if xml_file:
        summary = nmap.parse_xml(xml_file)
        if summary:
            nmap_result += f"# Nmap Scan Result for {target}\n\n"
            for host in summary:
                nmap_result += f"## Host: {host['address']} ({host['status']}) OS: {host['os']}\n"
                for p in host['ports']:
                    nmap_result += f"- {p['port']}/{p['protocol']} {p['state']} ({p['service']})\n"
                nmap_result += "\n"
        else:
            nmap_result = "Failed to parse Nmap XML output."
    else:
        nmap_result = "Nmap scan failed."

    # 2. Metasploit auxiliary scan
    msf_result = msf.scan_with_auxiliary(target)

    # Save combined report
    report_content = f"# AEGIS Red Team Report for {target}\n\n"
    report_content += nmap_result + "\n\n"
    report_content += "## Metasploit Auxiliary Scan Result\n\n"
    report_content += msf_result

    save_report(report_content)

def blue_team_mode(pcap_file=None, evtx_file=None, log_file=None):
    print("[*] Running Blue Team analysis")

    analysis = "# AEGIS Blue Team Report\n\n"

    if pcap_file:
        analysis += f"## PCAP File Analysis: {pcap_file}\n"
        # Tu wstaw parser PCAP - przykład prosty placeholder
        analysis += "Parsing PCAP not implemented yet.\n\n"

    if evtx_file:
        analysis += f"## EVTX File Analysis: {evtx_file}\n"
        # Tu wstaw parser EVTX - placeholder
        analysis += "Parsing EVTX not implemented yet.\n\n"

    if log_file:
        analysis += f"## Log File Analysis: {log_file}\n"
        # Tu prosty przykład: liczenie linii i podstawowa analiza
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            analysis += f"Log file contains {len(lines)} lines.\n\n"
        except Exception as e:
            analysis += f"Error reading log file: {e}\n\n"

    save_report(analysis)

def worm_mode(command=None, target=None):
    print("[*] Running Worm mode (testing only, no ethics)")

    # To jest uproszczony placeholder, gdzie można odpalić komendy bez limitów (tylko lokalnie!)
    if command and target:
        print(f"Executing worm command '{command}' on target '{target}'")
        # Tutaj wywołujemy exploit / payload z worm.py (który masz w swoim projekcie)
        # Przykład:
        # from agents.plugins.worm import WormPlugin
        # worm = WormPlugin()
        # output = worm.execute_command(command, target)
        # print(output)
        print("Worm mode execution is not implemented in this example.")
    else:
        print("Please provide --command and --target arguments for worm mode.")

def main():
    parser = argparse.ArgumentParser(description="AEGIS - Red/Blue Team Security Assistant")
    parser.add_argument("mode", choices=["red", "blue", "worm"], help="Choose mode of operation")
    parser.add_argument("--target", help="Target IP/Hostname for scanning or exploitation")
    parser.add_argument("--pcap", help="PCAP file path for Blue Team analysis")
    parser.add_argument("--evtx", help="EVTX file path for Blue Team analysis")
    parser.add_argument("--log", help="Log file path for Blue Team analysis")
    parser.add_argument("--command", help="Command to run in worm mode")

    args = parser.parse_args()

    if args.mode == "red":
        if not args.target:
            print("Error: --target is required in red mode")
            sys.exit(1)
        red_team_mode(args.target)

    elif args.mode == "blue":
        if not (args.pcap or args.evtx or args.log):
            print("Error: At least one of --pcap, --evtx or --log is required in blue mode")
            sys.exit(1)
        blue_team_mode(args.pcap, args.evtx, args.log)

    elif args.mode == "worm":
        worm_mode(args.command, args.target)

if __name__ == "__main__":
    main()
