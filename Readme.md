# codingTracker
Python project that track how many hours you spend coding and provides stats
on the languages and platform you use.

## Description
This repository contains the client.
The client is installed on your computer and track your coding activity. It
saves everything in a sqlite3 database in data/database.db by default.
If it can, the client sync the data with the server and erase the local data.

## Getting Started

### Dependencies
The project uses standard library only. For dev, see the setup.cfg

### Installing
Create a virtual environment: python3 -m venv venv
Activate it: source venv/bin/activate
pip install codingTracker
codingTrackerSetup

### Executing program
Run the client: codingTracker [OPTIONS]
[OPTIONS]: IP_address Port Path_to_db

## Authors

Contributors names and contact info

Emmanuel Guefif
eguefif@fastmail.com

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Version
0.1.b
