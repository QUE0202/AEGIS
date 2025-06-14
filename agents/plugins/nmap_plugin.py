# agents/plugins/nmap_plugin.py

import subprocess
import xml.etree.ElementTree as ET
import logging
import threading
import queue
import configparser
import os

logger = logging.getLogger("NmapPlugin")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class NmapPlugin:
    def __init__(self, config_path="config/nmap.ini"):
        self.nmap_path = "nmap"
        self.load_config(config_path)

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.nmap_path = config.get("Nmap", "nmap_path", fallback=self.nmap_path)
        logger.info(f"Loaded nmap path: {self.nmap_path}")

    def scan(self, target, args="-sV -O", xml_output=None, timeout=120):
        """
        Run nmap scan with XML output asynchronously.
        Returns path to xml file or None if failed.
        """
        if xml_output is None:
            xml_output = f"scan_{target.replace('.', '_')}.xml"
        cmd = [self.nmap_path] + args.split() + ["-oX", xml_output, target]

        def run_scan(q):
            try:
                logger.info(f"Running nmap scan on {target} with args '{args}'")
                subprocess.run(cmd, check=True)
                q.put(xml_output)
                logger.info(f"Scan finished, output saved to {xml_output}")
            except Exception as e:
                logger.error(f"Nmap scan error: {e}")
                q.put(None)

        q = queue.Queue()
        t = threading.Thread(target=run_scan, args=(q,))
        t.start()
        t.join(timeout)
        try:
            result = q.get_nowait()
        except queue.Empty:
            logger.error("Nmap scan thread timed out")
            result = None
        return result

    def parse_xml(self, xml_file):
        """
        Parse nmap XML and return a detailed summary.
        """
        if not os.path.isfile(xml_file):
            logger.error(f"XML file {xml_file} not found")
            return None

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            hosts_summary = []
            for host in root.findall("host"):
                addr = host.find("address").attrib.get("addr")
                status = host.find("status").attrib.get("state")
                ports = []
                ports_element = host.find("ports")
                if ports_element is not None:
                    for port in ports_element.findall("port"):
                        portid = port.attrib.get("portid")
                        protocol = port.attrib.get("protocol")
                        state = port.find("state").attrib.get("state")
                        service_el = port.find("service")
                        service = service_el.attrib.get("name") if service_el is not None else "unknown"
                        ports.append({
                            "port": portid,
                            "protocol": protocol,
                            "state": state,
                            "service": service
                        })

                os_el = host.find("os")
                os_match = None
                if os_el is not None:
                    os_matches = os_el.findall("osmatch")
                    if os_matches:
                        os_match = os_matches[0].attrib.get("name")

                hosts_summary.append({
                    "address": addr,
                    "status": status,
                    "os": os_match,
                    "ports": ports
                })
            return hosts_summary

        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
            return None

if __name__ == "__main__":
    np = NmapPlugin()
    xml_file = np.scan("127.0.0.1")
    if xml_file:
        summary = np.parse_xml(xml_file)
        print(summary)
