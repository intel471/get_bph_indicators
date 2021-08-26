#!/usr/bin/env python3.8
import os
import sys
from datetime import datetime
import json
import csv
from typing import List, Dict
from get_bph_indicators_config import GetBPHIndicatorsConfig
from titan_utilities import TitanUtilities

config: GetBPHIndicatorsConfig = GetBPHIndicatorsConfig()


def process_report_attachment(titan: TitanUtilities, report_attachment: Dict) -> Dict:
    bph_indicators: Dict = {}

    try:
        config.logger.info("Processing BPH tracking report attachment.")

        if url := report_attachment.get("url"):

            if filename := report_attachment.get("fileName"):
                attachment = titan.get_bph_tracking_report_attachment(url)

                # Save the raw file.
                with open(os.path.join(config.files_output_directory, filename), "w") as raw_writer:
                    raw_writer.writelines(attachment)

                ip_addresses = set([])
                domains = set([])

                rows = csv.reader(attachment.split("\n"))

                is_header: bool = True
                for row in rows:
                    if is_header:
                        is_header = False
                    else:
                        try:
                            ipaddr, _, domain, _ = row[0].split(";")
                        except Exception as e:
                            config.logger.info("Can't process row %s. Skipping.", str(row[0]))
                        else:
                            ip_addresses.add(ipaddr)
                            domains.add(domain)

                bph_indicators = {
                    "indicators": {
                        "inticators_ipv4_count": len(ip_addresses),
                        "indicators_domain_count": len(domains),
                        "indicators_ipv4": sorted(list(ip_addresses)),
                        "indicators_domain": sorted(list(domains))
                    }
                }

        config.logger.info("Processing BPH tracking report attachment complete.")

    except Exception as e:
        bph_indicators = {}
        config.logger.error("An error has occurred whilst processing BPH tracking report attachment: %s", {e})

    return bph_indicators


def process_bph_tracking_report(titan: TitanUtilities, bph_provider: str, uid: str) -> Dict:
    bph_provider_indicators: Dict = {}

    try:
        config.logger.info("Processing BPH tracking report (Provider: " + bph_provider + ", Report UID: " + uid)

        report: Dict = titan.get_bph_tracking_report(uid)
        if report:
            last_updated: int = report.get("lastUpdated", 0)
            if report_attachments := report.get("reportAttachments"):
                for report_attachment in report_attachments:
                    bph_indicators: Dict = process_report_attachment(titan, report_attachment)
                    bph_provider_indicators = {
                        "bph_provider": bph_provider,
                        "last_updated": last_updated,
                        "indicators": bph_indicators["indicators"]
                    }

        config.logger.info("Processing BPH tracking report complete.")

    except Exception as e:
        config.logger.error("An error has occurred whilst processing BPH tracking report: %s", {e})

    return bph_provider_indicators


def process_bph_tracking_reports(titan: TitanUtilities, reports: List) -> Dict:
    bph_provider_indicators: Dict = {
        "bph_provider_indicators": []
    }

    try:
        config.logger.info("Processing BPH tracking reports.")

        # Process the most recent report for each BPH Provider.
        bph_providers: List = []

        for report in reports:
            if handles := report.get("actorSubjectOfReport"):
                for handle in handles:
                    if bph_provider := handle.get("handle"):
                        if bph_provider not in bph_providers:
                            if uid := report.get("uid"):
                                report_bph_tracking_report_indicators: Dict = process_bph_tracking_report(titan, bph_provider, uid)
                                bph_provider_indicators["bph_provider_indicators"].append(report_bph_tracking_report_indicators)
                                bph_providers.append(bph_provider)

        config.logger.info("Processing BPH tracking reports complete.")

    except Exception as e:
        config.logger.error("An error has occurred whilst processing BPH tracking reports: %s", {e})

    return bph_provider_indicators


def acquire_bph_data(titan: TitanUtilities):
    success: bool = True

    try:
        config.logger.info("Processing BPH indicators.")

        bph_tracking_reports: List = titan.get_bph_tracking_reports()
        bph_provider_indicators: Dict = process_bph_tracking_reports(titan, bph_tracking_reports)

        current_date: str = datetime.today().strftime('%Y-%m-%d')
        with open(os.path.join(config.files_output_directory, f"{current_date}_{config.files_output_file_json}"), "w") as output_json_writer:
            output_json_writer.writelines(json.dumps(bph_provider_indicators, indent=4))

        config.logger.info("Processing BPH indicators complete.")

    except Exception as e:
        success = False
        config.logger.error("An error has occurred whilst processing BPH indicators: %s", {e})

    return success


def main():
    try:
        config_initialise_status: bool = config.initialise()
        if config_initialise_status is False:
            sys.exit(1)

        config.logger.info("Get BPH Indicators initialisation successful.")

        titan: TitanUtilities = TitanUtilities(config)
        if titan:
            acquire_bph_data(titan)

        config.logger.info("Get BPH Indicators complete.")

    except Exception as e:
        config.logger.error("An error has occurred: %s", {e})
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
