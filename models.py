import sqlite3
import os

DATABASE = 'company_info.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    if not os.path.exists(DATABASE):
        with get_db_connection() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS documents
                            (id INTEGER PRIMARY KEY, title TEXT, content TEXT, file_path TEXT)''')

def add_document_to_db(title, content, file_path=None):
    with get_db_connection() as conn:
        conn.execute("INSERT INTO documents (title, content, file_path) VALUES (?, ?, ?)", 
                     (title, content, file_path))
        conn.commit()

def search_documents(query):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM documents WHERE content LIKE ?", ('%' + query + '%',))
        return cursor.fetchall()

def summarize_content(content):
    prompt = f"Summarize the following document:\n\n{content}\n\nSummary:"
    return query_llm(prompt)
