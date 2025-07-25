from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///votes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()
    if Candidate.query.count() == 0:
        for name in ['Alice', 'Bob', 'Charlie']:
            db.session.add(Candidate(name=name))
        db.session.commit()

@app.route('/')
def index():
    candidates = Candidate.query.all()
    return render_template('index.html', candidates=candidates)

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()
    candidate_id = data.get('candidate_id')
    candidate = Candidate.query.get(candidate_id)
    if candidate:
        candidate.votes += 1
        db.session.commit()
        return jsonify({'message': 'Vote recorded'})
    return jsonify({'error': 'Candidate not found'}), 404

@app.route('/api/results')
def results():
    candidates = Candidate.query.all()
    data = [{'id': c.id, 'name': c.name, 'votes': c.votes} for c in candidates]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)