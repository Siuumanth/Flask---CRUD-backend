from app import app
from app import db,Drink

with app.app_context():
    db.create_all()
