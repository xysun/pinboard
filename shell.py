# interactive shell
import sqlite3, sys
from datetime import date

def add(conn):
    '''
    add a record 
    '''
    c = conn.cursor()
    with open('meta', 'r') as f:
        l = f.readline()

    i = str(int(l) + 1)

    time = date.today().isoformat()
    print("Link:")
    link = input()
    print("Title:")
    title = input().lower()
    print("Description:")
    desc = input().lower()
    print("Tags separated by spaces:")
    tags = input().lower().split()

    records = [(i + '_' + tag, time, link, title, desc, tag, 0, "") for tag in tags]

    for record in records:
        c.execute('insert into records values (?,?,?,?,?,?,?,?)', record)
    
    conn.commit()

    with open('meta', 'w') as f:
        f.write(i)
    
    print("records added")

def main():
    if len(sys.argv) < 2:
        print("usage: python3 shell.py [ADD|]", file = sys.stderr)
        sys.exit(2)

    conn = sqlite3.connect('bookmarks.db')
    
    if sys.argv[1].upper() == 'ADD':
        add(conn)
    
    conn.close()

if __name__ == '__main__':
    main()
