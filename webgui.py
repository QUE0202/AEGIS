import gradio as gr
from agents.plugins.metasploit_plugin import MetasploitPlugin
from agents.plugins.nmap_plugin import NmapPlugin
from agents.plugins.burp_plugin import BurpPlugin

msf = MetasploitPlugin()
nmap = NmapPlugin()
burp = BurpPlugin()

def run_msf_scan(target):
    output = msf.scan_with_auxiliary(target)
    return output

def run_msf_exploit(module, target):
    output = msf.exploit(module, target)
    return output

def run_nmap_scan(target):
    xml_file = nmap.scan(target)
    if xml_file:
        summary = nmap.parse_xml(xml_file)
        if summary:
            text = ""
            for host in summary:
                text += f"Host: {host['address']} ({host['status']}) OS: {host['os']}\n"
                for p in host['ports']:
                    text += f" - {p['port']}/{p['protocol']} {p['state']} ({p['service']})\n"
                text += "\n"
            return text
    return "Nmap scan failed."

def get_burp_scans():
    scans = burp.get_scans()
    if scans:
        return str(scans)
    return "Failed to fetch Burp scans."

def start_burp_scan(target_url):
    result = burp.start_scan(target_url)
    if result:
        return str(result)
    return "Failed to start Burp scan."

with gr.Blocks() as demo:
    gr.Markdown("# AEGIS Web GUI")

    with gr.Tab("Metasploit"):
        target = gr.Textbox(label="Target IP/Hostname")
        msf_scan_btn = gr.Button("Run Auxiliary Scan")
        msf_exploit_module = gr.Textbox(label="Exploit Module (e.g. exploit/windows/smb/ms17_010_eternalblue)")
        msf_exploit_target = gr.Textbox(label="Exploit Target IP")
        msf_scan_output = gr.Textbox(label="Scan Output", lines=10)
        msf_exploit_output = gr.Textbox(label="Exploit Output", lines=10)

        msf_scan_btn.click(run_msf_scan, inputs=target, outputs=msf_scan_output)
        gr.Button("Run Exploit").click(run_msf_exploit, inputs=[msf_exploit_module, msf_exploit_target], outputs=msf_exploit_output)

    with gr.Tab("Nmap"):
        nmap_target = gr.Textbox(label="Target IP/Hostname")
        nmap_scan_btn = gr.Button("Run Nmap Scan")
        nmap_output = gr.Textbox(label="Nmap Scan Result", lines=15)

        nmap_scan_btn.click(run_nmap_scan, inputs=nmap_target, outputs=nmap_output)

    with gr.Tab("Burp Suite"):
        burp_scan_list_btn = gr.Button("Get Scan List")
        burp_scan_list_output = gr.Textbox(label="Scan List", lines=10)
        burp_scan_target = gr.Textbox(label="Target URL for Scan")
        burp_start_scan_btn = gr.Button("Start Burp Scan")
        burp_start_scan_output = gr.Textbox(label="Start Scan Output", lines=10)

        burp_scan_list_btn.click(get_burp_scans, outputs=burp_scan_list_output)
        burp_start_scan_btn.click(start_burp_scan, inputs=burp_scan_target, outputs=burp_start_scan_output)

if __name__ == "__main__":
    demo.launch()
