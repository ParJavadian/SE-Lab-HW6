from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/main_db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    item = Item(name=data['name'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name}), 201

if __name__ == '__main__':
    try:
        resolved_host = socket.gethostbyname("db")
        print(f"Resolved 'db' to {resolved_host}")
    except Exception as e:
        print(f"Failed to resolve 'db': {e}")
    with app.app_context():
        db.create_all()  # Automatically create tables
    app.run(host='0.0.0.0', port=8080)

