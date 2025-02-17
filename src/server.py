import json
from flask import Flask, render_template, request, redirect, flash, url_for

from datetime import datetime


MAX_BOOK = 12
PLACE_COST = 3


def load_clubs(json_file='clubs.json'):
    with open(json_file) as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions(json_file='competitions.json'):
    with open(json_file) as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show-summary', methods=['POST'])
def show_summary():
    try:
        club = [c for c in clubs if c['email'] == request.form['email']][0]
    except IndexError:
        flash('email was not found.')
        return redirect(url_for('index'))
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        place_cost=PLACE_COST,
        current_datetime=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
     )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_compet = [c for c in competitions if c['name'] == competition]
        found_compet = found_compet[0]
        return render_template(
            'booking.html',
            club=found_club,
            competition=found_compet,
            place_cost=PLACE_COST,
        )
    except IndexError:
        flash("Something went wrong-please try again")
        return redirect(url_for('show_summary'))


@app.route('/purchase-places', methods=['POST'])
def purchase_places():
    try:
        competition = [
            c for c in competitions if c['name'] == request.form['competition']
        ]
        competition = competition[0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        places_allowed = int(club['points'])
        current_datetime = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    except IndexError:
        flash("Something went wrong-please try again")
        return redirect(url_for('show_summary'))
    if places_required > places_allowed // PLACE_COST:
        flash('You do not have enough points')
    elif places_required > int(competition['places']):
        flash('Not enough places available')
    elif current_datetime > competition['date']:
        flash('Competition over')
    elif places_required > MAX_BOOK:
        flash(
            f"You cannot purchase more than {MAX_BOOK} "
            f"{'place' if MAX_BOOK <= 1 else 'places'}"
        )
    else:
        club['points'] = places_allowed - places_required * PLACE_COST
        competition['places'] = int(competition['places']) - places_required
        flash('Great-booking complete!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            place_cost=PLACE_COST,
            current_datetime=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    return render_template(
        'booking.html',
        club=club,
        competition=competition,
        place_cost=PLACE_COST,
    )


@app.route('/points-board')
def points_board():
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
