import pandas as pd
from sqlalchemy import text
from src.config import get_engine

QUERY = """
SELECT movie_id,title,release_date,rating,vote_count,popularity,overview,language
FROM movies_raw
"""

def clean_movies(frame):
    clean = frame.copy().drop_duplicates("movie_id", keep="last")
    for col in ["title", "overview", "language"]:
        clean[col] = clean[col].astype("string").str.strip().replace("", pd.NA)

    clean["release_date"] = pd.to_datetime(
        clean["release_date"], errors="coerce"
    ).dt.date
    for col in ["rating", "vote_count", "popularity"]:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")

    clean.loc[~clean["rating"].between(0, 10), "rating"] = float("nan")
    clean.loc[clean["vote_count"] < 0, "vote_count"] = float("nan")
    clean.loc[clean["popularity"] < 0, "popularity"] = float("nan")
    clean = clean.dropna(subset=["movie_id", "title"])
    clean["overview"] = clean["overview"].fillna("No overview available")
    clean["language"] = clean["language"].fillna("unknown")
    clean["movie_id"] = clean["movie_id"].astype("int64")
    clean["vote_count"] = clean["vote_count"].astype("Int64")
    clean["rating"] = clean["rating"].round(2)
    clean["popularity"] = clean["popularity"].round(4)
    return clean

def main():
    engine = get_engine()
    raw = pd.read_sql(QUERY, con=engine)
    print(f"Raw rows: {len(raw)}")
    print("Missing values before cleaning:\n", raw.isna().sum())
    clean = clean_movies(raw)
    print(f"Clean rows: {len(clean)}")
    print("Missing values after cleaning:\n", clean.isna().sum())

    rows = clean.where(pd.notna(clean), None).to_dict(orient="records")
    with engine.begin() as conn:
        if rows:
            conn.execute(text("""
                INSERT INTO movies_cleaned
                  (movie_id,title,release_date,rating,vote_count,popularity,overview,language)
                VALUES
                  (:movie_id,:title,:release_date,:rating,:vote_count,:popularity,:overview,:language)
                ON DUPLICATE KEY UPDATE
                  title=VALUES(title), release_date=VALUES(release_date),
                  rating=VALUES(rating), vote_count=VALUES(vote_count),
                  popularity=VALUES(popularity), overview=VALUES(overview),
                  language=VALUES(language)
            """), rows)
    clean.to_csv("data/movies_cleaned.csv", index=False)
    print("Saved movies_cleaned table and data/movies_cleaned.csv")

if __name__ == "__main__":
    main()
