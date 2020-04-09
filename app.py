#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from forms import *
# from models import Artist, Venue
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# ✅ TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Tasks.
# TODO: Fix false value on seeking_talent, seeking_venue issue. update forms.py and all endpoints
# TODO: Add error messages for form fields
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: FIX SHOW MODEL RELATIONSHIP

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # ✅ TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(length=120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    shows = db.relationship('Show', backref='venue')

    def __repr__(self):
        return '<id: {}, name: {}, city: {}, state: {}, address: {},genres: {}, phone: {}, image: {}, facebook: {}, website: {}, seeking_talent: {}, seeking_description: {}, shows: {}>'.format(self.id, self.name, self.city, self.state, self.address, self.genres, self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_talent, self.seeking_description, self.shows)
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
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)  # 🚧 updates model
    shows = db.relationship('Show', backref='artist')

    def __repr__(self):
        return '<id: {}, name: {}, city: {}, state: {}, genres: {}, phone: {}, image: {}, facebook: {}, website_link: {}, seeking_venue: {}, seeking_description: {}>'.format(self.id, self.name, self.city, self.state, self.genres, self.phone, self.image_link, self.facebook_link, self.website_link, self.seeking_venue, self.seeking_description)
# print(Artist)

# ✅ TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    def __repr__(self):
        return '<id: {}, start_time: {}, artist_id: {}, venue_id: {}>'.format(self.id, self.start_time, self.artist_id, self.venue_id)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


def get_row(row):
    # builds dictionary object from table properties
    return {col.name: getattr(row, col.name) for col in row.__table__.columns}


def isTruthy(condition):
    # checks if given conditions is truthy
    return True if condition else False


