# TyphiNET web dashboard
![Code Count](https://img.shields.io/github/languages/count/lcerdeira/Spider) 
![Main Code Base](https://img.shields.io/github/languages/top/lcerdeira/Spider) 
![License](https://img.shields.io/badge/license-GPL) 
![Version](https://img.shields.io/badge/version-1.0-red) 
![Last Commit](https://img.shields.io/github/last-commit/lcerdeira/Spider) 
![Open Issues](https://img.shields.io/github/issues-raw/lcerdeira/Spider) 
![Repo Size](https://img.shields.io/github/repo-size/lcerdeira/Spider)

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
### Server System Requirements
- Ubuntu Server
- 24GB Memory Ram or 16GB
- 1TB Disk

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
- Clone repository to local. `git clone https://github.com/lcerdeira/Spider.git` .
- Into to repository cloned.
    - `cd webscrap` .
- After that run command `pip install -r requirements.txt` to install required modules.
- Now you stay at main directory. Run `scrapy crawl collections` on terminal to start webscraping to collecting csv.
- Now you stay at main directory. Run `scrapy crawl collections_from_link` on terminal to start webscraping to collecting newick.
- The downloaded files will appear on files directory automatically created.

### Flow Diagram
- ![flow diagram](./docs/diagram.jpeg)