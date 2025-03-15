"""Test cases for the ds_protocol module."""
import json
import pytest
from ds_protocol import encode_json, DataTuple, extract_json


def test_encode_join():
    """Test encoding a join message."""
    msg_type = 'join'
    user = 'ohhimark'
    pwd = 'password123'
    json_msg = json.dumps({msg_type: {"username": user,
                                      "password": pwd,
                                      "token": ""}})
    assert encode_json(msg_type=msg_type,
                       username=user,
                       password=pwd) == json_msg


@pytest.mark.xfail
def test_encode_join_fail():
    """Test encoding a join message with empty username, expecting failure."""
    msg_type = 'join'
    user = 'ohhimark'
    pwd = 'password123'
    json_msg = json.dumps({msg_type: {"username": user,
                                      "password": pwd,
                                      "token": ""}})
    assert encode_json(msg_type=msg_type,
                       username="",
                       password=pwd) == json_msg


def test_encode_post():
    """Test encoding a post message."""
    token = 'user_token'
    msg_type = 'post'
    entry = 'Hello World!'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           msg_type: {"entry": entry,
                                      "timestamp": time}})
    assert encode_json(msg_type=msg_type,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


@pytest.mark.xfail
def test_encode_post_fail():
    """Test encoding a post message with empty token, expecting failure."""
    token = 'user_token'
    msg_type = 'post'
    entry = ''
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           msg_type: {"entry": entry,
                                      "timestamp": time}})
    assert encode_json(msg_type=msg_type,
                       message=entry,
                       timestamp=time,
                       token="") == json_msg


def test_encode_bio():
    """Test encoding a bio message."""
    token = 'user_token'
    msg_type = 'bio'
    entry = 'Hello World!'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           msg_type: {"entry": entry,
                                      "timestamp": time}})
    assert encode_json(msg_type=msg_type,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


@pytest.mark.xfail
def test_directmessage_send_fail():
    """Test sending a direct message with empty entry, expecting failure."""
    token = 'user_token'
    msg_type = 'directmessage'
    entry = ''
    user = 'ohhimark'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           msg_type: {"entry": entry,
                                      "recipient": user,
                                      "timestamp": time}})
    assert encode_json(msg_type=msg_type,
                       username=user,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


def test_directmessage_send():
    """Test sending a direct message."""
    token = 'user_token'
    msg_type = 'directmessage'
    entry = 'Hello World!'
    user = 'ohhimark'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           msg_type: {"entry": entry,
                                      "recipient": user,
                                      "timestamp": time}})
    assert encode_json(msg_type=msg_type,
                       username=user,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


def test_directmessage_new():
    """Test encoding a request for new direct messages."""
    token = 'user_token'
    msg_type = 'directmessage'
    entry = 'new'
    json_msg = json.dumps({"token": token,
                           msg_type: entry})
    assert encode_json(msg_type=msg_type,
                       message=entry,
                       token=token) == json_msg


def test_directmessage_all():
    """Test encoding a request for all direct messages."""
    token = 'user_token'
    msg_type = 'directmessage'
    entry = 'all'
    json_msg = json.dumps({"token": token,
                           msg_type: entry})
    assert encode_json(msg_type=msg_type,
                       message=entry,
                       token=token) == json_msg


@pytest.mark.xfail
def test_encode_fail():
    """Test encoding with invalid message type, expecting failure."""
    assert encode_json(msg_type=1234,
                       message="What",
                       token=123456) is False


@pytest.mark.xfail
def test_encode_directmessage_fail():
    """Test encoding a direct message with invalid parameters, expecting
    failure."""
    assert encode_json(msg_type='directmessage',
                       message='what is this?',
                       token='1234') is False


@pytest.mark.xfail
def test_encode_type_fail():
    """Test encoding with an unknown message type, expecting failure."""
    assert encode_json(msg_type='something',
                       message='new',
                       token='1234') is False


# extract_json test cases
def test_extract_error():
    """Test extracting an error message response."""
    string = json.dumps({"response": {"type": "error",
                                      "message": "An error message will "
                                      "be contained here."}})
    assert extract_json(string) == DataTuple('error', 'An error message will '
                                             'be contained here.', '')


def test_extract_join_ok():
    """Test extracting a successful join response."""
    string = json.dumps({"response": {"type": "ok",
                                      "message": "", "token": "user_token"}})
    assert extract_json(string) == DataTuple('ok', '', 'user_token')


def test_extract_directmessage_send():
    """Test extracting a direct message sent confirmation."""
    string = json.dumps({"response": {"type": "ok",
                                      "message": "Direct message sent"}})
    assert extract_json(string) == DataTuple('ok', 'Direct message sent', '')


def test_extract_directmessage_new():
    """Test extracting new direct messages."""
    messages = [{"message": "Are you there?!",
                 "from": "markb", "timestamp": ""},
                {"message": "Bro? what happened?",
                 "from": "thebeemoviescript",
                 "timestamp": "1603167689.3928561"}]
    string = json.dumps({"response": {"type": "ok",
                                      "messages": messages}})
    assert extract_json(string) == DataTuple('ok', messages, '')


def test_extract_directmessage_all():
    """Test extracting all direct messages."""
    messages = [{"message": "Are you there?!",
                 "from": "markb",
                 "timestamp": "1603167689.3928561"},
                {"message": "Yeah I just went to grab some water! Jesus!",
                 "recipient": "markb",
                 "timestamp": "1603167699.3928561"},
                {"message": "Bzzzzz", "from": "thebeemoviescript",
                 "timestamp": "1603167689.3928561"}]
    string = json.dumps({"response": {"type": "ok", "messages": messages}})
    assert extract_json(string) == DataTuple('ok', messages, '')


@pytest.mark.xfail
def test_extract_notjson():
    """Test extracting from non-JSON input, expecting failure."""
    assert extract_json("this is a string") is False


@pytest.mark.xfail
def test_extract_fail_type():
    """Test extracting an unknown response type, expecting failure."""
    string = json.dumps({"response": {"type": "something",
                                      "message": "hi"}})
    assert extract_json(string) is False


@pytest.mark.xfail
def test_extract_fail_nomessage():
    """
    Test extracting a response with missing message field,
    expecting failure.
    """
    string = json.dumps({"response": {"type": "ok",
                                      "messager": "hi"}})
    assert extract_json(string) is False
