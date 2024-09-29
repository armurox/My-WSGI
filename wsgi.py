from wsgiref.simple_server import make_server

def application(environ, start_response):
    response_body = [
       ('%s: %s\n' % (key, value)).encode('utf-8') for key, value in sorted(environ.items())
    ]
    
    content_length = sum([len(s) for s in response_body])
    
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(content_length)),
    ]
    
    start_response(status, response_headers)
    return response_body

with make_server('127.0.0.1', 8000, application) as httpd:
    print('Serving on port 8000')
    httpd.serve_forever()