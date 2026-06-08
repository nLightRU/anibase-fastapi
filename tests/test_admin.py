from fastapi import status

anime_payload = {
    'title': 'Test Anime',
    'episodes': 12,
    'rating': 8.4,
    'description': 'Test Description',
    'is_hidden': False
}

def test_create_anime(client):
    response = client.post('/admin/anime/', json=anime_payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == anime_payload['title']
    assert data['episodes'] == anime_payload['episodes']
    assert data['rating'] == anime_payload['rating']
    assert data['description'] == anime_payload['description']
    assert data['is_hidden'] == anime_payload['is_hidden']
    assert 'id' in data


def test_list_anime(client):
    client.post('/admin/anime/', json=anime_payload)
    response = client.get('/admin/anime/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_anime(client):
    create_resp = client.post('/admin/anime/', json=anime_payload)
    anime_id = create_resp.json()['id']
    update_payload = {'title':'Updated Title'}
    response = client.put(f'/admin/anime/{anime_id}', json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == update_payload['title']

    # Проверяем, что остальные поля не изменились
    assert data['description'] == anime_payload['description']
    assert data['episodes'] == anime_payload['episodes']


def test_delete_anime(client):
    create_resp = client.post("/admin/anime/", json=anime_payload)
    anime_id = create_resp.json()["id"]
    response = client.delete(f"/admin/anime/{anime_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что аниме больше нет
    get_resp = client.get(f"/admin/anime/{anime_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
