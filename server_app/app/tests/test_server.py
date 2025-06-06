from presentation.schemas.message_schema import MessageCreate


def test_create_message(client):
    test_data = {
        "message": "test message",
        "date": "2023-01-01",
        "time": "12:00:00",
        "click_count": 1,
    }

    response = client.post("/messages/", json=test_data)
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == test_data["message"]
    assert "id" in data


def test_get_messages(client):
    response = client.get("/messages/")
    initial_count = len(response.json())

    test_data = MessageCreate(
        message="test message", date="2023-01-01", time="12:00:00", click_count=1
    )
    client.post("/messages/", json=test_data.model_dump())

    response = client.get("/messages/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == initial_count + 1
    assert data[-1]["message"] == test_data.message


def test_pagination(client):
    client.get("/messages/")

    for i in range(3):
        test_data = {
            "message": f"test message {i}",
            "date": "2023-01-01",
            "time": "12:00:00",
            "click_count": i,
        }
        client.post("/messages/", json=test_data)

    response = client.get("/messages/?offset=1&limit=1")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "test message 1"
