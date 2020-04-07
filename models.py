from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # ✅ TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(length=120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)

# print(Venue)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # ✅ TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(length=120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)


# TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# print(Artist)
