DROP TABLE IF EXISTS token;

CREATE TABLE token (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_token TEXT UNIQUE NOT NULL
);
