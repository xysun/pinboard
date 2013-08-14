import sqlite3, sys, os
from datetime import date

def display(conn):
    
    def buildline(link, title, date, description, tags):
        line = '\n<p class="record">\n<a href="' + link + '" target = "_blank">' + title + '</a>\n'
        line += date + '\n'
        for tag in tags:
            line += '[' + tag + '] '
        line += '\n'
        if len(description) > 0:
            line += '\n' + description + '\n'
        line += '</p>\n'
        return line

    head = '''
<!DOCTYPE HTML>
<html>
<head>
<link rel="stylesheet" type="text/css" href="index.css">
</head>
<body>
    '''
    
    footer = '''
</body>
</html>
    '''
    
    c = conn.cursor()
    print("your sql query (default select *) :")
    sql = input()
    if len(sql) == 0: #default
        sql = 'select * from records order by time desc' 
    if not sql.lstrip().upper().startswith('SELECT * '):
        print('only support SELECT * ')
        sys.exit(2)
    c.execute(sql)
    
    fr = c.__next__()
    link = fr[2]
    date = fr[1]
    title = fr[3]
    description  = fr[4]
    tags = set([fr[5]])

    with open('index.html', 'w') as f:
        f.write(head)
        f.write("\nQuery: " + sql + '\n')
        f.write("<hr />")
        for row in c:
            if row[2] == link: # same records
                tags.add(row[5])
                next
            else:
                line = buildline(link, title, date, description, tags)
                f.write(line)

                link = row[2]
                date = row[1]
                title = row[3]
                description = row[4]
                tags = set([row[5]])
        
        line = buildline(link, title, date, description, tags)
        f.write(line)
        f.write(footer)                 
    
    # open in chrome
    os.system('open -a Google\ Chrome index.html')

def add(conn):
    '''
    add a record 
    '''
    c = conn.cursor()
    c.execute('select count(*) from records')
    l = c.__next__()[0]
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

    print("records added")



def main():
    if len(sys.argv) < 2:
        print("usage: python3 shell.py [ADD|DISPLAY]", file = sys.stderr)
        sys.exit(2)

    conn = sqlite3.connect('bookmarks.db')
    
    if sys.argv[1].upper() == 'ADD':
        add(conn)
    elif sys.argv[1].upper() == 'SHOW':
        display(conn)

    conn.close()

if __name__ == '__main__':
    main()
