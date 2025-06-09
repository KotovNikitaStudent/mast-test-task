from unittest.mock import patch
from core.settings import get_settings

settings = get_settings()


def test_initial_ui(app):
    assert app.text_input.text() == ""
    assert app.list_view.model().rowCount() == 0
    assert app.post_button.text() == "Send POST"
    assert app.get_button.text() == "Get Records"
    assert app.page_input.value() == 0
    assert app.page_label.text() == "Offset: 0"


@patch("requests.post")
def test_send_post_request(mock_post, app):
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status = lambda: None
    app.text_input.setText("Test input")
    app.send_post_request()
    assert mock_post.called
    assert app.click_count == 1
    assert "POST successful" in app.list_view.model().stringList()[0]


@patch("requests.get")
def test_get_records(mock_get, app):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.json.return_value = [
        {"id": 1, "text": "Test", "date": "2025-06-08T19:00:00", "click_number": 1}
    ]

    app.get_records()
    assert mock_get.called
    called_args = mock_get.call_args[1]["params"]
    assert called_args["offset"] == 0
    assert called_args["limit"] == settings.PAGINATION_LIMIT

    assert app.list_view.model().stringList()[0].startswith("ID: 1")


@patch("requests.get")
def test_pagination(mock_get, app):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status = lambda: None

    mock_get.return_value.json.return_value = [
        {"id": 1, "text": "Test 1", "date": "2025-06-08T19:00:00", "click_number": 1}
    ]
    app.get_records()
    assert app.list_view.model().stringList()[0].startswith("ID: 1")
    assert app.page_label.text() == "Offset: 0"

    mock_get.return_value.json.return_value = [
        {"id": 11, "text": "Test 11", "date": "2025-06-08T19:00:00", "click_number": 11}
    ]
    app.next_page()
    assert app.offset == settings.PAGINATION_LIMIT
    assert app.page_input.value() == settings.PAGINATION_LIMIT
    assert app.page_label.text() == f"Offset: {settings.PAGINATION_LIMIT}"
    assert app.list_view.model().stringList()[0].startswith("ID: 11")

    mock_get.return_value.json.return_value = [
        {"id": 1, "text": "Test 1", "date": "2025-06-08T19:00:00", "click_number": 1}
    ]
    app.prev_page()
    assert app.offset == 0
    assert app.page_input.value() == 0
    assert app.page_label.text() == "Offset: 0"
    assert app.list_view.model().stringList()[0].startswith("ID: 1")

    arbitrary_offset = settings.PAGINATION_LIMIT * 2
    mock_get.return_value.json.return_value = [
        {"id": 21, "text": "Test 21", "date": "2025-06-08T19:00:00", "click_number": 21}
    ]
    app.page_input.setValue(arbitrary_offset)
    assert app.offset == arbitrary_offset
    assert app.page_label.text() == f"Offset: {arbitrary_offset}"
    assert app.list_view.model().stringList()[0].startswith("ID: 21")
