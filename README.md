# Job Scraper

A Python pipeline that scrapes automation, DevOps, cloud, platform, and network engineering job listings from **Indeed** and **LinkedIn** across North Carolina and remote locations. Results are saved to a local SQLite database and a CSV file.

---

## Features

- Searches multiple job titles and keywords in a single run
- Scrapes Indeed and LinkedIn via the [jobspy](https://github.com/Bunsly/JobSpy) library
- Filters out irrelevant titles (e.g. PLC, Manufacturing) and known low-signal companies
- Deduplicates listings by job ID
- Outputs results to `jobs.db` (SQLite) and `jobs_raw_table.csv`
- Each run starts fresh — existing output files are removed at startup

---

## Project Structure

```
├── main.py            # Entry point — orchestrates searches and writes output
├── utils/
│   └── scraper.py     # ScraperJobs class and ScrapeConfig dataclass
├── jobs.db            # SQLite output (generated at runtime, gitignored)
├── jobs_raw_table.csv # CSV output (generated at runtime, gitignored)
└── README.md
```

---

## Requirements

- Python 3.9+
- [jobspy](https://github.com/Bunsly/JobSpy)
- pandas

Install dependencies:

```bash
pip install jobspy pandas
```

---

## Usage

```bash
python main.py
```

The script will:
1. Delete any existing `jobs.db` and `jobs_raw_table.csv`
2. Loop over each location and search term
3. Scrape Indeed and LinkedIn for matching postings from the last 4 hours
4. Append results to `jobs.db` and `jobs_raw_table.csv`

---

## Configuration

All search parameters are defined at the top of `main.py`:

| Parameter   | Default                                      | Description                          |
|-------------|----------------------------------------------|--------------------------------------|
| `searches`  | 11 automation/DevOps queries                 | List of job search terms             |
| `sites`     | `["indeed", "linkedin"]`                     | Job boards to scrape                 |
| `locations` | Raleigh NC, Durham NC, Chapel Hill NC, Remote| Locations to search                  |
| `results`   | `1000`                                       | Max results per search/site          |
| `hours_old` | `4`                                          | Max age of listings in hours         |
| `country`   | `"USA"`                                      | Country filter (Indeed only)         |

---

## Output

### `jobs.db`
A SQLite database with a `jobs` table. Connect with any SQLite client or via Python:

```python
import sqlite3, pandas as pd
conn = sqlite3.connect("jobs.db")
df = pd.read_sql("SELECT * FROM jobs", conn)
```

### `jobs_raw_table.csv`
A flat CSV of all scraped results, with one header row and results appended per location.

**Columns retained:**
`id`, `site`, `job_url`, `job_url_direct`, `title`, `company`, `location`, `date_posted`, `is_remote`, `num_urgent_words`, `benefits`, `job_url_hyper`

---

## Filtering

Listings are filtered at scrape time in `scraper.py`:

- **Titles excluded:** PLC, Manufacturing, Mechanical, Electrical, Civil, Project
- **Companies excluded:** Epic, Piper Companies, Turing
- **Remote location:** When searching "Remote", only rows where `is_remote=True` are kept

To customize filters, edit `_TITLES_TO_DROP` and `_COMPANIES_TO_DROP` in `scraper.py`.

---

## Notes

- `jobs.db` and `jobs_raw_table.csv` are gitignored as they are runtime outputs, not source artifacts.
- LinkedIn and Indeed scraping errors are caught per search term and logged to stdout — they do not halt the pipeline.
