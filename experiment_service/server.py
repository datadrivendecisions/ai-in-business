"""Run the service. Cloud Run sets PORT; locally it defaults to 8080.

wsgiref's server is single-threaded and would be the wrong choice for
anything with load. This holds one classroom for one afternoon: thirty-two
submissions and a dashboard polling every five seconds. Gunicorn is in the
container for the deployed case; this entry point is what you run on a
laptop when you want to watch the routes work.
"""

import os
from wsgiref.simple_server import make_server

from app import build

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print("experiment service on http://localhost:%d" % port)
    make_server("", port, build()).serve_forever()
