CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
	colour VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS item (
    item_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id) ON DELETE CASCADE,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    date_added TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS purchase (
    user_id INTEGER REFERENCES "user"(user_id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES item(item_id) ON DELETE CASCADE,
    date TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, item_id)
);

CREATE TABLE IF NOT EXISTS session (
    token VARCHAR(64) PRIMARY KEY NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT now()
);
