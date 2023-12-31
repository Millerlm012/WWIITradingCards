-- decks
CREATE TABLE decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    publisher TEXT NOT NULL,
    deck_name TEXT NOT NULL,
    deck_number INTEGER NULL,
    url TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- cards
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id TEXT NOT NULL,
    card_name TEXT NOT NULL,
    url TEXT NOT NULL,
    front_image_url TEXT NULL,
    back_image_url TEXT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id)
        REFERENCES decks (id)
);

-- errors
CREATE TABLE errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id INTEGER NOT NULL,
    card_id TEXT NOT NULL,
    error TEXT NOT NULL,
    FOREIGN KEY (deck_id)
        REFERENCES decks (id)
)