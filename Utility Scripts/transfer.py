#script to convert legacy data.json to newer sqlite installation
import sqlite3, os.path, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "imagestore.db")
conn = sqlite3.connect(db_path, isolation_level=None)
c = conn.cursor()

with open('data.json') as f:
    data = json.load(f)
for i, info in enumerate(data, start=0):
    c.execute('INSERT INTO images VALUES (?,?,?,?)', (data[i]['Username'], data[i]['UID'], data[i]['Description'], data[i]['Link']))

print("done.")