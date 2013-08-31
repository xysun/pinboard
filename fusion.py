# use google fusion table to serve as database
# sample code from google: https://developers.google.com/fusiontables/docs/samples/python

from api_secret import client_id, client_secret, redirect_uri, api_key, tableid
import urllib.parse, urllib.request, json, http.client

class API:
    def __init__(self):
        self.access_token = ''
        self.params = ''
        self.api_key = api_key

    def main(self):
        print('copy and paste the url below into browser')
        print('https://accounts.google.com/o/oauth2/auth?%s%s%s%s' % \
            ('client_id=%s&' % (client_id),
            'redirect_uri=%s&' % (redirect_uri),
            'scope=https://www.googleapis.com/auth/fusiontables&',
            'response_type=code'))
        code = input('enter code:\n')
        data = urllib.parse.urlencode({
            'code':code,
            'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':redirect_uri,
            'grant_type':'authorization_code'
        })

        serv_req = urllib.request.urlopen(url='https://accounts.google.com/o/oauth2/token', data=data.encode())

        response = serv_req.read()
        tokens = json.loads(response.decode())
        access_token = tokens['access_token']
        self.access_token = access_token
        self.params = '?key=%s&access_token=%s' % (self.api_key, self.access_token)
    
    def runRequest(self, method, url, data=None, headers=None):
        request = http.client.HTTPSConnection('www.googleapis.com')

        if data and headers: 
            request.request(method, url, data, headers)
        elif headers: # for inserting a row
            request.request(method, url, headers=headers)
        else:
            request.request(method, url)
        response = request.getresponse()
        print(response.status, response.reason)
        response = response.read()
        print (response)
        return response

    # retrieve a table
    def retrieveTable(self, table_id):
        print("GET TABLE")
        return self.runRequest(
            'GET',
            '/fusiontables/v1/tables/%s/%s' % \
            (table_id, self.params)
        )

    # create a column
    def insertColumn(self, table_id, cname, ctype):
        print('INSERT COLUMN')
        data = '''{
            "name":%s,
            "type":%s
        }''' % (cname, ctype)
        return self.runRequest(
            'POST', 
            '/fusiontables/v1/tables/%s/columns%s' % (table_id, self.params),
            data,
            headers = {'Content-Type':'application/json'}
        )

    # update a column
    # delete a column
    def deleteColumn(self, table_id, column_id):
        print('DELETE COLUMN')
        return self.runRequest(
            'DELETE',
            '/fusiontables/v1/tables/%s/columns/%s%s' % (table_id, column_id, self.params)
        )
    # querying for data, GET
    def getRows(self, sql):
        print('GET ROWS')
        query = urllib.parse.urlencode(
            [('sql',sql), ('key', self.api_key), ('access_token', self.access_token)]
        )
        return self.runRequest(
            'GET',
            '/fusiontables/v1/query?%s' % query
        )

    # insert/delete/update a row, POST
    def postRows(self, sql):
        print('INSERT ROWS')
        query = urllib.parse.urlencode(
            [('sql',sql), ('key', self.api_key), ('access_token', self.access_token)]
        )
        return self.runRequest(
            'POST',
            '/fusiontables/v1/query?%s' % query,
            headers={'Content-length':0}
        )

