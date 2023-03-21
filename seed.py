from models import User, db, bcrypt
from app import app

db.drop_all()
db.create_all()

joel = User.register(
    username='User1',
    password='password',
    email='email@email.com',
    first_name='Joel',
    last_name='Burton'
)

tom = User.register(
    username='User2',
    password='password',
    email='email2@email.com',
    first_name='Tom',
    last_name='Frommyspace'
)

db.session.add(joel)
db.session.add(tom)

db.session.commit()