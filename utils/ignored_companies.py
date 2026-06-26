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
    return {"epic", "piper companies", "turing", "remotehunter", "idexcel",
            "bv teck", "world wide technology", "cbre", "motion recruitment", "crossover", "hired",
            "hire feed", "quik hire staffing", "sundayy", "dataannotation", "mixrank",
            "crossing hurdles", "zachary piper solutions", "revature", "actalent", "smart working",
            "bairesdev", "rapidscale", "ans", "domino's", "trace systems inc.", "lennor group",
            "fullstack", "quadrivia ai", "haystack", "qualys","jobs via dice", "bandwidth inc.",
            "tech consulting", "deloitte", "ninjaone", "siemens energy","kc ml2","randstad digital americas"}


