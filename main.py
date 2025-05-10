from util import api

class Main:
    def __init__(self):
        # Initialize the Flask app
        self.app = api.app
        self.app.run(debug=True, host='localhost', port=5000)
        # Setup directories
        api.setup_directories()

if __name__ == "__main__":
    Main()
    ...