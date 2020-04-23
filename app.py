from flask import Flask, request, session, redirect, render_template, flash, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "easyas123"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


HIGH_SCORE = "highscore"
BOARD = "board"

boggle_game = Boggle()


@app.route("/")
def home():
    session[BOARD] = boggle_game.make_board()
    return render_template("home.html", board = session[BOARD])


@app.route("/check-word")
def check_word():
    word = request.args.get("word-input", "")
    
    board = session[BOARD]

    msg = boggle_game.check_valid_word(board, word)
    
    return jsonify({"message": msg})
     
@app.route("/save-score", methods=["POST"])
def save_score():
    score = request.json.get("score", 0)
    print(f"i am score {score}")
    if session.get(HIGH_SCORE):
        if score > session.get(HIGH_SCORE):
            session[HIGH_SCORE] = score
    else:
        session[HIGH_SCORE] = score
        print(f"i am {session[HIGH_SCORE]}")
    return jsonify({"highscore":session[HIGH_SCORE]})

@app.route("/plays")    
def plays():
    """update the amount of times a user has played"""    
    if session.get("n_plays"):
        session["n_plays"] += 1

    else:
        session["n_plays"] = 1
    
    return jsonify({"plays":session["n_plays"]})