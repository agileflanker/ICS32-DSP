import pytest
from ds_messenger import *

dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')

def test_send_valid(dm = dm, dm2 = dm2):
    assert dm.send('Test', 'asdf') == True
    assert dm2.send('Test2', 'qwer') == True

def test_send_fail(dm = dm, dm2 = dm2):
    assert dm.send('FailTest', 'asdfqw') == False
    assert dm2.send('FailTest', 'qwerty') == False

def test_retrieve_new(dm = dm, dm2 = dm2):
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()

    assert type(msgs1) == list
    assert len(msgs1) == 1
    assert type(msgs1[0]) == DirectMessage
    assert msgs1[0].sender == 'asdf'
    assert msgs1[0].message == 'Test2'
    assert type(msgs2) == list
    assert len(msgs2) == 1
    assert type(msgs2[0]) == DirectMessage
    assert msgs2[0].sender == 'qwer'
    assert msgs2[0].message == 'Test'
    
def test_retrieve_all(dm = dm, dm2 = dm2):
    msgs1 = dm.retrieve_all()
    msgs2 = dm2.retrieve_all()

    assert type(msgs1) == list
    assert len(msgs1) == 2
    assert type(msgs1[0]) == DirectMessage
    assert msgs1[0].recipient == 'asdf'
    assert msgs1[0].message == 'Test'
    assert msgs1[1].sender == 'asdf'
    assert msgs1[1].message == 'Test2'
    assert type(msgs2) == list
    assert len(msgs2) == 2
    assert type(msgs2[0]) == DirectMessage
    assert msgs2[0].sender == 'qwer'
    assert msgs2[0].message == 'Test'
    assert msgs2[1].recipient == 'qwer'
    assert msgs2[1].message == 'Test2'

def test_retrieve_new_none(dm = dm, dm2 = dm2):
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()

    assert type(msgs1) == list
    assert len(msgs1) == 0
    assert type(msgs2) == list
    assert len(msgs2) == 0

def test_retrieve_all_error(dm = dm, dm2 = dm2):
    dm.token = "invalid"
    dm2.token = "invalid2"

    msgs1 = dm.retrieve_all()
    msgs2 = dm2.retrieve_all()
    assert msgs1 == 'Invalid user token.'
    assert msgs2 == 'Invalid user token.'

def test_retrieve_new_error(dm = dm, dm2 = dm2):
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()
    assert msgs1 == 'Invalid user token.'
    assert msgs2 == 'Invalid user token.'
