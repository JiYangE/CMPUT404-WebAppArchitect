#!/usr/bin/env python

from __future__ import print_function

import sys, os, cgi


print("Content-type: text/html")
print("")
print("<html><body><form method='post'><input name='x'></form></body></html>")

# print(os.environ)
print("")

form = cgi.FieldStorage()
# Escaping HTML
print(cgi.escape(form.getvalue('x')))
