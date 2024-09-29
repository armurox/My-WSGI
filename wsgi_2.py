#!/usr/bin/env python

from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
html = """
<html>
<body>
   <form method="get" action="">
        <p>
           Age: <input type="text" name="age" value="%(age)s">
        </p>
        <p>
            Hobbies:
            <input
                name="hobbies" type="checkbox" value="software"
                %(checked-software)s
            > Software
            <input
                name="hobbies" type="checkbox" value="tuning"
                %(checked-tuning)s
            > Auto Tuning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: %(age)s<br>
        Hobbies: %(hobbies)s
    </p>
</body>
</html>
"""

def application (environ, start_response):

    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])

    # As there can be more than one value for a variable then
    # a list is provided as a default value.
    age = d.get('age', [''])[0] # Returns the first age value
    hobbies = d.get('hobbies', []) # Returns a list of hobbies

    # Always escape user input to avoid script injection
    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % { # Fill the above html template in
        'checked-software': ('', 'checked')['software' in hobbies],
        'checked-tuning': ('', 'checked')['tuning' in hobbies],
        'age': age or 'Empty',
        'hobbies': ', '.join(hobbies or ['No Hobbies?'])
    }
    
    response_body = response_body.encode('utf-8')

    status = '200 OK'

    # Now content type is text/html
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

with make_server('localhost', 8051, application) as httpd:
    httpd.serve_forever()