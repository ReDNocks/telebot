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
            id_vk TEXT,
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
            payment BOOLEAN(0),
            date DATETIME,
            FOREIGN KEY (user)  REFERENCES USERS(id)
        );
    """)

    # Товары
    con.execute("""
            CREATE TABLE IF NOT EXISTS GOODS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                dishes INTEGER, 
                kol_vo_dishes INTEGER,
                orders INTEGER,
                FOREIGN KEY (dishes)  REFERENCES DISHES (id),
                FOREIGN KEY (orders)  REFERENCES ORDERS (id)
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
            photo LONGTEXT,
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

    # Рейтинг блюд
    con.execute("""
            CREATE TABLE IF NOT EXISTS RATING(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                dish INTEGER,
                rating INTEGER,
                FOREIGN KEY (dish)  REFERENCES DISHES (id)
            );
        """)

    # Коментарии блюд
    con.execute("""
            CREATE TABLE IF NOT EXISTS COMMENTS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                dish INTEGER,
                id_users INTEGER,
                comments LONGTEXT,
                FOREIGN KEY (dish)  REFERENCES DISHES (id)
                FOREIGN KEY (id_users)  REFERENCES USERS (id)
            );
        """)

