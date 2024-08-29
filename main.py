# Import from bards without specify parent directory in module,
# which will be important for AWS that starts in the src directory.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'bards'))

from bards.ArticleServer import run_http_server

# Running from terminal (Create and run web server)
if __name__ == "__main__":
    run_http_server("localhost", 3000) # Run Server using http.server module
