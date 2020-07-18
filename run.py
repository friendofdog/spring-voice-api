from models.firebase.app import authenticate
from springapi.app import create_app

if __name__ == '__main__':
    authenticate()
    app = create_app()
    app.run()
