CREATE_TABLE_REGISTRATION = """
    CREATE TABLE IF NOT EXISTS registration
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id VARCHAR(255),
    firstname VARCHAR(255),
    UNIQUE (telegram_id)
    )
"""

INSERT_INTO_TABLE_REGISTRATION = """
    INSERT OR IGNORE INTO registration(telegram_id, firstname)
    VALUES (?, ?)
"""

