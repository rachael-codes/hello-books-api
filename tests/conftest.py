# Purpose of this file = sets up all data you may need to use for your actual tests 

import pytest
from app import create_app
from app import db
from app.models.book import Book

# a fixture that generates a test db for us then cleans up
@pytest.fixture
def app(): 
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all() # will create a test db
        yield app # then run tests

    with app.app_context():
        db.drop_all() # then drop the test db (clean up)


# a fixture that takes in the app fixture and acts as a client making requests 
@pytest.fixture
def client(app): # app param comes from the app fixture above
    return app.test_client()


@pytest.fixture
def two_saved_books(app):
    # arrange
    ocean_book = Book(title="Ocean Book", description="Water 4eva")
    mountain_book = Book(title="Mountain Book", description="Mountains 4eva")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()