from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, DateTimeField, TextAreaField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional, Required
# from enums import state_choices, genre_choices
from enums import State, Genre  # see alternate implementation


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        # ✅ TODO implement enum restriction
        'state', validators=[DataRequired(), AnyOf([(choice.value) for choice in State])],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[Regexp(r'^[0-9\-\+]+$')]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        # ✅ TODO implement enum restriction
        'genres', validators=[DataRequired(), AnyOf([(choice.value) for choice in Genre])],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL()]
    )
    # 🚧  TODO: Add missing fields TODO: update validators
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )
    # seeking_talent = BooleanField('Seeking talent',)
    seeking_talent = RadioField(u'Seeking talent', choices=[
        ('true', u'Yes'),
        ('false', u'No')],
        default='false', validators=[Required()])
    seeking_description = TextAreaField('Seeking Description')


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        # ✅ TODO implement enum restriction
        'state', validators=[DataRequired(), AnyOf([(choice.value) for choice in State])],
        choices=State.choices()
    )
    phone = StringField(
        # ✅ TODO implement validation logic for state
        # https://knowledge.udacity.com/questions/105337
        # 🚧 fixes phone validator
        'phone', validators=[Regexp(r'^[0-9\-\+]+$')]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        # ✅ TODO implement enum restriction
        'genres', validators=[DataRequired(), AnyOf([(choice.value) for choice in Genre])],
        choices=Genre.choices()
    )
    ''''
    https://knowledge.udacity.com/questions/77530
    'genres', validators=[DataRequired(), AnyOf( [ (choice.value) for choice in Genre ] )],
    choices=Genre.choices()
    '''
    facebook_link = StringField(
        '''
        🤔 TODO implement enum restriction
        adds optional validator, to stop validation chain
        check if implementation is correct and does not trigger any errors
        if no errors, apply to all optional fields
        '''
        # 'facebook_link', validators=[Optional(), URL()]
        'facebook_link', validators=[URL()]
    )
    # TODO: Add missing fields
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )
    # seeking_venue = BooleanField('Seeking Venue',)
    seeking_venue = RadioField(u'Seeking venue', choices=[
        ('true', u'Yes'),
        ('false', u'No')],
        default='false', validators=[Required()])
    seeking_description = StringField('seeking_description',)

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )
    # TODO: Add missing fields
