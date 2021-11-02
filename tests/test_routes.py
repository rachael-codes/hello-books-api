# get all books and return no records (makes sure app fixture works?)
def test_get_all_books_with_no_records(client): # We pass in the client fixture here, which we registered in conftest.py. 
    response = client.get('/books') # sends an HTTP request to /books 
    response_body = response.get_json() # makes sure response comes back as JSON

    assert response.status_code == 200
    assert response_body == [] 

# get one book by id
def test_get_book_by_id(client, two_saved_books): # passes in 2 fixtures
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id" : 1,
        "title" : "Ocean Book",
        "description" : "Water 4eva"
    }

def test_create_a_book(client):
    response = client.post('/books', json={
        "title" : "The Never Ending Story",
        "description" : "The horse dies"
    })
    response_body = response.get_json()

    assert response.status_code == 201 
