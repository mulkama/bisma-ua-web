from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.email


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)

    # Relationship to access the user who favorited the item
    user = db.relationship("User", backref=db.backref("favorites", lazy=True))

    def __repr__(self):
        return f"<Favorites {self.item_name} for User {self.user_id}>"
