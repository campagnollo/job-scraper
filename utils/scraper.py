from threading import local
import pandas as pd
from jobspy import scrape_jobs
from jobspy.exception import LinkedInException, IndeedException

class ScraperJobs:
    def __init__(self):
        pass

    def scrape_jobs(self, searches, sites, results, old, country, location):
        """
        Scrape jobs from specified sites based on search queries.

        Parameters:
        searches (list): List of search queries.
        sites (list): List of job sites to scrape.
        results (int): Number of results to scrape per search query.
        """
        df=pd.DataFrame()
        for search in searches:
            for site in sites:
                try:
                    jobs=scrape_jobs(site_name=[site],
                                     search_term=search,
                                     results_wanted=results,
                                     hours_old=old,
                                     country_indeed=country,
                                     location=location
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

            print(f"Scraped {len(jobs)} jobs for search query: '{search}'")
            df_search= pd.DataFrame(jobs)

            # If the requested location is Remote, remove non-remote rows.
            if location.strip().lower() == "remote" and "is_remote" in df_search.columns:
                df_search = df_search[df_search["is_remote"].fillna(False)]


            if df_search is not None and not df_search.empty:
                df = pd.concat([df, df_search], ignore_index=True)
            if not df.empty and "id" in df.columns:
                df = df.drop_duplicates(subset=['id'])
        df = df.drop(columns=["job_type", "salary_source", "interval", "min_amount", "max_amount", "currency",
                              "job_level", "job_function", "listing_type", "emails", "description",
                              "company_industry", "company_logo", "company_address", "company_num_employees",
                              "company_revenue", "company_description", "skills", "experience_range", "company_rating",
                              "company_reviews_count", "vacancy_count", "work_from_home_type", "company_addresses",
                              "company_url_direct"], errors='ignore')
        return df

