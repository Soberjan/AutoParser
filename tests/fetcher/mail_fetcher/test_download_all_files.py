import os
import shutil
import tempfile

import pytest

from src.fetcher.mail_fetcher import MailFetcher

def test_download_all_files(mocker):
    temp_dir = tempfile.mkdtemp()

    mock_imap = mocker.MagicMock()
    mocker.patch('src.fetcher.mail_fetcher.imapclient.IMAPClient', return_value=mock_imap)
    mock_imap.search.return_value = [1]
    mock_imap.fetch.return_value = {
        1: {b'BODY[]': b'raw email bytes'}
    }

    mock_part = mocker.MagicMock()
    mock_part.filename = 'example.txt'
    mock_part.get_payload.return_value = b'hello from mock'

    mock_message = mocker.MagicMock()
    mock_message.mailparts = [mock_part]
    mocker.patch('src.fetcher.mail_fetcher.pyzmail.PyzMessage.factory', return_value=mock_message)

    mock_logger = mocker.MagicMock()
    mock_logger.info.return_value = 'downloaded file!'
    mocker.patch('src.fetcher.mail_fetcher.logger', return_value=mock_logger)

    fetcher = MailFetcher(
        download_folder=temp_dir,
        email='user@example.com',
        password='password123',
        imap_server='imap.example.com'
    )
    fetcher.download_all_files()

    saved_file = os.path.join(temp_dir, 'example.txt')
    assert os.path.exists(saved_file)
    with open(saved_file, 'rb') as f:
        content = f.read()
        assert content == b'hello from mock'

    shutil.rmtree(temp_dir)
