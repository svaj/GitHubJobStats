import pytest
import asyncio
import async_timeout
from jobstats import *

async def test_get_jobs():
    """ Ensure we get at least 1 job. """
    for location in ['San Francisco', 'Los Angeles', 'New York']:
        async with aiohttp.ClientSession(loop=loop) as session:
            jobs = await get_jobs(session, location)
            location_jobs[location] = jobs
            job_total += len(jobs)
    assert job_total > 0

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
