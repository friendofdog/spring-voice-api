from springapi.app import create_app
from models.firebase.app import authenticate


if __name__ == '__main__':
    authenticate()
    app = create_app()
    app.run()
