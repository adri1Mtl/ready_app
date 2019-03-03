import tornado.ioloop
import tornado.web
from tornado.httputil import HTTPHeaders
import csv

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Index of app. Please launch a /count request!')

class CountHandler(tornado.web.RequestHandler):
    def get(self):
        filters = self.request.arguments #get request arguments
        dictOfSearchCriterias = {} #dictionary of search criterias
        self.set_header("Content-Type", "application/json")#one automated test may fail because of "application/json; charset UTF-8" in header
        for key,value in filters.items():              
            arg = value[0].decode()
            dictOfSearchCriterias[key] = arg 
        with open("dogs.csv","r") as csv_file:
            csvFile = list(csv.reader(csv_file, delimiter=','))
            columns = []
            listOfUnknowFields = []
            count = 0
            for column in csvFile[0]: #get all columns names
                columns.append(column)
            for key,value in dictOfSearchCriterias.items():
                try:
                    index = columns.index(key)
                except ValueError:
                    listOfUnknowFields.append(key)
            if listOfUnknowFields: #if not empty
                response = { "unknown fields": sorted(listOfUnknowFields) } #sort alphabetically
                self._status_code = 400
                self.write(response)
            else: #actual search 
                for row in csvFile[1:]: #for each row
                    fullMatch = True
                    for key,value in dictOfSearchCriterias.items():
                        index = columns.index(key) #look at the appropriate column
                        if not row[index].lower() == value.lower(): #if the value is different from request argument, it is not a match. (Ignore case)
                            fullMatch = False
                            break
                    if fullMatch: count +=1 #add 1 to count if the row is a match
                response = { "count": count }
                self.write(response) #return JSON response

if __name__ == "__main__":
    app = tornado.web.Application([tornado.web.url(r"/", MainHandler),tornado.web.url(r"/count", CountHandler)])
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()    

# if you need to deploy as a WSGI application you need to use the following line instead:
# application = tornado.wsgi.WSGIApplication([(r"/", MainHandler),(r"/count", CountHandler),])
# and you need to copy the code in your WSGI configuration file.