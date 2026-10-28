CREATE DATABASE IF NOT EXISTS movie_analytics
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movie_analytics;

CREATE TABLE IF NOT EXISTS movies_raw (
  movie_id BIGINT PRIMARY KEY,
  title VARCHAR(500),
  release_date VARCHAR(30),
  rating DECIMAL(4,2),
  vote_count INT,
  popularity DECIMAL(14,4),
  overview TEXT,
  language VARCHAR(10),
  collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genres (
  genre_id INT PRIMARY KEY,
  genre_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS movie_genres (
  movie_id BIGINT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY (movie_id, genre_id),
  FOREIGN KEY (movie_id) REFERENCES movies_raw(movie_id) ON DELETE CASCADE,
  FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS movies_cleaned (
  movie_id BIGINT PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  release_date DATE NULL,
  rating DECIMAL(4,2) NULL,
  vote_count INT NULL,
  popularity DECIMAL(14,4) NULL,
  overview TEXT,
  language VARCHAR(10),
  cleaned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_cleaned_rating (rating),
  INDEX idx_cleaned_release_date (release_date)
);
