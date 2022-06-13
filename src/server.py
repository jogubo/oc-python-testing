import json
from flask import Flask, render_template, request, redirect, flash, url_for


MAX_BOOK = 12
PLACE_COST = 1


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show-summary', methods=['POST'])
def show_summary():
    try:
        club = [c for c in clubs if c['email'] == request.form['email']][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
         )
    except IndexError:
        flash('email was not found.')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase-places', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    place_allowed = int(club['points']) // PLACE_COST
    if places_required > place_allowed:
        flash('You do not have enough points')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > MAX_BOOK:
        flash(
            f"You cannot purchase more than {MAX_BOOK} "
            f"{'place' if MAX_BOOK <= 1 else 'places'}"
        )
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    else:
        club['points'] = place_allowed - places_required * PLACE_COST
        competition['places'] = int(competition['places']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
