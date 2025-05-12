from util import api
from util.setup_dirs import setup_directories

app = api.app

# Ensure directories exist
setup_directories()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