def isNone(condition):
    # check is condition exists otherwise deafults to None
    return condition if condition else None


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    """
    Show: /Venues
    return => pages/venues
    """
    # ✅ TODO: replace with real venues data.
    # TODO: add try except finally blocks
    # TODO: add documentation comment block
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    locations = db.session.query(Venue.city, Venue.state).group_by(  # build venue groups
        Venue.city, Venue.state).all()
    data = []
    for locale in locations:  # loop thru venue groups
        city = locale[0]
        state = locale[1]
        venue_query = db.session.query(Venue).filter(  # build venue query
            Venue.city == city, Venue.state == state)
        location = {
            "city": city,
            "state": state,
            "venues": []
        }
        venues = venue_query.all()  # execute venue query

        for venue in venues:  # display venues
            print(venue.id)
            location['venues'].append({
                "id": venue.id,
                "name": venue.name,
                "upcoming_show_count": len(venue.shows)
            })
        data.append(location)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    SEARCH: Venue
    return => /pages/search_venues
    """
    # ✅ TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # TODO: Add try, except, finally block
    # ✅TODO: Add documentation comment block
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    # grab search term from user input
    search_term = request.form.get('search_term', '')
    # query for venue search terms, allow for name, city & state
    venues = db.session.query(Venue).filter((Venue.name.ilike('%{}%'.format(search_term))) |
                                            (Venue.city.ilike('%{}%'.format(search_term))) |
                                            (Venue.state.ilike('%{}%'.format(search_term)))).all()
    response = {  # set default response values
        "count": 0,
        "data": []
    }
    for venue in venues:  # build return objects for venue search term
        v_obj = {
            "id": venue.id,
            "name": venue.name,
            "upcoming_show_count": len(venue.shows)
        }
        response["data"].append(v_obj)  # append venues to response.data
    response["count"] = len(response['data'])  # set count for matching venues
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    """
    Show: /Veneus/venue_id
    @params: venue_id
    return => pages/show_venue
    """
    # ✅ TODO: replace with real venue data from the venues table, using venue_id
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block

    venue = db.session.query(Venue).filter_by(id=venue_id).first()
    # query returns first matching venue to matching venue_id
    if not venue:  # if no venues match for the given id
        flash('Sorry this venue is not in our records')  # output error message
        redirect('/venues')  # redirect users to a list of venues
    data = get_row(venue)  # returns dictionary from table properties

    data["genres"] = data["genres"].split(';') if data['genres'] else []
    data["past_shows"] = []
    data["upcoming_shows"] = []
    now_datetime = datetime.now()
    # loop thru shows and show info to venue data:
    for show in venue.shows:
        show_obj = {
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        }
        # # check if show is upcoming or a past show:
        if show.start_time <= now_datetime:
            data['past_shows'].append(show_obj)  # add show to past shows
        else:
            # add show to upcoming shows
            data['upcoming_shows'].append(show_obj)

    # get past shows count
    data['past_shows_count'] = len(data['past_shows'])
    # get upcoming shows count
    data['upcoming_shows_count'] = len(data['upcoming_shows'])
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    CREATE: Venue
    return => /pages/home
    """
    # ✅  TODO: insert form data as a new Venue record in the db, instead
    # ✅  TODO: modify data to be the data object returned from db insertion
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block
    form = VenueForm()
    if not form.validate_on_submit():  # if validation fails?? 🚧
        data = request.form  # grab values from form as data
        # build out new venue object from data properties
        venue = Venue(name=data['name'], address=data['address'], city=data['city'], state=data['state'], phone=data['phone'],
                      image_link=data['image_link'], facebook_link=data['facebook_link'], website_link=data['website_link'])
        # evaluate seeking talent property:
        venue.seeking_talent = isTruthy(data['seeking_talent'])
        venue.seeking_description = data['seeking_description']
        venue.shows = []
        db.session.add(venue)  # pending changes
        db.session.commit()  # commit changes
        # ✅ TODO: on unsuccessful db insert, flash an error instead.
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue ' +
              data.name + ' could not be listed. Please try again.')
        return render_template('forms/new_venue.html', form=form)
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<string:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    """
    Delete =>  venue
    @params: venue_id
    return => /venues
    """
    # print('deleting..', venue_id)
    # ✅  TODO: Complete this endpoint for taking a venue_id, using SQLAlchemy ORM to delete a record.
    # TODO: Handle cases where the session commit could fail. note(add rollback())
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()

    if not venue:
        flash('Venue not found. Please Try again.' + str(venue_id))
        return redirect('/venues')
    # TODO: check if venue has shows if so raise error:
    if len(venue.shows) != 0:
        show = Show.query.filter(Show.venue_id == venue_id).first()
        db.session.delete(show)
        flash('Venue deleted successfully, with Shows.')
        # ❌ return redirect('/venues/' + str(venue_id))
    db.session.delete(venue)
    db.session.commit()
    # ✅ TODO: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect('/venues')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    """
    Show: Artists
    return => /Artists
    """
    # ✅ TODO: replace with real data returned from querying the database
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block

    artists = db.session.query(Artist).order_by(Artist.id).all()
    print(artists)
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    SEARCH: Artist
    return => /pages/search_artists
    """
    # ✅ TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    # grab search term from user input
    search_term = request.form.get('search_term', '')
    # query for artist allow for search by name, city, state
    artists = db.session.query(Artist).filter((Artist.name.ilike('%{}%'.format(search_term))) | (
        Artist.city.ilike('%{}%'.format(search_term))) | (Artist.state.ilike('%{}%'.format(search_term)))).all()
    response = {  # set defaults
        'count': 0,
        'data': []
    }
    for artist in artists:  # loop thru artists and build artist result
        artist_obj = {
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len(artist.shows)
        }
    response['data'].append(artist_obj)  # append artist
    response['count'] = len(response['data'])  # get count of total artists

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Show: /Artist/artist_id
    @params: artist_id = id of artist to show
    result => pages/show_artist.html
    """
    # shows the venue page with the given venue_id
    # ✅ TODO: replace with real venue data from the venues table, using venue_id
    # TODO: add try, except, finally block
    # ✅  TODO: add documentation comment block

    # query artist by id, return first match
    artist = db.session.query(Artist).filter_by(id=artist_id).first()

    if not artist:  # handle error if no artists match id:
        flash('No matching Artists', 'error')
        return redirect('/artists')
    data = {  # set defaults
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(';'),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "image_link": artist.image_link,
        "facebook_link": artist.facebook_link,
        "website_link": artist.website_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0
    }
    # loop through shows associated to artist and return show info
    for show in artist.shows:
        show_obj = {
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": str(show.start_time)
        }
        curr_time = datetime.now()
        if show.start_time <= curr_time:  # sort past and upcoming shows
            data['past_shows'].append(show_obj)
        else:
            data['upcoming_shows'].append(show_obj)

    data['past_shows_count'] = len(data['past_shows'])
    data['upcoming_shows_count'] = len(data['upcoming_shows'])
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Show: /artists/:artist_id/edit
    @params: artist_id
    return => /forms/edit_artist
    """
    # ✅  TODO: populate form with fields from artist with ID <artist_id>
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block
    form = ArtistForm()
    # query artist property values
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:  # handle error if no artist matches
        flash('Artist not found')
        return redirect('/artists')
    data = {  # buid for field values
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "image_link": artist.image_link,
        "genres": artist.genres.split(';'),
        "facebook_link": artist.facebook_link,
        "website_link": artist.website_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
    }
    return render_template('forms/edit_artist.html', form=form, artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    UPDATE: /artists/:artist_id/edit
    @params: artist_id
    return => /artist/:artist_id
    """
    # ✅ TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block

    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    data = request.form
    artist.name = data['name']
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.image_link = data['image_link']
    artist.genres = ';'.join(data.getlist('genres'))
    artist.facebook_link = data['facebook_link']
    artist.website_link = data['website_link']
    artist.seeking_venue = isTruthy(data['seeking_venue'])
    artist.seeking_description = data['seeking_description']
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Show: /venues/:venue_id/edit
    @params: venue_id
    return => /forms/edit_venue
    """
    # ✅  TODO: populate form with values from venue with ID <venue_id>
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block
    form = VenueForm()
    # query venue properties by venue_id
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    print("🚨", venue)
    if not venue:  # handle error if no venue matches
        flash('Venue not found')
        return redirect('/venues')
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "genres": venue.genres.split(';'),
        "image_link": venue.image_link,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
    }
    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    UPDATE: /venues/:venue_id/edit
    @params: venue_id
    return => /venues/:venue_id
    """
    # ✅  TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    # TODO: add try, except, finally block
    # ✅ TODO: add documentation comment block

    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    data = request.form
    venue.name = data['name']
    venue.city = data['city']
    venue.state = data['state']
    venue.phone = data['phone']
    venue.image_link = data['image_link']
    venue.genres = ';'.join(data.getlist('genres'))
    venue.facebook_link = data['facebook_link']
    venue.website_link = data['website_link']
    venue.seeking_talent = isTruthy(data['seeking_talent'])
    venue.seeking_description = data['seeking_description']
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Create: Artist
    return => pages/home
    """
    # called upon submitting the new artist listing form
    # ✅ TODO: insert form data as a new Venue record in the db, instead modify data to be the data object returned from db insertion
    # TODO: add try, except, finally block
    # ✅  TODO: add documentation comment block
    data = request.form
    artist = Artist()
    artist.name = data['name']
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.genres = ';'.join(data.getlist('genres'))
    artist.image_link = data['image_link']
    artist.facebook_link = data['facebook_link']
    artist.website_link = data['website_link']
    artist.seeking_venue = isTruthy(data['seeking_venue'])
    artist.seeking_description = data['seeking_description']
    db.session.add(artist)
    db.session.commit()
    print(artist)
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
    """
    Show: /shows
    return => /pages/shows
    """
    # displays list of shows at /shows
    # ✅  TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # TODO: add try, except, finally block
    # TODO: add documentation comment block
    shows = db.session.query(Show).all()
    data = []
    for show in shows:
        artist = show.artist
        venue = show .venue
        data.append({
            "venue_id": isNone(venue.id),
            "venue_name": isNone(venue.name),
            "artist_id": isNone(artist.id),
            "artist_name": isNone(artist.name),
            "artist_image_link": isNone(artist.image_link),
            "start_time": str(show.start_time),
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Create: /shows/create
    return => success: /pages/home | error: /shows/create
    """
    # called to create new shows in the db, upon submitting new show listing form
    # ✅ TODO: insert form data as a new Show record in the db, instead
    # TODO: UPDATE try, except, finally block
    # ✅ TODO: add documentation comment block

    data = request.form  # grab data from form input
    show = Show()  # instantiate new show object
    # query Artist by artist_id
    artist = db.session.query(Artist).filter_by(id=data['artist_id']).first()
    if not artist:  # if artist doesn't exist:
        flash('Cannot find the artist requested. Please Try again.')
        return redirect('/shows/create')
    venue = db.session.query(Venue).filter_by(id=data['venue_id']).first()
    if not venue:  # if venue doesn't exist
        flash('Cannot find the venue requested. Please Try again.')
        return redirect('/shows/create')
    try:
        show.start_time = dateutil.parser.parse(
            data['start_time'])  # get start_time
    except:
        flash('Please provide a valid date.')
        return redirect('/shows/create')
    show.artist_id = artist.id
    show.venue_id = venue.id
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
