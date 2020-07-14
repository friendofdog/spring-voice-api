from app.routes import healthcheck

if __name__ == '__main__':
    healthcheck.app.run(debug=True)
