from . import db



class Book(db.Model):

    title = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    published = db.Column(db.String(20))
    isbn = db.Column(db.String(50), primary_key = True, unique = True)
    pages = db.Column(db.Integer)
    thumbnail = db.Column(db.String(300))
    language = db.Column(db.String(2))