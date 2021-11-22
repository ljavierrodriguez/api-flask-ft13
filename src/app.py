from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from models import db, User

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "dialet+driver://user:pass@host:port/dbname"
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/test"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/test"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade 


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/api/users', methods=['GET', 'POST', 'DELETE'])
def get_post_users():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))
        return jsonify(users), 200

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        phone = request.json.get('phone')
        email = request.json.get('email')

        user = User()
        user.username = username
        user.password = password
        user.phone = phone
        user.email = email 
        user.save()

        return jsonify({
            "success": "User was created!",
            "user": user.serialize()
        }), 201

    if request.method == 'DELETE':
        users = User.query.all()

        for user in users:
            user.delete()     

        return jsonify({
            "success": "Users were deleted!"
        }), 200

@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_users(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return jsonify(user.serialize()), 200

    if request.method == 'PUT':
        username = request.json.get('username')
        password = request.json.get('password')
        phone = request.json.get('phone')
        email = request.json.get('email')

        user = User.query.get(id)
        user.username = username
        user.password = password
        user.phone = phone
        user.email = email 
        user.update()

        return jsonify({
            "success": "User was updated!",
            "user": user.serialize()
        }), 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        user.delete()
        return jsonify({
            "success": "User was deleted!",
        }), 200




if __name__ == '__main__':
    app.run()