#!/usr/bin/python3 # Just in-case the user didn't set up a virtual env :)
import requests
import json
import argparse

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

def get_jobs(location="Portland"):
    """
    Grabs the jobs for a city from GitHub's API.
    :param location: The location (city, zip, or other location search term)
    :return: a list of jobs for this location.
    """
    #TODO: Reminder to check for pagination.

def parse_jobs(jobs):
    """
    Parses the json jobs from GitHub.
    :param jobs: json describing a set of jobs
    :return: Returns a dict of dicts of Language with Experience levels: {'Python':{'0-2 years':44}, 'Ruby': {'1-4 years': 3}}
    """


def display_city_jobs(location, jobs):
    """
    Displays percentage of jobs in a location (by Requirement and Exp Level)
    :param location: The location we are to display.
    :param jobs: The parsed jobs from parse_jobs
    :return: None
    """


def main():
    """ Entry point of our application, set up the command line args, main execution of our application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locations", nargs="+", help="<Required> List of locations to display.", required=True)
    job_total = 0
    args = parser.parse_args()
    for location in args.locations:
        jobs = get_jobs(location=location) # TODO: grab these upfront, thread them so we aren't waiting too long.
        parsed_jobs = parse_jobs(jobs)
        display_city_jobs(location, jobs)
    print("Sourced {:n} job postings".format(job_total))
    return

# Run the application.
main()
