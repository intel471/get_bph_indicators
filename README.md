# get_bph_indicators

## Intel 471 get_bph_indicators (Acquisition of Bulletproof Hosting Indicators From Titan)

## Overview
get_bph_indicators delivers the ability for Intel 471's Gold and Platinum customers to automate the acquisition of Bulletproof Hosting (BPH) indicators from the Titan platform.

Whilst it is possible to view BPH information within the Titan UI, obtaining this data programmatically via the Titan API is currently a little more challenging. However, this script outlines an approach for achieving this.

When run, the script will acquire the latest available data for all BPH providers that are tracked by Intel 471.

## Requirements
- A suitable host for the get_bph_indicators script. This host should have access to the Titan API (https://api.intel471.com).
- Python 3.8+ installed on the above host.
- Your Titan credentials (username and API key).

## Configuration
The /config/get_bph_indicators.ini contains all of the following configuration settings:

| Setting                                                 | Description                                                                                                |
| -------                                                 | -----------                                                                                                |
| files                                                   |                                                                                                            |
| config_directory                                        | The sub directory containing the config file.                                                              |
| log_directory                                           | The sub directory to which log files are written.                                                          |
| log_prefix                                              | Prefix to be used for log filenames.                                                                       |
| output_directory                                        | The sub directory to which output files are written.                                                       |
| output_file_json                                        | The name of the consolidated JSON formatted file containing the BPH data.                                  |
|                                                         |                                                                                                            |
| intel471                                                |                                                                                                            |
| titan_username                                          | Titan username.                                                                                            |
| titan_api_key                                           | Titan API key.                                                                                             |
| titan_api_base_url                                      | Base URL of the Titan API.                                                                                 |
| titan_api_batch_size                                    | Maximum number of objects to obtain from Titan API for a single request (max 100).                         |
| titan_user_agent                                        | The user agent string to be used for all requests to the Titan API.                                        |
| bph_tracking_tag                                        | The name of the Titan tag that is used to identify Bulletproof Hosting Tracking reports.                   |

Most of the config points described above are pre-populated in the sample provided.  The main items to add are the Titan username and Titan API key. The values for the other config points may of course be changed to match your own requirements.

## Installation
- Copy the entire contents (files and directories) of the directory containing the script to an appropriate directory on the host that will run the script.
- Navigate to the directory above eg:
  ```
  cd /opt/intel471/get_bph_indicators
  ```
- Create a virtual environment within which the integration script will run eg:
  ```
  python3 -m venv env
  ```
- Activate your virtual environment eg:
  ```
  source env/bin/activate
  ```
- Install the required packages within the virtual environment eg:
  ```
  $ pip install -r requirements.txt
  ```
- Edit the /config/get_bph_indicators.ini file in line with your requirements (eg Titan credentials).

## Invocation
The integration script may be run manually using:
```
python3 get_bph_indicators.py
```

## Logging
Log files are written to the directory specified by the [files][log_directory] config point, using a prefix specified by the [files][log_prexix] config point.

## Output
Each time the script is run, files containing the latest BPH indicator data for all providers tracked by Intel 471 are written to the [files][output] directory.

A .csv file containing the raw data will be written for each of the tracked BPH providers.  In addition, a .json file will be written that contains a consolidated collection of all indicators for all tracked BPH providers.
