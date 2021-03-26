![Spyder_Logo](docs/spyder_logo_v2.jpeg)

# Spyder
![Code Count](https://img.shields.io/github/languages/count/lcerdeira/Spyder) 
![Main Code Base](https://img.shields.io/github/languages/top/lcerdeira/Spyder) 
![License](https://img.shields.io/badge/license-GPLv3-blue)
![Version](https://img.shields.io/badge/version-1.0-red) 
![Last Commit](https://img.shields.io/github/last-commit/lcerdeira/Spyder) 
![Open Issues](https://img.shields.io/github/issues-raw/lcerdeira/Spyder) 
![Repo Size](https://img.shields.io/github/repo-size/lcerdeira/Spyder)
[![DOI](https://zenodo.org/badge/331138839.svg)](https://zenodo.org/badge/latestdoi/331138839)

## Requirements
### Language and framework
- Python 3+
- Scrapy 2.4

#### Main files
- generate_file.py
    - It is responsable for create directories and files saving csv and newick data.
- collections.py
    - It is responsable for scraping csv data from form on each collection.
- collections_from_link.py
    - It is responsable for scraping csv and newick data from each collection.
### Server System Requirements (Snapshot or docker allowed)
- Ubuntu Server
- 16GB RAM Memory
- 512GB Disk

## Used
- Open terminal of your operational system.
- Verify Python version and installation with `python --version` by terminal.
- If not installed run `sudo apt update` and `sudo apt install python3.8` .
- Verify pip (manager python's libraries) version and installation with `pip --version` by terminal.
- If not installed run `sudo apt install python3-pip` .
- Verify git (manager repository) version and installation with `git --version` by terminal.
- If not installed run `sudo apt install git` .
- Create a directory for your project
    - `mkdir <your directory_name>` .
- Into your directory
    - `cd <your directory>` .
- Clone repository to local. `git clone https://github.com/lcerdeira/Spyder.git` .
- Into to repository cloned.
    - `cd webscrap` .
- After that run command `pip install -r requirements.txt` to install required modules.
- Now you stay at main directory. Run `scrapy crawl collections` on terminal to start webscraping to collecting csv.
- Now you stay at main directory. Run `scrapy crawl collections_from_link` on terminal to start webscraping to collecting newick.
- The downloaded files will appear on files directory automatically created.

### Flow Diagram
- ![flow diagram](./docs/diagram.jpeg)
