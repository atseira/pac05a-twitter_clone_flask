from app import create_app, db
from models.models import User

app = create_app()


def init_db():
    with app.app_context():
        db.create_all()
        admin = User(username='admin')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    init_db()
