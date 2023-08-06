import sqlite3 as sl

con = sl.connect('tgbase.db')

with con:
    # Пользователи
    con.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_telegram TEXT,
            name TEXT,
            address TEXT,
            post INTEGER,
            tel TEXT,
            UNIQUE(tel),
            UNIQUE(id_telegram)
        );
    """)
    # Заказы
    con.execute("""
        CREATE TABLE IF NOT EXISTS ORDERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time_deliv TIME,
            user INTEGER,
            payment BOOLEAN,
            FOREIGN KEY (user)  REFERENCES USERS(id)
        );
    """)
    #Корзина
    con.execute("""
        CREATE TABLE IF NOT EXISTS BASKET (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            goods INTEGER,
            orders INTEGER,
            FOREIGN KEY (orders)  REFERENCES ORDERS (id),
            FOREIGN KEY (goods)  REFERENCES GOODS (id)
        );
    """)

    con.execute("""
            CREATE TABLE IF NOT EXISTS GOODS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                dishes INTEGER, 
                kol_vo_dishes INTEGER,
                user_id INTEGER,
                FOREIGN KEY (user_id)  REFERENCES USERS (id),
                FOREIGN KEY (dishes)  REFERENCES DISHES (id)
            );
        """)

    #Блюда
    con.execute("""
        CREATE TABLE IF NOT EXISTS DISHES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight TEXT,
            price TEXT,
            description LONGTEXT,
            photo IMAGE,
            category INTEGER,
            cooking_time DATATIME,
            rating INTEGER,
            stoped BOOLEAN,
            FOREIGN KEY (category)  REFERENCES CATEGORY (id)
             
        );
    """)
    #Категория блюд
    con.execute("""
        CREATE TABLE IF NOT EXISTS CATEGORY (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
    """)



