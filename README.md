This is my local 'pinterest' collection, a tag-based bookmark system using python and sqlite3. 

![screenshot](screenshot.png?raw=true)

* Read entries are marked gray.

### Philosophy

* Minimalist. 
* Local, non-social. 

    I don't need sync since I never read long articles on my phone. And all my development folders are Dropbox-ed. 

### Usage:

`python3 init.py` : initiate the database

`python3 shell.py add` : add a record.

`python3 shell.py show` : generate `index.html` file and open in Chrome

You can always directly hack the database through `sqlite3 bookmarks.db`.


Work in progress. 

### Useful linkes:

* [Google maps documentation](https://developers.google.com/maps/documentation/javascript/tutorial)
* [Google fusion documentation](https://developers.google.com/fusiontables/docs/v1/using)
