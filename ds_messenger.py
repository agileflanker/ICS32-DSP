# Andrew Ngo
# azngo@uci.edu
# 63263981

import socket
import ds_protocol

class DirectMessage:
    def __init__(self, recipient: str = None,
                 message: str = None,
                 timestamp: str = None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
		
    def send(self, message:str, recipient:str) -> bool:
        # must return true if message successfully sent, false if send failed.
        pass
		
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        pass
 
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        pass



def connect_to_server(server: str = '127.0.0.1', port: int = 3001):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        return sock
    except Exception as e:
        return False


def send(server: str, port: int,
         username: str, password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    if not server or not port:
        print("Client error")
        return False
    if not username or not password:
        print("No username or password")
        return False

    client = connect_to_server(server, port)
    if client is False:
        print(f"Error communicating with {server} on port {port}")
        return False

    try:
        while True:
            join_msg = ds_protocol.encode_json(msg_type='join',
                                               username=username,
                                               password=password)
            client.sendall(join_msg + b'\r\n')

            recv = ds_protocol.extract_json(client.recv(4096).decode())
            recv_resp = recv.response
            recv_msg = recv.message

            print("Received server message:", recv_msg)
            if recv_resp == "error" or not recv.token:
                return False
            else:
                token = recv.token

            if message:
                post_msg = ds_protocol.encode_json(msg_type='post',
                                                   message=message,
                                                   token=token)
                client.sendall(post_msg + b'\r\n')
                recv = ds_protocol.extract_json(client.recv(4096).decode())
                recv_resp = recv.response
                recv_msg = recv.message
                print("Received server message:", recv_msg)
                if recv_msg == "error":
                    return False
            if bio:
                bio_msg = ds_protocol.encode_json(msg_type='bio',
                                                  message=bio,
                                                  token=token)
                client.sendall(bio_msg + b'\r\n')
                recv = ds_protocol.extract_json(client.recv(4096).decode())
                recv_resp = recv.response
                recv_msg = recv.message
                print("Received server message:", recv_msg)
                if recv_resp == "error":
                    return False
            client.close()
            return True

    except ValueError as ve:
        print("SOME VALUE ERROR", ve)
        return False
    except Exception as e:
        print(f"Error communicating with server {server}: {e}")
        return False
