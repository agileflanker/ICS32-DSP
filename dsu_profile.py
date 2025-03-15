# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS
# CODE RIGHT NOW, though can you certainly take a look at it if you are curious
# since we already covered a bit of the JSON format in class.

'''
The dsu_profile module allows a user to save their information to a DSU file or
load information from an existing DSU file to a Profile object.
'''

import json
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to load or save Profile objects to
    file the system.
    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to deserialize a dsu file to a
    Profile object.
    """


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU
    server. You will need to use this class to manage the information provided
    by each new user created within your program for a2. Pay close attention to
    the properties and functions in this class as you will need to make use of
    each of them in your program.

    When creating your program you will need to collect user input for the
    properties exposed by this class. A Profile class should ensure that a
    username and password are set, but contains no conventions to do so. You
    should make sure that your code verifies that required properties are set.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username    # REQUIRED
        self.password = password    # REQUIRED
        self._friends = []
        self._messages = []

    def save_messages(self, msgs: list) -> None:
        '''
        save_messages appends all messages passed in to the end of profile
        object's ._messages attribute.
        '''
        for msg in msgs:
            self._messages.append(msg)
            if 'from' in msg:
                self.save_friends(msg['from'])
            else:
                self.save_friends(msg['recipient'])

    def overwrite_messages(self, msgs: list):
        '''
        overwrite_messages replaces the _messages attribute with the new list
        of messages.
        '''
        self._messages = []
        self.save_messages(msgs)

    def save_friends(self, friend: str):
        '''
        appends a friend to the end of the ._friends attribute if the name is
        not in the list.
        '''
        if friend not in self._friends:
            self._friends.append(friend)

    def get_messages(self) -> list:
        '''
        returns all messages
        '''
        return self._messages

    def get_friends(self) -> list:
        '''
        returns all friends
        '''
        return self._friends

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        p = Path(path)
        p.touch()

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f)
                    f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU"
                                   "file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data
        stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self._friends = obj['_friends']
                    for msg_obj in obj['_messages']:
                        self._messages.append(msg_obj)

                    f.close()

            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()
