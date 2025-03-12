# Andrew Ngo
# azngo@uci.edu
# 63263981

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and
    converts it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        type = json_obj['response']['type']
        if type == 'ok':
            if 'token' in response:
                token = response['token']
            else:
                token = ''
            if 'message' in response:
                message = response['message']
            elif 'messages' in response:
                message = response['messages']
            else:
                raise ValueError("ProtocolError: No message found")
        elif type == 'error':
            message = response['message']
            token = ''
        else:
            raise ValueError(f"ProtocolError: Invalid message type {type}")

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    
    return DataTuple(type=type, message=message, token=token)


def encode_json(msg_type: str,
                username: str = None, password: str = None,
                message: str = None, timestamp=None,
                token: str = None):
    if msg_type == 'join':
        if not username or not password:
            raise ValueError("ProtocolError: No username or password")
        msg = {msg_type: {"username": username,
                          "password": password,
                          "token": ""}}

    elif msg_type == 'post' or msg_type == 'bio':
        if not token or not message:
            raise ValueError("ProtocolError: No token or message")
        msg = {"token": token, 
               msg_type: {"entry": message, "timestamp": timestamp}}

    elif msg_type == 'directmessage':
        if not token or not message:
            raise ValueError("ProtocolError: No token or message")
        if username:
            msg = {"token": token,
                   msg_type: {"entry": message,
                              "recipient": username,
                              "timestamp": timestamp}}
        elif message in ('new', 'all'):
            msg = {"token": token, msg_type: message}
        else:
            raise ValueError("ProtocolError: Invalid directmessage")
    else:
        raise ValueError("ProtocolError: Invalid message type")

    return json.dumps(msg)
