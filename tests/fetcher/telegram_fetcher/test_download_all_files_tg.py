import pytest
from src.fetcher.telegram_fetcher import TelegramFetcher

@pytest.fixture
def fetcher():
    return TelegramFetcher("fake_id", "fake_hash", "chat123")

def test_download_all_files(mocker, fetcher):
    mock_client = mocker.MagicMock()
    mock_loop = mocker.MagicMock()
    mock_client.loop = mock_loop

    mocker.patch("src.fetcher.telegram_fetcher.TelegramClient", return_value=mock_client)

    fetcher.download_all_files()

    # Проверки
    mock_client.__enter__.assert_called_once()
