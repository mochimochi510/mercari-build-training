--step5-1

-- CREATE TABLE IF NOT EXISTS items(
--     id INTEGER PRIMARY KEY,
--     name TEXT NOT NULL,
--     category TEXT NOT NULL,
--     image TEXT NOT NULL
-- );

-- step5-3
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    image TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);