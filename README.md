# Movie API → MySQL → Pandas Mini Project

This end-to-end project collects movie data from the official TMDB API, stores it in MySQL tables, extracts it using Pandas, cleans the records, saves the cleaned data back to MySQL, and performs basic EDA.

## Requirements
- Python 3.10+
- MySQL Server / MySQL Workbench
- TMDB API Read Access Token

## Setup
1. Unzip the project.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install packages: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your token and MySQL credentials.
5. Execute `sql/schema.sql` in MySQL Workbench.
6. Run from the project root: `python -m src.run_pipeline`
7. Open the notebook: `jupyter notebook notebooks/data_cleaning_eda.ipynb`

Get a TMDB API token at https://www.themoviedb.org/settings/api. Documentation: https://developer.themoviedb.org/docs/getting-started. Do not share your token or commit `.env` to GitHub.

## Tables
- `movies_raw`: API movie metadata
- `genres`: genre lookup values
- `movie_genres`: movie-to-genre relationships
- `movies_cleaned`: cleaned analytical records

## Pipeline
TMDB API → Python requests → MySQL → Pandas cleaning → cleaned MySQL table + CSV → EDA charts.

The zip contains no real API data or credentials. Respect TMDB's terms, attribution requirements, and rate limits.
