from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    military_popularity = db.Column(db.Integer, default=50)
    business_popularity = db.Column(db.Integer, default=50)
    citizen_popularity = db.Column(db.Integer, default=50)
    turns_in_office = db.Column(db.Integer, default=0)
    game_over = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    impact = db.Column(db.Text)
    left_military_impact = db.Column(db.Integer)
    left_business_impact = db.Column(db.Integer)
    left_citizen_impact = db.Column(db.Integer)
    right_military_impact = db.Column(db.Integer)
    right_business_impact = db.Column(db.Integer)
    right_citizen_impact = db.Column(db.Integer)

# Sample scenarios
INITIAL_SCENARIOS = [
    {
        "content": "Executive Order: Addressing Military Budget Allocation\n\nBy the authority vested in me as President, I hereby propose a 15% increase in military spending...",
        "impact": "The Joint Chiefs are requesting additional funding for modernization efforts.",
        "left_military_impact": -15,
        "left_business_impact": 5,
        "left_citizen_impact": 10,
        "right_military_impact": 15,
        "right_business_impact": -10,
        "right_citizen_impact": -5
    },
    {
        "content": "Executive Order: Corporate Tax Reform\n\nIn light of economic challenges, I propose implementing new corporate tax policies...",
        "impact": "Major corporations are lobbying for tax reductions to stimulate growth.",
        "left_military_impact": 0,
        "left_business_impact": -20,
        "left_citizen_impact": 15,
        "right_military_impact": 5,
        "right_business_impact": 20,
        "right_citizen_impact": -15
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    game = GameState()
    db.session.add(game)
    db.session.commit()
    return jsonify({
        'game_id': game.id,
        'initial_state': {
            'military': 50,
            'business': 50,
            'citizen': 50,
            'turns': 0
        }
    })

@app.route('/get_scenario', methods=['GET'])
def get_scenario():
    scenarios = Scenario.query.all()
    if not scenarios:
        # If no scenarios in database, use sample scenarios
        scenario_data = random.choice(INITIAL_SCENARIOS)
        return jsonify(scenario_data)
    
    scenario = random.choice(scenarios)
    return jsonify({
        'content': scenario.content,
        'impact': scenario.impact
    })

@app.route('/process_swipe', methods=['POST'])
def process_swipe():
    data = request.json
    game_id = data['game_id']
    direction = data['direction']
    
    game = GameState.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Use sample scenario if no scenarios in database
    scenarios = Scenario.query.all()
    if not scenarios:
        scenario_data = random.choice(INITIAL_SCENARIOS)
    else:
        scenario = random.choice(scenarios)
        scenario_data = {
            'left_military_impact': scenario.left_military_impact,
            'left_business_impact': scenario.left_business_impact,
            'left_citizen_impact': scenario.left_citizen_impact,
            'right_military_impact': scenario.right_military_impact,
            'right_business_impact': scenario.right_business_impact,
            'right_citizen_impact': scenario.right_citizen_impact
        }
    
    if direction == 'right':
        game.military_popularity += scenario_data['right_military_impact']
        game.business_popularity += scenario_data['right_business_impact']
        game.citizen_popularity += scenario_data['right_citizen_impact']
    else:
        game.military_popularity += scenario_data['left_military_impact']
        game.business_popularity += scenario_data['left_business_impact']
        game.citizen_popularity += scenario_data['left_citizen_impact']

    game.turns_in_office += 1
    
    # Ensure popularities stay within bounds
    game.military_popularity = max(0, min(100, game.military_popularity))
    game.business_popularity = max(0, min(100, game.business_popularity))
    game.citizen_popularity = max(0, min(100, game.citizen_popularity))
    
    # Check for game over conditions
    if (game.military_popularity <= 0 or game.business_popularity <= 0 or 
        game.citizen_popularity <= 0 or game.military_popularity >= 100 or 
        game.business_popularity >= 100 or game.citizen_popularity >= 100):
        game.game_over = True

    db.session.commit()

    return jsonify({
        'new_state': {
            'military': game.military_popularity,
            'business': game.business_popularity,
            'citizen': game.citizen_popularity,
            'turns': game.turns_in_office,
            'game_over': game.game_over
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add initial scenarios if none exist
        if not Scenario.query.first():
            for scenario_data in INITIAL_SCENARIOS:
                scenario = Scenario(**scenario_data)
                db.session.add(scenario)
            db.session.commit()
    app.run(debug=True)