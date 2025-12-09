import sqlite3
import os.path
from flask import g

DATABASE = 'database.db'
DB_TEMPLATE = 'db.template'

file_exists = lambda path: os.path.isfile(path)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts
    return db

def init_db(app):
    if file_exists(DB_TEMPLATE):
        return
    print("Init DB...")
    with app.app_context():
        db = get()
        with app.open_resource(DB_TEMPLATE , mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query(query, args=(), one=False):
    cur = get().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert(query, args=(), one=False):
    db = get()
    cur = db.execute(query, args)
    db.commit()
    cur.close()



if __name__ == '__main__':
    print("hello world")

