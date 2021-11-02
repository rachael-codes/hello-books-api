from app import db
# db is line 7 from our main __init__ file in the app folder 
# it's an instance of SQLAlchemy 

# our Book class will inherit from db 
class Book(db.Model):
    # we define three columns for the Book table 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # __tablename__ = "books" # this would make the Book model link to a table named books
    # w/o line 11, the table will default to being named Book 

