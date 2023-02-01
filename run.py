import app
from app import create_app
from app.models.testdb import run_db

if __name__ == "__main__":
    flask_app = create_app()
    run_db(flask_app)
    flask_app.run(debug=True)
