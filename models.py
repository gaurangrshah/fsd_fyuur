from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), default='Other', nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    # ✅ TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(length=120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.Text, nullable=True)
    shows = db.relationship('Show', backref='venue')

    def __repr__(self):
        return '<id: {}, name: {}, city: {}, state: {}, address: {},genres: {}, phone: {}, image: {}, facebook: {}, website: {}, seeking_talent: {}, seeking_description: {}, shows: {}>'.format(self.id, self.name, self.city, self.state, self.address, self.genres, self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_talent, self.seeking_description, self.shows)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), default='Other', nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    # ✅ TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(length=120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    # 🚧 updates model
    seeking_description = db.Column(db.Text, nullable=True)
    shows = db.relationship('Show', backref='artist')

    def __repr__(self):
        return '<id: {}, name: {}, city: {}, state: {}, genres: {}, phone: {}, image: {}, facebook: {}, website_link: {}, seeking_venue: {}, seeking_description: {}>'.format(self.id, self.name, self.city, self.state, self.genres, self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_venue, self.seeking_description)

# ✅ TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    def __repr__(self):
        return '<id: {}, start_time: {}, artist_id: {}, venue_id: {}>'.format(self.id, self.start_time, self.artist_id, self.venue_id)
