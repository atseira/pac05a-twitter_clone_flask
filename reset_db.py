from app import create_app, db
from init_db import init_db

app = create_app()

def reset_db():
    with app.app_context():
        db.drop_all()
        init_db()

if __name__ == '__main__':
    reset_db()
