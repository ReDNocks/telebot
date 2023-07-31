import sqlite3 as sl

con = sl.connect('tgbase.db')

with con:
    # Пользователи
    con.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            post INTEGER,
            tel TEXT,
            UNIQUE(tel)
        );
    """)
    # Заказы
    con.execute("""
        CREATE TABLE IF NOT EXISTS ORDERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time_deliv TIME,
            USER INTEGER,
            payment BOOLEAN
        );
    """)
    #Корзина
    con.execute("""
        CREATE TABLE IF NOT EXISTS BASKET (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dishes INTEGER, 
            kol_vo_dishes INTEGER,
            orders INTEGER
        );
    """)
    #Блюда
    con.execute("""
        CREATE TABLE IF NOT EXISTS DISHES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight INTEGER,
            price FLOAT,
            description LONGTEXT,
            photo IMAGE,
            category INTEGER,
            cooking_time DATATIME,
            rating INTEGER
        );
    """)
    #Категория блюд
    con.execute("""
        CREATE TABLE IF NOT EXISTS CATEGORY (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
    """)




sql_insert = "INSERT OR IGNORE INTO CATEGORY (id, name) values(?, ?)"
# INSERT OR IGNORE - модификатор для уникальных значений
with con:
    con.execute(sql_insert, [1, "Горячее"])
    # executemany - для двумерного
    con.execute(sql_insert, [2, "Напитки"])


# with con:
#     data = con.execute("SELECT * FROM SERVICES").fetchall()
#     print(data)
#     # data = con.execute("PRAGMA table_info(CLIENTS);").fetchall()
#     # for x in data:
#     #     print(x[1])