from unittest.mock import MagicMock
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest


def test_send_message_updates_model(main_window, qtbot):
    main_window.line_edit.setText("Hello World")
    QTest.mouseClick(main_window.send_button, Qt.MouseButton.LeftButton)
    assert main_window.line_edit.text() == ""


def test_send_message_calls_api(main_window):
    main_window.line_edit.setText("Test message")
    main_window.send_message()
    main_window.message_api.create_message.assert_called()


def test_refresh_messages_calls_api(main_window):
    main_window.refresh_messages()
    main_window.message_api.get_messages.assert_called_with(
        offset=main_window.current_offset
    )


def test_load_all_messages(populate_messages, main_window):
    populate_messages(10)
    main_window.load_all_messages()
    assert len(main_window.message_model.messages) == 10


def test_pagination_navigation(main_window, qtbot, mock_server_api):
    main_window.message_api.default_limit = 100

    def get_messages_side_effect(offset=0, limit=None, all_pages=False):
        limit = limit or main_window.message_api.default_limit
        return [
            MagicMock(
                message=f"msg {i}", date="2023-01-01", time="12:00:00", click_count=i
            )
            for i in range(offset, offset + limit)
        ]

    main_window.message_api.get_messages.side_effect = get_messages_side_effect

    main_window.refresh_messages()
    assert main_window.page_label.text() == "Page: 1"

    QTest.mouseClick(main_window.next_button, Qt.MouseButton.LeftButton)
    assert main_window.current_offset == 100
    assert main_window.page_label.text() == "Page: 2"

    QTest.mouseClick(main_window.prev_button, Qt.MouseButton.LeftButton)
    assert main_window.current_offset == 0
    assert main_window.page_label.text() == "Page: 1"


def test_progress_bar_visibility(main_window, qtbot):
    assert not main_window.progress_bar.isVisible()

    main_window.show_progress(True)
    assert main_window.progress_bar.isVisible()

    main_window.show_progress(False)
    assert not main_window.progress_bar.isVisible()
