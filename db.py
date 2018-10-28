"""
File to handle my database operations
"""
"""
CREATE TABLE public.users(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL
);
"""
"""
CREATE TABLE public.products(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    unit_cost VARCHAR NOT NULL,
    quantity VARCHAR NOT NULL
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
import psycopg2
from psycopg2.extras import DictCursor


class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(host="localhost", database="manager", user="postgres", password="pass1234")
            self.cur = self.conn.cursor(cursor_factory=DictCursor)
            self.conn.autocommit = True
        except:
            print("Failed to connect")
