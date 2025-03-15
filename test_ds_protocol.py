from ds_protocol import *
import pytest


# encode_json test cases
def test_encode_join():
    type = 'join'
    user = 'ohhimark'
    pwd = 'password123'
    json_msg = json.dumps({type: {"username": user,
                                  "password": pwd,
                                  "token": ""}})
    assert encode_json(msg_type=type,
                       username=user,
                       password=pwd) == json_msg


@pytest.mark.xfail
def test_encode_join_fail():
    type = 'join'
    user = 'ohhimark'
    pwd = 'password123'
    json_msg = json.dumps({type: {"username": user,
                                  "password": pwd,
                                  "token": ""}})
    assert encode_json(msg_type=type,
                       username="",
                       password=pwd) == json_msg


def test_encode_post():
    token = 'user_token'
    type = 'post'
    entry = 'Hello World!'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           type: {"entry": entry,
                                  "timestamp": time}})
    assert encode_json(msg_type=type,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


@pytest.mark.xfail
def test_encode_post_fail():
    token = 'user_token'
    type = 'post'
    entry = ''
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           type: {"entry": entry,
                                  "timestamp": time}})
    assert encode_json(msg_type=type,
                       message=entry,
                       timestamp=time,
                       token="") == json_msg


def test_encode_bio():
    token = 'user_token'
    type = 'bio'
    entry = 'Hello World!'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           type: {"entry": entry,
                                  "timestamp": time}})
    assert encode_json(msg_type=type,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


@pytest.mark.xfail
def test_directmessage_send_fail():
    token = 'user_token'
    type = 'directmessage'
    entry = ''
    user = 'ohhimark'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           type: {"entry": entry,
                                  "recipient": user,
                                  "timestamp": time}})
    assert encode_json(msg_type=type,
                       username=user,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


def test_directmessage_send():
    token = 'user_token'
    type = 'directmessage'
    entry = 'Hello World!'
    user = 'ohhimark'
    time = 1603167689.3928561
    json_msg = json.dumps({"token": token,
                           type: {"entry": entry,
                                  "recipient": user,
                                  "timestamp": time}})
    assert encode_json(msg_type=type,
                       username=user,
                       message=entry,
                       timestamp=time,
                       token=token) == json_msg


def test_directmessage_new():
    token = 'user_token'
    type = 'directmessage'
    entry = 'new'
    json_msg = json.dumps({"token": token,
                           type: entry})
    assert encode_json(msg_type=type,
                       message=entry,
                       token=token) == json_msg


def test_directmessage_all():
    token = 'user_token'
    type = 'directmessage'
    entry = 'all'
    json_msg = json.dumps({"token": token,
                           type: entry})
    assert encode_json(msg_type=type,
                       message=entry,
                       token=token) == json_msg


@pytest.mark.xfail
def test_encode_fail():
    assert encode_json(msg_type=1234,
                       message="What",
                       token=123456) is False


@pytest.mark.xfail
def test_encode_directmessage_fail():
    assert encode_json(msg_type='directmessage',
                       message='what is this?',
                       token='1234') is False


@pytest.mark.xfail
def test_encode_type_fail():
    assert encode_json(msg_type='something',
                       message='new',
                       token='1234') is False


# extract_json test cases
def test_extract_error():
    string = json.dumps({"response": {"type": "error",
                                      "message": "An error message will "
                                      "be contained here."}})
    assert extract_json(string) == DataTuple('error', 'An error message will '
                                             'be contained here.', '')


def test_extract_join_ok():
    string = json.dumps({"response": {"type": "ok",
                                      "message": "", "token": "user_token"}})
    assert extract_json(string) == DataTuple('ok', '', 'user_token')


def test_extract_directmessage_send():
    string = json.dumps({"response": {"type": "ok",
                                      "message": "Direct message sent"}})
    assert extract_json(string) == DataTuple('ok', 'Direct message sent', '')


def test_extract_directmessage_new():
    messages = [{"message": "Are you there?!",
                 "from": "markb", "timestamp": ""},
                {"message": "Bro? what happened?",
                 "from": "thebeemoviescript",
                 "timestamp": "1603167689.3928561"}]
    string = json.dumps({"response": {"type": "ok",
                                      "messages": messages}})
    assert extract_json(string) == DataTuple('ok', messages, '')


def test_extract_directmessage_all():
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
    assert extract_json("this is a string") is False


@pytest.mark.xfail
def test_extract_fail_type():
    string = json.dumps({"response": {"type": "something",
                                      "message": "hi"}})
    assert extract_json(string) is False


@pytest.mark.xfail
def test_extract_fail_nomessage():
    string = json.dumps({"response": {"type": "ok",
                                      "messager": "hi"}})
    assert extract_json(string) is False
