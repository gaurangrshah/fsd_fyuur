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
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# db = SQLAlchemy(app)
db.init_app(app)
# ✅ TODO: connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Tasks.
# TODO: Add Try, Except Blocks for all endpoints that commit to db
# TODO: Check default value when "No" is checked for boolean seeking field
# TODO: update model nullability
# TODO: ✅ Add form validate token to each form {{ form.csrf_token }}
# TODO: check if upcoming and past shows get populated correctly
# TODO: Check how to cascade shows on venue delete
#----------------------------------------------------------------------------#


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
# ✅ TODO: replace with real venues data.
# ✅ TODO: num_shows should be aggregated based on number of upcoming shows per venue.
def venues():
    """
    Show: /Venues
    return => pages/venues
    """
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
    db.session.close()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
# ✅ TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
# seach for Hop should return "The Musical Hop".
# search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
def search_venues():
    """
    SEARCH: Venue
    return => /pages/search_venues
    """

    # grab search term from user input
    search_term = request.form.get('search_term', '')
    # query for venue search terms, allow for name, city & state
    venues = db.session.query(Venue).filter((Venue.name.ilike('%{}%'.format(search_term))) |
                                            (Venue.city.ilike('%{}%'.format(search_term))) |
                                            (Venue.state.ilike('%{}%'.format(search_term)))).all()
    if not venues:
        flash('Sorry, no results matching: {} found'.format(search_term))
        return redirect(url_for('venues'))

    response = {  # set default response values
        "count": 0,
        "data": []
    }

    for venue in venues:  # build return objects for venue search term
        venue_obj = {
            "id": venue.id,
            "name": venue.name,
            "upcoming_show_count": len(venue.shows)
        }
        response["data"].append(venue_obj)  # append venues to response.data
    response["count"] = len(response['data'])  # set count for matching venues
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>', methods=['GET', 'POST'])
# ✅ TODO: replace with real venue data from the venues table, using venue_id
def show_venue(venue_id):
    """
    Show: /Veneus/venue_id
    @params: venue_id
    return => pages/show_venue
    """

    # query returns first matching venue to matching venue_id
    venue = db.session.query(Venue).filter_by(id=venue_id).first()

    if not venue:  # if no venues match for the given id
        flash('Sorry venue id: {} is not in our records'.format(
            venue_id))  # output error message
        # redirect users to a list of venues
        return redirect(url_for('venues'))

    data = get_row(venue)  # returns dictionary from table properties

    data["genres"] = data["genres"].split(';') if data['genres'] else []
    data["past_shows"] = []
    data["upcoming_shows"] = []

    if len(venue.shows) > 0:
        # loop thru shows and update show info:
        for show in venue.shows:
            show_obj = {
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": str(show.start_time)
            }
            # check if show is upcoming or past:
            curr_datetime = datetime.now()  # get current time
            if show.start_time <= curr_datetime:
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
# ✅  TODO: insert form data as a new Venue record in the db, instead
# ✅  TODO: modify data to be the data object returned from db insertion
# ✅  TODO: on unsuccessful db insert, flash an error instead.
def create_venue_submission():
    """
    CREATE: Venue
    return => /venues
    """

    form = VenueForm()

    try:
        data = request.form  # grab values from form
        # build out new venue object from data properties
        venue = Venue(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            phone=data['phone'],
            image_link=data['image_link'],
            facebook_link=data['facebook_link'],
            website_link=data['website_link'],
            seeking_talent=isTruthy(data['seeking_talent']),
            seeking_description=data['seeking_description'],
            shows=[]
        )
        db.session.add(venue)  # pending changes
        db.session.commit()  # commit changes
        flash('Venue "{}" was successfully listed!'.format(
            request.form['name']))
        return redirect(url_for('venues'))

    except:
        db.session.rollback()
        flash('An error occurred. Venue "{}" could not be listed. Please try again.'.format(
            request.form['name']))
        return redirect(url_for('create_venue_submission', form=form))

    finally:
        db.session.close()


@app.route('/venues/<string:venue_id>/delete', methods=['GET'])
# ✅ TODO: Complete this endpoint for taking a venue_id, using SQLAlchemy ORM to delete a record.
# ✅ TODO: Handle cases where the session commit could fail. note(add rollback())
# ✅ TODO: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
# clicking that button delete it from the db then redirect the user to the homepage
def delete_venue(venue_id):
    """
    Delete =>  venue
    @params: venue_id
    return => /venues
    """

    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        if len(venue.shows) != 0:
            show = Show.query.filter(Show.venue_id == venue_id).first()
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()
        flash('Venue with id: {} was successfully deleted'.format(venue_id))
    except:
        flash('Venue with id: {} could not be deleted'.format(venue_id))
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
# ✅ TODO: replace with real data returned from querying the database
def artists():
    """
    Show: Artists
    return => /Artists
    """

    # artists = db.session.query(Artist).order_by(Artist.id).all()
    artists = Artist.query.order_by(Artist.id).all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
