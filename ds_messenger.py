# Andrew Ngo
# azngo@uci.edu
# 63263981

'''
DSU client for a ICS32 DSP.
Allows a user to communicate with other users on the server.
'''

import socket
import ds_protocol


class DirectMessage:
    '''
    Class for storing direct messages sent and received by users
    '''
    def __init__(self):
        self.sender = None
        self.recipient = None
        self.message = None
        self.timestamp = None

    def to_dict(self):
        '''
        Method for converting a DirectMessage object to a dictionary.
        '''
        msg = {}
        if self.sender:
            msg['from'] = self.sender
        else:
            msg['recipient'] = self.recipient
        msg['message'] = self.message
        msg['timestamp'] = self.timestamp
        return msg


class DirectMessenger:
    '''
    Client class that handles communication between users on a DSU server.
    Returns True if successful, False if unsuccessful
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.client = connect_to_server(dsuserver)
        data = join_server(self.client, username, password)
        self.token = data

    def send(self, message: str, recipient: str) -> bool:
        '''
        Attempts to send a message to the specified recipient.
        '''
        if self.token is None:
            return False
        json = ds_protocol.encode_json(msg_type='directmessage',
                                       username=recipient,
                                       message=message,
                                       token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4096).strip())
        recv_type = recv.msg_type
        return recv_type == 'ok'

    def retrieve_new(self) -> list:
        '''
        Attempts to retrieve unread messages from the server. If successful,
        returns a list of DirectMessage objects containing the contents.
        Returns an error message if unsuccessful.
        '''
        if self.token is None:
            return None
        json = ds_protocol.encode_json(msg_type='directmessage',
                                       message='new',
                                       token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4096).strip())
        if recv.msg_type == 'ok':
            lines = recv.message
            new_msgs = []
            for line in lines:
                dm = DirectMessage()
                dm.sender = line['from']
                dm.message = line['message']
                dm.timestamp = line['timestamp']
                new_msgs.append(dm)
            return new_msgs
        return recv.message

    def retrieve_all(self) -> list:
        '''
        Retrieves all messages, both sent and received, from the server. If
        successful, returns a list of DirectMessage objects. If unsuccessful,
        returns an error message.
        '''
        if self.token is None:
            return None
        json = ds_protocol.encode_json(msg_type='directmessage',
                                       message='all',
                                       token=self.token).encode()
        self.client.sendall(json + b'\r\n')
        recv = ds_protocol.extract_json(self.client.recv(4069).strip())
        if recv.msg_type == 'ok':
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
        return recv.message


def join_server(client: socket,
                username: str, password: str) -> ds_protocol.DataTuple:
    '''
    Helper method that takes a client socket connected to a server and sends a
    join message to join the server. Returns the token received by the server
    if successful. Returns None if unsuccessful.
    '''
    if not client:
        return None
    join_msg = ds_protocol.encode_json('join',
                                       username,
                                       password).encode()
    client.sendall(join_msg + b'\r\n')
    recv = client.recv(4096).decode().strip()
    data = ds_protocol.extract_json(recv)
    return data.token


def connect_to_server(server):
    '''
    Helper method that creates a socket and connects to the server. Returns the
    socket.
    '''
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, 3001))
        return client
    except ConnectionRefusedError:
        return None
    except socket.gaierror:
        return None
