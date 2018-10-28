"""
File to handle my database operations
"""
"""
CREATE TABLE public.users(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL
);
"""
"""
CREATE TABLE public.products(
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    unit_cost INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);
"""
"""
CREATE TABLE public.sales(
    id SERIAL PRIMARY KEY,
    attendant VARCHAR NOT NULL,
    cart_items VARCHAR NOT NULL,
    total VARCHAR NOT NULL
);
"""
"""
INSERT INTO public.users(first_name, last_name, email, password, is_admin) VALUES ()
"""
import psycopg2
from psycopg2.extras import DictCursor
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
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
            self.conn.autocommit = True
        except:
            print("Failed to connect")
    
    def create_admin(self):
        """Function to create an admin"""
        self.cur.execute("INSERT INTO public.users(first_name, last_name, email, password, is_admin) VALUES (%s, %s, %s, %s, %s)",
                         ("admin", "owner", "admin@email.com", generate_password_hash("pass1234"), True))
    
    def get_user(self, email):
        self.cur.execute("SELECT * FROM public.users WHERE email=%s", (email,))
        return self.cur.fetchone()
    
    def create_user(self, user):
        self.cur.execute("INSERT INTO public.users(first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                         (user.first_name, user.last_name, user.email, user.password))
    
    def delete_attendants(self):
        self.cur.execute("DELETE FROM public.users WHERE is_admin=%s", (False,))
    
    def delete_products(self):
        self.cur.execute("TRUNCATE public.products")
