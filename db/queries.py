CREATE_TABLE_REGISTRATION = """
    CREATE TABLE IF NOT EXISTS registration
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id VARCHAR(255),
    firstname VARCHAR(255)
    )
"""

INSERT_INTO_TABLE_REGISTRATION = """
    INSERT INTO registration(telegram_id, firstname)
    VALUES (?, ?)
"""

CREATE_TABLE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    id_product VARCHAR(255),
    photo TEXT
    )
"""

INSERT_PRODUCTS = """
    INSERT INTO products(name, size, price, id_product, photo)
    VALUES (?, ?, ?, ?, ?)
"""

CREATE_TABLE_PRODUCTS_DETAILS = """
    CREATE TABLE IF NOT EXISTS products_details
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(255),
    info_product VARCHAR(255),
    id_product VARCHAR(255)
    )
"""

INSERT_PRODUCTS_DETAILS = """
    INSERT INTO products_details(category, info_product, id_product)
    VALUES (?, ?, ?)
"""

CREATE_TABLE_COLLECTION_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS collection_products
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        productid INTEGER NOT NULL,
        collection TEXT NOT NULL
    )
"""

INSERT_COLLECTION_PRODUCTS = """
    INSERT INTO collection_products (productid, collection)
    VALUES (?, ?)
"""

CREATE_TABLE_SHEETS = """
    CREATE TABLE IF NOT EXISTS sheets
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id VARCHAR(255),
        product_name VARCHAR(255),
        size VARCHAR(255),
        category VARCHAR(255),
        price VARCHAR(255)
    )
"""

INSERT_SHEET_DATA = """
    INSERT INTO sheets (telegram_id, product_name, size, category, price)
    VALUES (?, ?, ?, ?, ?)
"""
