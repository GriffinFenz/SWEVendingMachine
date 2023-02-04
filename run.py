from app import create_app
from app.models.testdb import run_db
from app.extensions import db

if __name__ == "__main__":
    flask_app = create_app(db)
    run_db(flask_app)
    flask_app.run(debug=True)
