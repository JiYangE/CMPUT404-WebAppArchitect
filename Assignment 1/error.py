# The following response content is from https://hg.python.org/cpython/file/2.7/Lib/BaseHTTPServer.py
responses = {
    404: ('Not Found', 'Nothing matches the given URI')
    }

class ErrorHandler(Exception):
    
    # Setup an HTML template to display 404 error response
    TEMPLATE = \
    """
    <head>
        <title>404 Not Found</title>
            <meta http-equiv="Content-Type"
            content="text/html;charset=utf-8"/>
            <!-- check conformance at http://validator.w3.org/check -->
            <link rel="stylesheet" type="text/css" href="deep.css">
    </head>

    <body>
        <hr>
        <div class="eg">
            <h1 style="color:black">404 Not Found</h1>
            <hr>
            <p>Nothing matches the given URI.
        </div>
        <hr>
    </body>
    """
    
    # Construtor method for setting required fields
    def __init__(self, status_code):
        # should be 404 for our case
        self.status_code = status_code
        self.status_msg = responses[status_code][0]
        self.status_reason = responses[status_code][1]