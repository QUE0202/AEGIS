# agents/plugins/metasploit_plugin.py

import subprocess
import logging
import threading
import configparser
from queue import Queue, Empty

logger = logging.getLogger("MetasploitPlugin")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class MetasploitPlugin:
    def __init__(self, config_path="config/msf.ini"):
        self.msf_path = "msfconsole"
        self.load_config(config_path)

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.msf_path = config.get("Metasploit", "msfconsole_path", fallback=self.msf_path)
        logger.info(f"Loaded msfconsole path: {self.msf_path}")

    def run_command(self, command, timeout=60):
        """
        Run msfconsole command non-interactively.
        Returns stdout or error message.
        """
        try:
            cmd = [self.msf_path, "-q", "-x", command + "; exit"]
            logger.debug(f"Running command: {' '.join(cmd)}")
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            logger.debug("Command finished")
            return proc.stdout
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout expired for command: {command}")
            return "[!] Timeout expired."
        except Exception as e:
            logger.error(f"Exception: {e}")
            return f"[!] Error running msfconsole: {e}"

    def scan_with_auxiliary(self, target):
        logger.info(f"Starting auxiliary port scan on {target}")
        cmd = f"use auxiliary/scanner/portscan/tcp; set RHOSTS {target}; run"
        return self.run_command(cmd)

    def exploit(self, exploit_path, target):
        logger.info(f"Attempting exploit {exploit_path} on {target}")
        cmd = f"use {exploit_path}; set RHOST {target}; run"
        return self.run_command(cmd)

    def interactive_session(self):
        """
        Starts interactive msfconsole session (blocking).
        """
        try:
            subprocess.run([self.msf_path])
        except Exception as e:
            logger.error(f"Interactive session error: {e}")

if __name__ == "__main__":
    msf = MetasploitPlugin()
    output = msf.scan_with_auxiliary("192.168.1.1")
    print(output)
