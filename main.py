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
    The script appends results location-by-location. If no jobs are
    found for a location, that location is skipped and the remaining
    locations continue to be processed.
"""

import os
import sqlite3
from utils.scraper import ScraperJobs, ScrapeConfig


def main():
    """
    Entry point for the job scraper pipeline.

    Searches for automation and DevOps-related roles across Indeed and LinkedIn
    for multiple locations in the Raleigh/NC area and remote. For each location,
    scrapes up to 1000 results posted within the last 12 days and appends them
    to a local SQLite database (jobs.db) and a CSV file (jobs_raw_table.csv).

    Any existing jobs.db and jobs_raw_table.csv files are deleted at startup
    to ensure a clean run. If no jobs are found for a given location, that
    location is skipped and processing continues.

    Locations searched:
        Raleigh NC, Durham NC, Chapel Hill NC, North Carolina, Remote

    Output files:
        jobs.db             — SQLite database with a 'jobs' table
        jobs_raw_table.csv  — Raw results appended per location
    """
    searches = [
        "Python automation engineer",
        "Infrastructure automation engineer",
        "Cloud automation engineer",
        "Network automation engineer",
        "SRE Python AWS",
        "DevOps engineer contract Python Terraform",
        "Systems engineer Python AWS",
        "Ansible automation engineer",
        "Network automation architect",
        "Cloud network engineer",
        "Kubernetes platform engineer"]
    sites = ["indeed", "linkedin"]
    locations = ["Raleigh, NC", "Remote"]
    results = 1000
    hours_old = 4
    country = "USA"

    if os.path.exists("jobs.db"):
        os.remove("jobs.db")
    if os.path.exists("jobs_raw_table.csv"):
        os.remove("jobs_raw_table.csv")

    scraper = ScraperJobs()

    for local in locations:
        config = ScrapeConfig(
            searches=searches,
            sites=sites,
            results=results,
            hours_old=hours_old,
            country=country,
            location=local,
        )
        df = scraper.scrape_jobs(config)

        if df.empty:
            print(f"No jobs found for '{local}'. Skipping database and CSV write.")
            continue

        conn = sqlite3.connect("jobs.db")
        df.to_sql("jobs", conn, if_exists="append", index=False)
        conn.close()

        write_header = not os.path.exists("jobs_raw_table.csv")
        df.to_csv("jobs_raw_table.csv", mode="a", header=write_header, index=False)


if __name__ == "__main__":
    main()