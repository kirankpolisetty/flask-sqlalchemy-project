from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from models import User, db


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict())

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        if not data or not data.get("name") or not data.get("email"):
            return jsonify({"error": "name and email are required"}), 400
        user = User(name=data["name"], email=data["email"])
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 409
        return jsonify(user.to_dict()), 201

    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        data = request.get_json()
        if data.get("name"):
            user.name = data["name"]
        if data.get("email"):
            user.email = data["email"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 409
        return jsonify(user.to_dict())

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
