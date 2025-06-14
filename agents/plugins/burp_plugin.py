# agents/plugins/burp_plugin.py

import requests
import logging
import configparser

logger = logging.getLogger("BurpPlugin")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class BurpPlugin:
    def __init__(self, config_path="config/burp.ini"):
        self.api_url = "http://localhost:1337"
        self.api_key = None
        self.load_config(config_path)

    def load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        self.api_url = config.get("Burp", "api_url", fallback=self.api_url)
        self.api_key = config.get("Burp", "api_key", fallback=self.api_key)
        logger.info(f"Burp API URL set to {self.api_url}")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get_scans(self):
        url = f"{self.api_url}/scans"
        try:
            r = requests.get(url, headers=self._headers(), timeout=15)
            r.raise_for_status()
            logger.info("Fetched scans list successfully")
            return r.json()
        except Exception as e:
            logger.error(f"Error fetching scans: {e}")
            return None

    def start_scan(self, target_url):
        url = f"{self.api_url}/scan"
        payload = {"url": target_url}
        try:
            r = requests.post(url, json=payload, headers=self._headers(), timeout=15)
            r.raise_for_status()
            logger.info(f"Started scan on {target_url}")
            return r.json()
        except Exception as e:
            logger.error(f"Error starting scan: {e}")
            return None

    def get_scan_status(self, scan_id):
        url = f"{self.api_url}/scan/{scan_id}/status"
        try:
            r = requests.get(url, headers=self._headers(), timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error(f"Error getting scan status: {e}")
            return None

if __name__ == "__main__":
    burp = BurpPlugin()
    scans = burp.get_scans()
    print(scans)