# ✅ TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
# seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
# search for "band" should return "The Wild Sax Band".
def search_artists():
    """
    SEARCH: Artist
    return => /pages/search_artists
    """

    # grab search term from user input
    search_term = request.form.get('search_term', '')
    # query for artist allow for search by name, city, state
    artists = db.session.query(Artist).filter((Artist.name.ilike('%{}%'.format(search_term))) |
                                              (Artist.city.ilike('%{}%'.format(search_term))) |
                                              (Artist.state.ilike('%{}%'.format(search_term)))).all()
    if not artists:
        flash('Sorry, no results matching: {} found'.format(search_term))
        return redirect(url_for('artists'))
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


@app.route('/artists/<int:artist_id>', methods=['GET', 'POST'])
# ✅ TODO: replace with real venue data from the venues table, using venue_id
def show_artist(artist_id):
    """
    Show: /Artist/:artist_id
    @params: artist_id
    result => pages/show_artist
    """

    # query artist by id, return first match
    artist = db.session.query(Artist).filter_by(id=artist_id).first()

    if not artist:  # handle error if no artists match id:
        flash('No matching Artists', 'error')
        return redirect('/artists')

    data = get_row(artist)  # get current values

    data["genres"] = data["genres"].split(';') if data['genres'] else []
    data["past_shows"] = []
    data["upcoming_shows"] = []

    if len(artist.shows) > 0:
        # loop through related shows and populate show info
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

    # count shows:
    data['past_shows_count'] = len(data['past_shows'])
    data['upcoming_shows_count'] = len(data['upcoming_shows'])
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
# ✅  TODO: populate form with fields from artist with ID <artist_id>
def edit_artist(artist_id):
    """
    Show: /artists/:artist_id/edit
    @params: artist_id
    return => /forms/edit_artist
    """

    form = ArtistForm()
    # query artist property values
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()

    if not artist:  # handle error if no artist matches
        flash('Artist not found')
        return redirect('/artists')

    data = get_row(artist)  # populate artist info from table
    data['genres'] = artist.genres.split(';')
    return render_template('forms/edit_artist.html', form=form, artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
# ✅ TODO: take values from the form submitted, and update existing
# artist record with ID <artist_id> using the new attributes
def edit_artist_submission(artist_id):
    """
    UPDATE: /artists/:artist_id/edit
    @params: artist_id
    return => /artist/:artist_id
    """

    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    try:
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
        flash('Artist "{}" successfully updated'.format(artist.name))

    except:
        db.session.rollback()
        flash('An error occured. Artist with id: "{}" was not updated'.format(artist_id))

    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
# ✅ TODO: populate form with values from venue with ID <venue_id>
# ✅ TODO: add documentation comment block
def edit_venue(venue_id):
    """
    Show: /venues/:venue_id/edit
    @params: venue_id
    return => /forms/edit_venue
    """
    form = VenueForm()
    # query venue properties by venue_id
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()

    if not venue:  # handle error if no venue matches
        flash('Venue not found')
        return redirect('/venues')

    data = get_row(venue)
    data['genres'] = venue.genres.split(';')
    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
# ✅ TODO: take values from the form submitted, and update existing
# venue record with ID <venue_id> using the new attributes
def edit_venue_submission(venue_id):
    """
    UPDATE: /venues/:venue_id/edit
    @params: venue_id
    return => /venues/:venue_id
    """

    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    try:
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
        flash('Venue "{}" successfully updated'.format(venue.name))

    except:
        db.session.rollback()
        flash('An error occured. Venue with id: "{}" was not updated'.format(venue_id))

    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
# ✅ TODO: insert form data as a new Venue record in the db, instead modify data to be the data object returned from db insertion
def create_artist_submission():
    """
    CREATE: Artist
    return => pages/home
    """
    form = ArtistForm()

    try:
        data = request.form  # grab values from form

        artist = Artist(
            name=data['name'],
            city=data['city'],
            state=data['state'],
            phone=data['phone'],
            genres=';'.join(data.getlist('genres')),
            image_link=data['image_link'],
            facebook_link=data['facebook_link'],
            website_link=data['website_link'],
            seeking_venue=isTruthy(data['seeking_venue']),
            seeking_description=data['seeking_description'],
            shows=[]
        )

        db.session.add(artist)
        db.session.commit()
        # ✅ TODO: on successful db insert, flash success
        flash('Artist "{}" was successfully listed!'.format(
            request.form['name']))
        return redirect(url_for('artists'))

    except:
        db.session.rollback()
        # ✅ TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash('An error occured. Artist "{}" could not be listed. Please try again'.format(
            request.form['name']))
        return redirect(url_for('create_artist_submission', form=form))

    finally:
        db.session.close()


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
# ✅  TODO: replace with real venues data.
#       num_shows should be aggregated based on number of upcoming shows per venue.
def shows():
    """
    Show: /shows
    return => /pages/shows
    """

    shows = Show.query.all()
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
# ✅ TODO: insert form data as a new Show record in the db
def create_show_submission():
    """
    Create: /shows/create
    return => /shows
    """

    form = ShowForm()

    try:
        data = request.form  # grab data from form input
        show = Show()  # instantiate new show object
        # query Artist by artist_id
        artist = db.session.query(Artist).filter_by(
            id=data['artist_id']).first()
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
        # ✅ on successful db insert, flash success
        flash('Show was successfully listed!')
        return redirect(url_for('shows'))
    except:
        db.session.rollback()
        # ✅ TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed. Please try again.')
        return redirect(url_for('create_shows'))
    finally:
        db.session.close()


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
