from util import api
from util.setup_dirs import setup_directories

app = api.app

if __name__ == "__main__":
    app.run(debug=0, host='localhost', port=8000)