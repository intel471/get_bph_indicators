#!/usr/bin/env python3.8


from typing import List, Dict
import requests
import requests.packages.urllib3
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import quote


class TitanUtilities:
    def __init__(self, config):
        self.config = config
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def get_bph_tracking_reports(self) -> List:
        reports: List = []

        try:
            self.config.logger.info("Attempting to acquire BPH tracking reports.")

            count: int = self.config.titan_api_batch_size

            request: str = self.config.titan_api_base_url + "reports?sort=latest&count=" + str(count) + "&reportTag=" + quote(self.config.bph_tracking_tag)

            headers = {}
            if self.config.titan_user_agent:
                headers = {"User-Agent": self.config.titan_user_agent}

            self.config.logger.info("Sending request: " + request)

            response = requests.get(request, headers=headers, auth=(self.config.titan_username, self.config.titan_api_key))
            if response.status_code == 200:
                results = response.json()
                if results.get("reports"):
                    reports = results["reports"]

            self.config.logger.info(str(len(reports)) + " BPH tracking reports acquired.")

        except HTTPError as http_err:
            reports = []
            self.config.logger.error("Unable to get BPH tracking reports from Titan: %s", {http_err})

        except Exception as e:
            reports = []
            self.config.logger.error("Unable to get BPH tracking reports from Titan: %s", {e})

        return reports

    def get_bph_tracking_report(self, uid: str) -> Dict:
        report: Dict = {}

        try:
            self.config.logger.info("Attempting to acquire BPH tracking report.")

            request: str = self.config.titan_api_base_url + "reports/" + uid

            headers = {}
            if self.config.titan_user_agent:
                headers = {"User-Agent": self.config.titan_user_agent}

            self.config.logger.info("Sending request: " + request)

            response = requests.get(request, headers=headers, auth=(self.config.titan_username, self.config.titan_api_key))
            if response.status_code == 200:
                report: Dict = response.json()
                self.config.logger.info("Acquired BPH tracking report.")

        except HTTPError as http_err:
            report = {}
            self.config.logger.error("Unable to get BPH tracking report from Titan: %s", {http_err})

        except Exception as e:
            report = {}
            self.config.logger.error("Unable to get BPH tracking report from Titan: %s", {e})

        return report

    def get_bph_tracking_report_attachment(self, url: str) -> str:
        attachment: str = ""

        try:
            self.config.logger.info("Attempting to acquire BPH tracking report attachment.")

            headers = {}
            if self.config.titan_user_agent:
                headers = {"User-Agent": self.config.titan_user_agent}

            self.config.logger.info("Sending request: " + url)

            response = requests.get(url, headers=headers, auth=(self.config.titan_username, self.config.titan_api_key))
            if response.status_code == 200:
                attachment = response.text.strip()

                self.config.logger.info("Acquired BPH tracking report attachment.")

        except HTTPError as http_err:
            attachment = ""
            self.config.logger.error("Unable to get BPH tracking report attachment from Titan: %s", {http_err})

        except Exception as e:
            attachment = ""
            self.config.logger.error("Unable to get BPH tracking report attachment from Titan: %s", {e})

        return attachment
