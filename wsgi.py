from util import api
from waitress import serve
from util.setup_dirs import setup_directories

app = api.app

# Ensure directories exist
setup_directories()

if __name__ == "__main__":
    print("Starting Remove BG Server on http://localhost:8000")
    serve(app, host="0.0.0.0", port=8000, threads=4)
