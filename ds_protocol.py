# Andrew Ngo
# azngo@uci.edu
# 63263981

'''
ds_protocol allows a client to parse messages received by a DSU server and
encode messages sent to the server.
'''

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['msg_type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and
    converts it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        msg_type = json_obj['response']['type']
        if msg_type == 'ok':
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
        elif msg_type == 'error':
            message = response['message']
            token = ''
        else:
            raise ValueError(f"ProtocolError: Invalid message type {msg_type}")

    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(msg_type=msg_type, message=message, token=token)


def encode_json(msg_type: str,
                username: str = None, password: str = None,
                message: str = None, timestamp=None,
                token: str = None):
    '''
    Encodes message types of ('join', 'post', 'bio', 'directmessage').
    'join' requires a username and password
    'post' & 'bio' requirse a token received from the server and a message
    'directmessage' requires a token and three types of messages.
    If 'all', encodes a request for all messages saved in a user.
    If 'new', encodes a request for new messages sent to a user.
    Else, requires a username to send the message to.

    '''
    if msg_type == 'join':
        if not username or not password:
            raise ValueError("ProtocolError: No username or password")
        msg = {msg_type: {"username": username,
                          "password": password,
                          "token": ""}}

    elif msg_type in ('post', 'bio'):
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
