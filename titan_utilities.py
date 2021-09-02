from typing import List, Dict
import requests
import requests.packages.urllib3
from requests import Response
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import quote


class TitanUtilities:
    def __init__(self, config):
        self.config = config
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.session = requests.Session()
        self.session.auth = (self.config.titan_username, self.config.titan_api_key)
        if self.config.titan_user_agent:
            self.session.headers = {"User-Agent": self.config.titan_user_agent}

    def get_bph_tracking_reports(self) -> List:
        self.config.logger.info("Attempting to acquire BPH tracking reports.")
        url: str = "{}/reports?sort=latest&count={}&reportTag={}".format(
            self.config.titan_api_base_url.rstrip('/'), self.config.titan_api_batch_size, quote(self.config.bph_tracking_tag))
        try:
            result = self._fetch_reports(url)
        except Exception as e:
            self.config.logger.error("Unable to get BPH tracking reports from Titan: %s", {e})
            return []
        else:
            reports = result.json()["reports"]
            self.config.logger.info("%s BPH tracking reports acquired.", len(reports))
            return reports

    def get_bph_tracking_report(self, uid: str) -> Dict:
        self.config.logger.info("Attempting to acquire BPH tracking report.")
        url: str = "{}/reports/{}".format(self.config.titan_api_base_url.rstrip('/'), uid)
        try:
            result = self._fetch_reports(url)
        except Exception as e:
            self.config.logger.error("Unable to get BPH tracking report from Titan: %s", {e})
            return {}
        else:
            self.config.logger.info("Acquired BPH tracking report.")
            return result.json()

    def get_bph_tracking_report_attachment(self, url: str) -> str:
        self.config.logger.info("Attempting to acquire BPH tracking report attachment.")
        try:
            result = self._fetch_reports(url)
        except Exception as e:
            self.config.logger.error("Unable to get BPH tracking report attachment from Titan: %s", {e})
            return ""
        else:
            self.config.logger.info("Acquired BPH tracking report attachment.")
            return result.text.strip()

    def _fetch_reports(self, url) -> Response:
        self.config.logger.info(f"Sending request: {url}")
        response = self.session.get(url)
        response.raise_for_status()
        return response
