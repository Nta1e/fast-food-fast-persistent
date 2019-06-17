from app.models.database import Database
from app import app

db = Database(app)


def main():

    db.query("""DROP TABLE IF EXISTS users CASCADE""")
    db.query("""DROP TABLE IF EXISTS menu CASCADE""")
    db.query("""DROP TABLE IF EXISTS orders CASCADE""")

    db.query(""" CREATE TABLE users(
            id serial PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            admin BOOLEAN DEFAULT 'false'
            )
            """)

    db.query(""" CREATE TABLE menu(
            meal_id serial PRIMARY KEY,
            menu_item VARCHAR(255),
            price INTEGER
        )
        """)

    db.query(""" CREATE TABLE orders(
            id serial PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            menu_id INTEGER REFERENCES menu(meal_id) ON DELETE CASCADE,
            order_made VARCHAR(255),
            location VARCHAR(255),
            comment VARCHAR(500),
            made_by VARCHAR(255),
            status VARCHAR(255) DEFAULT 'New',
            order_date TIMESTAMP DEFAULT NOW()
        )
            """)

    db.conn.commit()
    db.conn.close()

if __name__ == "__main__":
    main()

print("...........................TABLES CREATED .................................")
