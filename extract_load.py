import time
import requests
import pandas as pd
from sqlalchemy import text
from src.config import TOKEN, PAGES, BASE_URL, get_engine, validate_config

def get_json(session, endpoint, params=None):
    response = session.get(
        f"{BASE_URL}/{endpoint.lstrip('/')}",
        params=params or {},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

def main():
    validate_config()
    engine = get_engine()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {TOKEN}",
        "accept": "application/json",
    })

    records = []
    for page in range(1, PAGES + 1):
        payload = get_json(session, "movie/popular",
                           {"language": "en-US", "page": page})
        page_records = payload.get("results", [])
        records.extend(page_records)
        print(f"Fetched page {page}/{PAGES}: {len(page_records)} movies")
        time.sleep(0.25)

    if not records:
        raise RuntimeError("No movies returned by the API.")

    frame = pd.json_normalize(records)
    mapping = {
        "id": "movie_id", "title": "title", "release_date": "release_date",
        "vote_average": "rating", "vote_count": "vote_count",
        "popularity": "popularity", "overview": "overview",
        "original_language": "language",
    }
    for col in mapping:
        if col not in frame.columns:
            frame[col] = None
    movies = frame[list(mapping)].rename(columns=mapping)
    movies = movies.drop_duplicates("movie_id", keep="last")
    movies["movie_id"] = pd.to_numeric(movies["movie_id"], errors="coerce")
    movies = movies.dropna(subset=["movie_id"])
    movies["movie_id"] = movies["movie_id"].astype("int64")
    rows = movies.where(pd.notna(movies), None).to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO movies_raw
              (movie_id,title,release_date,rating,vote_count,popularity,overview,language)
            VALUES
              (:movie_id,:title,:release_date,:rating,:vote_count,:popularity,:overview,:language)
            ON DUPLICATE KEY UPDATE
              title=VALUES(title), release_date=VALUES(release_date),
              rating=VALUES(rating), vote_count=VALUES(vote_count),
              popularity=VALUES(popularity), overview=VALUES(overview),
              language=VALUES(language)
        """), rows)
    print(f"Loaded/updated {len(rows)} raw movie records.")

    genre_payload = get_json(session, "genre/movie/list", {"language": "en"})
    genres = [{"genre_id": int(g["id"]), "genre_name": g["name"]}
              for g in genre_payload.get("genres", [])]
    with engine.begin() as conn:
        if genres:
            conn.execute(text("""
                INSERT INTO genres (genre_id,genre_name)
                VALUES (:genre_id,:genre_name)
                ON DUPLICATE KEY UPDATE genre_name=VALUES(genre_name)
            """), genres)

        movie_ids = [int(x) for x in movies["movie_id"].tolist()]
        for movie_id in movie_ids:
            conn.execute(text("DELETE FROM movie_genres WHERE movie_id=:id"),
                         {"id": movie_id})
        links = [{"movie_id": int(m["id"]), "genre_id": int(g)}
                 for m in records for g in (m.get("genre_ids") or [])]
        links = list({(x["movie_id"], x["genre_id"]): x for x in links}.values())
        if links:
            conn.execute(text("""
                INSERT IGNORE INTO movie_genres (movie_id,genre_id)
                VALUES (:movie_id,:genre_id)
            """), links)
    print(f"Loaded {len(genres)} genres and movie-genre relationships.")

if __name__ == "__main__":
    main()
