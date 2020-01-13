# 2019 Orbital Launches Crawler

Author: Guorui Ma @[WindfuryBulb](https://github.com/WindfuryBulb)

## Project Description

This crawler can get the number of orbital launches in 2019 in the 'Orbital launches' table in [Wikipedia 2019 Orbital Launches website](https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches) **if and only if** at least one of its payloads is reported as 'Successful', 'Operational', or 'En Route', and then output a ``.csv`` file contains dates (Jan 1, 2019 - Dec 31, 2019) in ISO8601 format and how many successful orbital launches on that coresponding day.

**Note:** A launch in the U.S on Dec 20, 2019 with only one payload called "Starliner Boe-OFT" that is reported as 'Spacecraft anomaly, recovered successfully' is treated as **failure**.

## Get started

This project is written in **python 3** with following libraries:

* `beautifulsoup4` (Author uses version 4.8.2)
* `requests` (Author uses version 2.18.4)

You can install Python 3.6 or newer first, and then install the two libraries via following script:

`python3 -m pip install beautifulsoup4 requests`

Finally, you can run the crawler via following script:

`python3 2019_orbit_script.py`