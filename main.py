from util import api
from util.setup_dirs import setup_directories

app = api.app

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)