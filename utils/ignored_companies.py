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
    return {
        "actalent",
        "ans",
        "bairesdev",
        "bandwidth inc.",
        "bv teck",
        "cbre",
        "crossing hurdles",
        "crossover",
        "dataannotation",
        "deloitte",
        "domino's",
        "epic",
        "fullstack",
        "gsk",
        "haystack",
        "hcltech",
        "hired",
        "hire feed",
        "idexcel",
        "infosys",
        "insight global",
        "jobs via dice",
        "kc ml2",
        "lennor group",
        "mixrank",
        "motion recruitment",
        "ninjaone",
        "piper companies",
        "quadrivia ai",
        "qualys",
        "quik hire staffing",
        "randstad digital americas",
        "rapidscale",
        "remotehunter",
        "revature",
        "sandvik",
        "sandvik coromant",
        "siemens energy",
        "skillstorm",
        "smart working",
        "sundayy",
        "tech consulting",
        "trace systems inc.",
        "turing",
        "world wide technology",
        "zachary piper solutions",
    }


