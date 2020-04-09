from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, DateTimeField, TextAreaField, SelectMultipleField, RadioField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, AnyOf, URL, Optional
from enums import State, Genre


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
        'phone', validators=[DataRequired()]
    )
    image_link = URLField(
        'image_link', validators=[DataRequired(), URL()]
    )
    genres = SelectMultipleField(
        # ✅ TODO implement enum restriction
        'genres', validators=[DataRequired(), AnyOf([(choice.value) for choice in Genre])],
        choices=Genre.choices()
    )
    facebook_link = URLField(
        'facebook_link', validators=[DataRequired(), URL()]
    )
    # ✅ TODO: Add missing fields
    website_link = URLField(
        'website_link',  validators=[Optional(), URL()]
    )
    # seeking_talent = BooleanField('Seeking talent',)
    seeking_talent = RadioField(u'Seeking talent', choices=[
        ('true', u'Yes'),
        ('false', u'No')],
        default='false', validators=[DataRequired()])
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
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        # ✅ TODO implement enum restriction
        'genres', validators=[DataRequired(), AnyOf([(choice.value) for choice in Genre])],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    # ✅ TODO: Add missing fields
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )
    seeking_venue = RadioField(u'Seeking venue', choices=[
        ('true', u'Yes'),
        ('false', u'No')],
        default='false', validators=[DataRequired()])
    seeking_description = TextAreaField('Seeking Description')

# ✅ TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM


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
