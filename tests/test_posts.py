from app.schemas.post_schema import PostResponse


def test_get_posts_authorized(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json()) 
    
    if response.status_code != 200:
        print("Error: Unauthorized. Check the token setup.")
        assert False, "Token might be invalid or authorization logic might have an issue."
    # Validate the response against the PostResponse schema
    try:
        validated_posts = [PostResponse(**post) for post in response.json()]
    except Exception as e:
        print("Schema Validation Failed:", e)
        print("Response Content:", response.text)
        raise e

    assert response.status_code == 200
    assert len(validated_posts) == len(test_posts)
    for post, test_post in zip(validated_posts, test_posts):
        assert post.title == test_post.title
        assert post.content == test_post.content
        assert post.id == test_post.id


def test_get_posts_unauthorized(client):
    response = client.get("/posts/")
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    # Assert the response is 401 Unauthorized
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_post_authorized(authorized_client, test_user):
    post_data = {
        "title": "New Post",
        "content": "New Content",
        "user_id": test_user['id']
    }
    res = authorized_client.post("/posts/", json=post_data)
    assert res.status_code == 201
    
    response_json = res.json()
    print("Response JSON:", response_json)  # Debugging output
    
    # Validate response keys
    assert 'id' in response_json
    assert response_json['title'] == post_data['title']
    assert response_json['content'] == post_data['content']
    assert response_json['user_id'] == post_data['user_id']

    


def test_create_post_unauthorized(client,test_user):
    post_data = {
        "title": "New Post",
        "content": "New Content",
        "user_id": test_user['id']
    }
    res = client.post("/posts/", json=post_data)
    assert res.status_code == 401
    
    