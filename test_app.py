from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

class FlaskTests(TestCase):

    def setUp(self):
        self.boggle_game = Boggle()
        self.board = [['L','A','T','E', 'R'],
                      ['F','Z','N','O','K'],
                      ['L','R','T','E', 'P'],
                      ['L','A','T','E','R'],
                      ['L','A','T','E','V']]

    def tearDown(self):
        self.boogle_game = ""
        self.board = []

    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = self.board
            res = client.get("/check-word?word-input=late")
            self.assertEqual(res.json["message"], "ok")
    def test_invalid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = self.board
            res = client.get("/check-word?word-input=lt")
            self.assertEqual(res.json["message"], "not-word")

    def test_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = self.board
            res = client.get("/check-word?word-input=doughnut")
            self.assertEqual(res.json["message"], "not-on-board")

    def test_high_score(self):
        with app.test_client() as client:
          
            
            res = client.post("/save-score", data = json.dumps(dict(score = 10)), content_type = "application/json")
            print(res.get_json())
            self.assertEqual(int(res.json["highscore"]), 10)
