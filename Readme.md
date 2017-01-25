
This application uses the GitHub Jobs API to show a breakdown of jobs by city and then by experience.

It should output something akin to:

Boston:
  - Python
    - 0-2 years: 25%
    - 3-5 years: 10%
    - 5+ years:  5%
  - Ruby:
    - 0-2 years: 30%
    - 3-5 years: 15%
    - 5+ years: 8%

San Francisco:
  - Node:
    - 0-2 years: 25%
    - 3-5 years: 10%
    - 5+ years:  5%
  - Scala:
    - 0-2 years: 25%
    - 3-5 years: 10%
    - 5+ years:  5%


Sourced: 1,123 job postings

Requirements
------------
This project Requires python3 and pip3.  You must install these before attempting to install this project.


Installation
----------
Install requirements via pip3: `pip3 install -r requirements.txt`


Running
------
You may run the program via `python jobstats.py -l "Los Angeles" "San Francisco" Portland "New York"`.  Feel free to
substitute whatever location keywords you desire.

Notes
-----

* The percentages of each location might sum up over 100.  This is because a particular posting may be in more than 1 language set.
E.g. A posting could be a dev with 1-3 years of python exp as well as 2-3 years ASP.net.
* As there is no set rule to how job descriptions are written, many times the requirements are not simply listed in terms of X many years for Y skill.
This is why you will see many "Not specified" levels of experience required for your locations.