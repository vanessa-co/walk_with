# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app import app
# from models import db

from datetime import datetime
from app import app
from models import db, User, Walk, Review, Follow


def seed_data():
    # Create some users
    vanessa = User(username='vanessa', email='vanessa@email.com', password='password1')
    kim = User(username='kim', email='kim@email.com', password='password2')
    kevin = User(username='kevin', email='kevin@email.com', password='password3')

    db.session.add_all([vanessa, kim, kevin])
    db.session.commit()

    #  walks for vanessa
    vanessa_walk1 = Walk(location='Central Park', distance=2.5, photo='https://i.natgeofe.com/n/15ec8dec-df7c-45af-a0ae-08d4e906a134/belvedere-castle.jpg?w=2880&h=2160', user=vanessa, created_at=datetime(2022, 1, 1))
    vanessa_walk2 = Walk(location='Hudson River Park', distance=3.2, photo='https://www.frommers.com/system/media_items/attachments/000/868/444/s980/Frommers-New-York-City-jogging-hudson-park-1190x768.jpg?1646914426', user=vanessa, created_at=datetime(2022, 2, 1))

    db.session.add_all([vanessa_walk1, vanessa_walk2])
    db.session.commit()

    # reviews for Vanessa's walks
    vanessa_review1 = Review(text='Great walk!', user=vanessa, walk=vanessa_walk1, created_at=datetime(2022, 1, 5))
    vanessa_review2 = Review(text='Beautiful views!', user=vanessa, walk=vanessa_walk2, created_at=datetime(2022, 2, 5))

    db.session.add_all([vanessa_review1, vanessa_review2])
    db.session.commit()

    # Have kim follow vanessa
    kim_follow_vanessa = Follow(follower=kim, followed=vanessa, created_at=datetime(2022, 3, 1))
    db.session.add(kim_follow_vanessa)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()



