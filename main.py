"""
Job scraping entry point.

This script searches Indeed and LinkedIn for automation, DevOps, cloud,
platform, systems, and network automation roles across a predefined set of
North Carolina and remote locations.

For each location, the script calls the ScraperJobs helper class to collect
matching job postings, then appends the results to both a SQLite database
and a CSV file. Existing output files are removed at startup so each run
starts with a fresh jobs.db database and jobs_raw_table.csv export.

Outputs:
    jobs.db: SQLite database containing scraped job records in the "jobs" table.
    jobs_raw_table.csv: CSV export of the scraped job records.

Notes:
    The script currently appends results location-by-location. If no jobs are
    found for a location, the script exits early and skips the remaining
    locations.
"""

import os
from utils.scraper import ScraperJobs
import sqlite3



def main():
    searches = ["Python automation engineer",
                "Infrastructure automation engineer",
                "Cloud automation engineer",
                "Network automation engineer",
                "Platform support engineer Python",
                "SRE Python AWS",
                "DevOps engineer contract Python Terraform",
                "Tools engineer Python",
                "Systems engineer Python AWS",
                "Python migration engineer",
                "Ansible automation engineer"]
    sites = ["indeed", "linkedin"]
    location = ["Raleigh, NC", "Durham, NC", "Chapel Hill, NC", "North Carolina", "Remote"]
    results = 1000
    old = 12
    country = "USA"
    if os.path.exists("jobs.db"):
        os.remove("jobs.db")
        os.remove("jobs_raw_table.csv")

    scraper = ScraperJobs()
    for local in location:
        df = scraper.scrape_jobs(searches, sites, results, old, country, local)

        if df.empty:
            print("No jobs found. Skipping database and CSV write.")
            return

        comm = sqlite3.connect("jobs.db")
        df.to_sql("jobs", comm, if_exists="append", index=False)
        comm.close()

        df.to_csv("jobs_raw_table.csv", mode="a")


if __name__ == "__main__":
    main()
