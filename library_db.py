import sqlite3

def create_connection():
    conn = sqlite3.connect("library.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      title TEXT, 
                      author TEXT, 
                      year INTEGER, 
                      status TEXT)''')
    conn.commit()
    conn.close()

def add_book(title, author, year):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)", (title, author, year, 'Available'))
    conn.commit()
    conn.close()

def get_all_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, title, author, year):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?''',
                   (title, author, year, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
    conn.commit()
    conn.close()

def issue_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE books SET status = 'Issued' WHERE id = ?''', (book_id,))
    conn.commit()
    conn.close()

def return_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE books SET status = 'Available' WHERE id = ?''', (book_id,))
    conn.commit()
    conn.close()
