from datetime import datetime
from models.record import Record


def test_create_record(client):
    response = client.post(
        "/records",
        json={
            "text": "Test text",
            "date": "2025-06-08T19:00:00",
            "time": "19:00:00",
            "click_number": 1,
        },
    )
    assert response.status_code == 201
    assert response.json()["text"] == "Test text"


def test_get_records(client, db):
    db.add(
        Record(text="Test text", date=datetime.now(), time="19:00:00", click_number=1)
    )
    db.commit()

    response = client.get("/records?offset=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["text"] == "Test text"


def test_pagination(client, db):
    for i in range(15):
        db.add(
            Record(
                text=f"Text {i}", date=datetime.now(), time="19:00:00", click_number=i
            )
        )
    db.commit()

    response = client.get("/records?offset=10&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 5
