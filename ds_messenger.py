# Andrew Ngo
# azngo@uci.edu
# 63263981

import socket
import ds_protocol
from collections import namedtuple

class DirectMessage:
    def __init__(self):
        self.sender = None
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    '''
    User immediately joins the server provided a username and password

    dsuserver: IP address of the server
    username: username associated with a profile
    password: password associated with a profile
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.client = connect_to_server(dsuserver)
        data = join_server(self.client, username, password)
        self.token = data.token

    def send(self, message:str, recipient:str) -> bool:
        print(self.token)
        print(message)
        print(recipient)
        json = ds_protocol.encode_json(msg_type='directmessage',
                                        username=recipient,
                                        message=message,
                                        token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4096).strip())
        type = recv.type
        if type == 'ok':
            return True
        else:
            return False

    def retrieve_new(self) -> list:
        json = ds_protocol.encode_json(msg_type='directmessage',
                                        message='new',
                                        token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4096).strip())
        if recv.type == 'ok':
            lines = recv.message
            new_msgs = []
            for line in lines:
                dm = DirectMessage()
                dm.sender = line['from']
                dm.message = line['message']
                dm.timestamp = line['timestamp']
                new_msgs.append(dm)
            return new_msgs
        else:
            return recv.message
 
    def retrieve_all(self) -> list:
        json = ds_protocol.encode_json(msg_type='directmessage',
                                       message='all',
                                       token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4069).strip())
        if recv.type == 'ok':
            lines = recv.message
            all_msgs = []
            for line in lines:
                dm = DirectMessage()
                if 'recipient' in line:
                    dm.recipient = line['recipient']
                else:
                    dm.sender = line['from']
                
                dm.message = line['message']
                dm.timestamp = line['timestamp']
                all_msgs.append(dm)
            return all_msgs
        else:
            return None

def join_server(client: socket, username: str, password: str) -> ds_protocol.DataTuple:
        join_msg = ds_protocol.encode_json('join',
                                           username,
                                           password).encode()
        client.sendall(join_msg + b'\r\n')
        recv = client.recv(4096).decode().strip()
        data = ds_protocol.extract_json(recv)
        return data

def connect_to_server(server):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, 3001))
    return client

