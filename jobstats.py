#!/usr/bin/python3 # Just in-case the user didn't set up a virtual env :)
import json
import argparse
import asyncio
import async_timeout
import aiohttp
from urllib.parse import quote
from bs4 import BeautifulSoup #  to strip HTML.
import re

"""
This application uses the GitHub API to show a breakdown of jobs by city and then by experience.

It should output something akin to:

Boston:
  - Python
    - 0-2 years experience: 25%
    - 3-5 years experience: 10%
    - 5+ years experience:  5%
  - Ruby:
    - 0-2 years experience: 30%
    - 3-5 years experience: 15%
    - 5+ years experience: 8%
San Francisco:
  - Node:
    - 0-2 years experience: 25%
    - 3-5 years experience: 10%
    - 5+ years experience:  5%
  - Scala:
    - 0-2 years experience: 25%
    - 3-5 years experience: 10%
    - 5+ years experience:  5%


Sourced: 1,123 job postings

"""

MAX_JOBS_PER_PAGE = 50  # from https://jobs.github.com/api

# For a more comprehensive list: https://en.wikipedia.org/wiki/List_of_programming_languages
LANGS_TO_SCAN_FOR = {'python', 'ruby', 'nodejs', 'javascript', 'C', 'C++', 'C#', 'java', 'scala', 'go', 'php'}
#  TODO: allow this to be overridden by a command line arg.


async def get_jobs(session, location="Portland", page=0):
    """
    Grabs the jobs for a city from GitHub's API.
    :param session: The Async session.
    :param location: The location (city, zip, or other location search term) to fetch.
    :param page: The current page of results to fetch.
    :return: a list of jobs for this location.
    """
    url = "https://jobs.github.com/positions.json?location={}&page={}".format(quote(location), page)
    with async_timeout.timeout(10):  # TODO: Set this from an optional command line arg.
        async with session.get(url) as response:
            print("Got jobs page {} for {}".format(page, location))
            if response.status != 200:
                raise Exception("Failed getting job listings for {}, page {}".format(location, page))
            # parse jobs from json
            json_text = await response.text()
            try:
                jobs = json.loads(json_text)
            except:
                raise Exception("Could not load JSON from GitHub API response for {}, page {}".format(location, page))

            # if results >= 50, attempt to add on another page of results
            if len(jobs) >= MAX_JOBS_PER_PAGE:
                jobs.extend(get_jobs(session, location, page + 1))

            return jobs


def parse_jobs(jobs):
    """
    Parses the json jobs from GitHub.
    :param jobs: json describing a set of jobs
    :return: Returns a dict of dicts of Language with Experience levels: {'Python':{'0-2 years': ['job1','job2']}, 'Ruby': {'1-4 years': ['job1', 'job3]}}
    """
    parsed_jobs = {}

    for j in jobs:
        # Find out Requirements, it looks like these are somewhere in Description -- some html that is free-form
        # There might not be any hard language requirements stated either!
        # There might not be any exp level mentioned as well!

        description = BeautifulSoup(j['description'], "html.parser").get_text().lower()  # Strip HTML from description.
        # Remove non-ascii chars for easier processing.
        description = re.sub(r'[^\x00-\x7F]+', ' ', description)

        # find language requirements and exp levels in description, if it is even there.
        # This is pretty gross and I'm not sure of a good way to do better -- save for something crazy with NLP / http://www.nltk.org/
        # Let's just check for the mere existence of the language keywords in the description.
        for lang in LANGS_TO_SCAN_FOR:
            if lang in description:
                # Keyword found - let's see the level of exp required!

                if lang not in parsed_jobs:
                    parsed_jobs[lang] = {}
                # Try to find a level of experience needed (default "Not specified")
                matches = re.findall(r'[\d]+-[\d]+ years', description)
                if matches:
                    # For now, just take the first match. of ??-?? years experience
                    level = matches[0]
                else:
                    level = "Not specified"
                if level not in parsed_jobs[lang]:
                    parsed_jobs[lang][level] = [j['url']]
                else:
                    parsed_jobs[lang][level].append(j['url'])
    return parsed_jobs



def display_city_jobs(location, jobs):
    """
    Displays percentage of jobs in a location (by Requirement and Exp Level)
    :param location: The location we are to display.
    :param jobs: The parsed jobs from parse_jobs
    :return: None
    """
    print("{}:".format(location))
    # print by language & experience
    # Get number of unique jobs in this location:
    unique_jobs = []
    for lang in jobs:
        for level in jobs[lang]:
            unique_jobs += jobs[lang][level]
    unique_jobs = set(unique_jobs)  # Now we have the unique values
    # Proceed to display
    for lang in jobs:
        print("  - {}:".format(lang))
        for level in jobs[lang]:
            pct = len(jobs[lang][level])/len(unique_jobs)*100
            print("    - {}: {:.0f}%".format(level, pct))


async def main(loop):
    """ Entry point of our application, set up the command line args, main execution of our application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations", nargs="+", help="<Required> List of locations to display.", required=True)
    job_total = 0
    args = parser.parse_args()

    location_jobs = {}
    # Perform all our HTTP requests up front.
    for location in args.locations:
        async with aiohttp.ClientSession(loop=loop) as session:
            jobs = await get_jobs(session, location)
            location_jobs[location] = jobs
            job_total += len(jobs)
    # now get the lang. requirements and exp levels and then display them.
    for location in args.locations:
        parsed_jobs = parse_jobs(location_jobs[location])
        display_city_jobs(location, parsed_jobs)
    print("Sourced {:n} job postings".format(job_total))
    return

# Run the application.
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
