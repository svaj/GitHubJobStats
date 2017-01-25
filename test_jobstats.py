import pytest
from jobstats import *

def test_get_jobs():
    return

def test_parse_jobs():
    jobs = [
        {
            'url': 'http://www.svajlenka.com/',
            'description': "<b>WOW Python dev needed! Requirements: 2-3 years experience. WOW</b>"
        },
        {
            'url': 'http://bad-place-to.work',
            'description': '<strong>Rockstar Ninja Brogrammers needed! 15-20 years of NodeJS REQUIRED.'
        }
    ]
    parsed_jobs = parse_jobs(jobs)
    expected_result = {
        "python": {'2-3 years': ['http://www.svajlenka.com/']},
        'nodejs': {'15-20 years': ['http://bad-place-to.work']}
    }
    assert parsed_jobs == expected_result
