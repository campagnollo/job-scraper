"""
scraper.py

Job scraping module for the job_scraper pipeline.

Provides the ScraperJobs class, which wraps the jobspy library to scrape
job listings from Indeed and LinkedIn across multiple search terms and
locations. Results are returned as a cleaned pandas DataFrame with
irrelevant columns removed and duplicate listings deduplicated.

Dependencies:
    jobspy     — third-party job scraping library
    pandas     — data manipulation and DataFrame output

Output schema (columns retained after cleaning):
    id, site, job_url, job_url_direct, title, company, location,
    date_posted, is_remote, num_urgent_words, benefits, job_url_hyper

Usage:
    from scraper import ScraperJobs, ScrapeConfig

    config = ScrapeConfig(
        searches=["Python automation engineer"],
        sites=["indeed", "linkedin"],
        results=100,
        hours_old=4,
        country="USA",
        location="Raleigh, NC",
    )
    scraper = ScraperJobs()
    df = scraper.scrape_jobs(config)
"""

from dataclasses import dataclass
from typing import List

import pandas as pd
from jobspy import scrape_jobs
from jobspy.exception import LinkedInException, IndeedException

# Columns removed from raw jobspy output — not needed for downstream processing.
_COLUMNS_TO_DROP = [
    "job_type", "salary_source", "interval", "min_amount", "max_amount",
    "currency", "job_level", "job_function", "listing_type", "emails",
    "description", "company_industry", "company_logo", "company_address",
    "company_num_employees", "company_revenue", "company_description",
    "skills", "experience_range", "company_rating", "company_reviews_count",
    "vacancy_count", "work_from_home_type", "company_addresses",
    "company_url_direct", "job_url_direct"
]
_LOCATIONS_TO_DROP_PATTERNS = [
    r"\bMexico\b", r"\bBrasil\b", r"\bBrazil\b", r"\bColombia\b",
    r"\bArgentina\b", r"\bChile\b", r"\bPeru\b", r"\bVenezuela\b",
    r"\bEcuador\b", r"\bBolivia\b", r"\bParaguay\b", r"\bUruguay\b",
    r"\bPanama\b", r"\bGuatemala\b", r"\bHonduras\b", r"\bNicaragua\b",
    r"\bCosta Rica\b", r"\bEl Salvador\b", r"\bCuba\b", r"\bDominican\b",
]
_TITLES_TO_DROP = ["PLC","Manufacturing", "Mechanical", "Electrical", "Civil", "Project"]
_COMPANIES_TO_DROP = ["Epic", "Piper Companies", "Turing", "RemoteHunter", "idexcel",
                      "CBRE", "Crossover", "Hired", "Hire Feed", "Quik Hire Staffing", "Sundayy"]

_SUPPORTED_SITES = ["indeed", "linkedin", "glassdoor", "ziprecruiter", "careerjet",
                    "simplyhired", "dice"]


@dataclass
class ScrapeConfig:
    """Configuration parameters for a single scrape_jobs run.

    Attributes:
        searches  (list[str]): Search queries (e.g. 'Python automation engineer').
        sites     (list[str]): Job sites to scrape. Supported: 'indeed', 'linkedin'.
        results   (int):       Max results to request per search/site combination.
        hours_old (int):       Maximum age of listings in hours (e.g. 12).
        country   (str):       Country filter for Indeed (e.g. 'USA').
        location  (str):       Location string (e.g. 'Raleigh, NC' or 'Remote').
                               If 'remote', non-remote rows are filtered out.
    """
    searches: List[str]
    sites: List[str]
    results: int
    hours_old: int
    country: str
    location: str


class ScraperJobs:
    """Scrapes job listings from Indeed and LinkedIn using the jobspy library."""

    @staticmethod
    def get_supported_sites() -> List[str]:
        """Return the list of job sites supported by this scraper."""
        return _SUPPORTED_SITES

    def scrape_jobs(self, config: ScrapeConfig) -> pd.DataFrame:
        """
        Scrape job listings across multiple search terms and a single location.

        Iterates over each search term and site combination, scrapes results,
        filters for remote roles if location is 'remote', deduplicates by job
        ID, and drops columns not relevant to downstream processing.

        Parameters:
            config (ScrapeConfig): Dataclass containing all scrape parameters.

        Returns:
            pd.DataFrame: Cleaned, deduplicated job listings. Returns an empty
                          DataFrame if no results are found across all searches.

        Raises:
            Exceptions from jobspy (LinkedInException, IndeedException, ValueError)
            are caught per search/site and logged to stdout — they do not
            propagate to the caller.
        """
        df = pd.DataFrame()

        for search in config.searches:
            jobs = pd.DataFrame()

            for site in config.sites:
                try:
                    site_jobs = scrape_jobs(
                        site_name=[site],
                        search_term=search,
                        results_wanted=config.results,
                        hours_old=config.hours_old,
                        country_indeed=config.country,
                        location=config.location,
                    )
                except ValueError as ve:
                    print(f"Value error in search '{search}': {ve}")
                    continue
                except LinkedInException as le:
                    print(f"LinkedIn scraping error in search '{search}': {le}")
                    continue
                except IndeedException as ie:
                    print(f"Indeed scraping error in search '{search}': {ie}")
                    continue

                #   todo: prevent empty entries from being concatenated, which can cause issues with downstream processing
                jobs = pd.concat(
                    [df.dropna(axis=1, how='all') for df in [jobs, site_jobs]],
                    ignore_index=True
                )

            print(f"Scraped {len(jobs)} jobs for search query: '{search}'")
            df_search = pd.DataFrame(jobs)

            # If the requested location is Remote, remove non-remote rows.
            if config.location.strip().lower() == "remote" and "is_remote" in df_search.columns:
                df_search = df_search[df_search["is_remote"].fillna(False)]
            if not df_search.empty:
                df = pd.concat([df, df_search], ignore_index=True)
            if not df.empty and "id" in df.columns:
                df = df.drop_duplicates(subset=["id"])
        if "title" in df.columns:
            mask = df["title"].str.contains("|".join(_TITLES_TO_DROP), case=False, na=False)
            df = df[~mask]
        if "company" in df.columns:
            mask = df["company"].str.contains("|".join(_COMPANIES_TO_DROP), case=False, na=False)
            df = df[~mask]
        if "location" in df.columns:
            pattern = "|".join(_LOCATIONS_TO_DROP_PATTERNS)
            mask = df["location"].str.contains(pattern, case=False, na=False, regex=True)
            df = df[~mask]
        df = df.drop(columns=_COLUMNS_TO_DROP, errors="ignore")
        return df