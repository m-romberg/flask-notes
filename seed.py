from models import User, Note, db, bcrypt
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

n1 = Note(
    title="Chores",
    content="Clean room, laundry",
    owner="User1"
)

n2 = Note(
    title="Homework",
    content="Math",
    owner="User2"
)

db.session.add(joel)
db.session.add(tom)
db.session.add_all([n1, n2])

db.session.commit()