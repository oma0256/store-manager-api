"""
File to handle my database operations
"""
commands = (
    """
    CREATE TABLE IF NOT EXISTS public.users(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.products(
        id SERIAL PRIMARY KEY,
        name VARCHAR UNIQUE NOT NULL,
        unit_cost INTEGER NOT NULL,
        quantity INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.sales(
        id SERIAL PRIMARY KEY,
        attendant INTEGER REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
        cart_items VARCHAR NOT NULL,
        total VARCHAR NOT NULL
    )
    """
    )
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash
from api.__init__ import app


class DB:
    def __init__(self):
        try:
            if app.config["TESTING"]:
                self.conn = psycopg2.connect(host="localhost", 
                                             database="test_db", 
                                             user="postgres", 
                                             password="pass1234")
            else:
                self.conn = psycopg2.connect(host="localhost", 
                                             database="manager", 
                                             user="postgres", 
                                             password="pass1234")
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.conn.autocommit = True
        except as e:
            print("Failed to connect " + e)
        for command in commands:
            self.cur.execute(command)
            print(self.cur)
    
    def create_admin(self):
        """Function to create an admin"""
        self.cur.execute("INSERT INTO users(first_name, last_name, email, password, is_admin) VALUES (%s, %s, %s, %s, %s)",
                         ("admin", "owner", "admin@email.com", generate_password_hash("pass1234"), True))
    
    def get_user(self, email):
        self.cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        return self.cur.fetchone()
    
    def create_user(self, user):
        self.cur.execute("INSERT INTO users(first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                         (user.first_name, user.last_name, user.email, user.password))
    
    def delete_attendants(self):
        self.cur.execute("DELETE FROM users WHERE is_admin=%s", (False,))
    
    def delete_products(self):
        self.cur.execute("TRUNCATE products")
    
    def add_product(self, product):
        self.cur.execute("INSERT INTO products(name, unit_cost, quantity) VALUES (%s, %s, %s)", 
                         (product.name, product.unit_cost, product.quantity))
    
    def get_product_by_name(self, name):
        self.cur.execute("SELECT * FROM products WHERE name=%s", (name,))
        return self.cur.fetchone()
    
    def get_products(self):
        self.cur.execute("SELECT * FROM products")
        return self.cur.fetchall()
    
    def get_product_by_id(self, product_id):
        self.cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        return self.cur.fetchone()
    
    def update_product(self, name, unit_cost, quantity, product_id):
        self.cur.execute("UPDATE products SET name=%s, unit_cost=%s, quantity=%s WHERE id=%s", 
                         (name, unit_cost, quantity, product_id))
    
    def delete_product(self, product_id):
        self.cur.execute("DELETE FROM products WHERE id=%s", (product_id,))

    def delete_sales(self):
        self.cur.execute("TRUNCATE sales")

    def add_sale(self, attendant, products, total):
        self.cur.execute("INSERT INTO sales(attendant, cart_items, total) VALUES (%s, %s, %s)",
                     (attendant, products, total))

    def get_sale_records(self):
        self.cur.execute("SELECT * FROM sales")
        return self.cur.fetchall()

    def get_single_sale(self, sale_id):
        self.cur.execute("SELECT * FROM sales WHERE id=%s", (sale_id,))
        return self.cur.fetchone()
