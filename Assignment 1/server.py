#  coding: utf-8 

import SocketServer
import os 
from error import ErrorHandler


# Copyright 2013 Abram Hindle, Eddie Antonio Santos Ji Yang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#** User Stories
#   - As a user I want to view files in ./www via a webbrowser
#   - As a user I want to view files in ./www via curl
#   - As a webserver admin I want to serve HTML and CSS files from ./www
#   - As a webserver admin I want ONLY files in ./www and deeper to be
#     served.
#
#** Requirements
#   - [ ] The webserver can serve files from ./www
#   - [ ] The webserver can be run using the runner.sh file
#   - [ ] The webserver can pass all the tests in freetests.py
#   - [ ] The webserver can pass all the tests in not-free-tests.py
#     (you don't have this one!)
#   - [ ] The webserver supports mime-types for HTML
#   - [ ] The webserver supports mime-types for CSS
#   - [ ] The webserver can return index.html from directories (paths
#     that end in /)
#   - [ ] The webserver can server 404 errors for paths not found
#   - [ ] The webserver works with Firefox and Chromium
#     http://127.0.0.1:8080/
#   - [ ] The webserver can serve CSS properly so that the front page
#     has an orange h1 header.
#   - [ ] I can check out the source code via an HTTP git URL
#   - [ ] Provide a screenshot (commit and push it!) of Firefox at
#     http://127.0.0.1:8080/ and http://127.0.0.1:8080/deep

# The following response content(HTTP_CODE) is from https://hg.python.org/cpython/file/2.7/Lib/BaseHTTPServer.py
HTTP_CODE = {
    200: ('OK', 'Request fulfilled, document follows'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    404: ('Not Found', 'Nothing matches the given URI'),
}
MIME_TYPE = {
    "CSS": "text/css",
    "HTML": "text/html"
}


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def request_analysis(self, req):
        req_method, root_dir = self.check_head(req)
        # comment lines below when submitting, for test only
        # req_method = "POST"
        # protocal_version = "HTTP/0.9"
        method = getattr(self, req_method)
        method(root_dir)   

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall("OK")
        try:
            self.request_analysis(self.data)
        except ErrorHandler as error:
            self.handle_error(error)
    
    def abs_path(self, target_file, path):
        if not target_file[-1] == ('/'):
            self.redirect(path + '/')
        else:
            pass
    
    def check_head(self, request):
        # head_line should contain 3 parts, request method, root_dir and protocal name
        head_line = request.splitlines()[0]
        # expect "GET / HTTP/1.1" in args
        req_method, root_dir, protocal_version = head_line.split(" ")
        # handle exceptions
        return req_method.lower(), root_dir

    # GET method
    def get(self, filename):
        # Expect result on my Mac:
        # ROOT_PATH = /Users/YJ/Documents/CMPUT404-assignment-webserver/www
        # DESTINATION = /Users/YJ/Documents/CMPUT404-assignment-webserver/www/index.html
        # ABSOLUTEPATH = /Users/YJ/Documents/CMPUT404-assignment-webserver/www/index.html
        # print "\n==================\nGetting %s\n" % filename
        root_path = os.path.abspath("www")
        # print "ROOT_PATH = " + root_path
        target_file = root_path + filename
        # print "DESTINATION = " + target_file
        absolute_path = os.path.abspath(target_file)
        # print "ABSOLUTEPATH = " + absolute_path
        
        # check whether the abs_path is what we want 
        # handle 404 error (not found)
        if not absolute_path.startswith(root_path):
            # print "ABSOLUTE_PATH error"
            raise ErrorHandler(404)
        if os.path.isdir(absolute_path):
            self.abs_path(target_file, filename)
            absolute_path = os.path.join(absolute_path, 'index.html')
        if not os.path.exists(absolute_path):
            raise ErrorHandler(404)
  
        # https://docs.python.org/2/library/mimetypes.html
        mime_type = MIME_TYPE.get(absolute_path.split('.')[-1].upper(), MIME_TYPE['HTML'])
        
        # load HTML page then retrieve
        page_content = open(absolute_path).read()
        self.deal_response(200, mime_type, page_content)
        
    # https://en.wikipedia.org/wiki/HTTP_301        
    def redirect(self, filename):
        response = "HTTP/1.1 %d %s\r\n" % (301, "Good!")
        response += "Location: %s\r\n\r\n" % filename
        # print response
        self.request.sendall(response)
        
    # https://en.wikipedia.org/wiki/HTTP_301    
    def deal_response(self, code, mime_type, content=''):
        response = "HTTP/1.1 %d %s \n" % (code, HTTP_CODE[code][0])
        response += "Content-Length: %d \r\n" % len(content)
        response += "Content-Type: %s \r\n" % mime_type
        response += "Connection: close \r\n\r\n"
        response += content + "\r\n"
        # print response
        self.request.sendall(response)
        
    def handle_error(self, error):
        # Send error
        self.deal_response(error.status_code, MIME_TYPE['HTML'], error.TEMPLATE)

            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()