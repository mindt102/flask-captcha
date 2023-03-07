from project import db, models, create_app

app = create_app()

with app.app_context():
    db.create_all()