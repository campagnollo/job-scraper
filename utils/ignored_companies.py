"""
ignored_companies.py

Defines the list of companies to exclude from job scraping results.

Add company names here to filter them out of scraped job listings.
This module is imported by scraper.py and applied as a DataFrame filter
during post-processing.
"""
def companies_to_drop():
    """
        Return a set of company names to exclude from job scraping results.

        These companies are typically staffing agencies, job boards, or employers
        deemed unsuitable for the current job search criteria. The returned set
        is used in scraper.py to filter out matching rows from the jobs DataFrame.

        Returns:
            set[str]: Company names to exclude from scraped job listings.
        """
    return {"Epic", "Piper Companies", "Turing", "RemoteHunter", "idexcel",
            "BV Teck","World Wide Technology", "CBRE","Motion Recruitment", "Crossover", "Hired",
            "Hire Feed", "Quik Hire Staffing", "Sundayy", "DataAnnotation", "MixRank",
            "Crossing Hurdles", "Zachary Piper Solutions","Revature", "Actalent", "Smart Working",
            "BairesDev","RapidScale"}
