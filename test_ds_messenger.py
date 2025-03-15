'''
Testing module for ds_messenger
'''


from ds_messenger import DirectMessage, DirectMessenger, \
    connect_to_server, join_server


def test_to_dict():
    '''
    Tests the to_dict() method of a DirectMessage object
    '''
    dm_obj = DirectMessage()
    dm_obj.sender = 'asdf'
    dm_obj.message = 'asdf'
    dm_obj.timestamp = 'asdf'
    dm_obj2 = DirectMessage()
    dm_obj2.recipient = 'qwer'
    dm_obj2.message = 'qwer'
    dm_obj2.timestamp = 'qwer'
    assert dm_obj.to_dict() == {'from': 'asdf',
                                'message': 'asdf',
                                'timestamp': 'asdf'}
    assert dm_obj2.to_dict() == {'recipient': 'qwer',
                                 'message': 'qwer',
                                 'timestamp': 'qwer'}


def test_no_client():
    '''
    Tests the connect_to_server() and join_server() helper functions
    '''
    assert connect_to_server('127') is None
    assert connect_to_server('127.0.0.2') is None
    assert join_server(None, 'asdf', 'asdf') is None


def test_send_valid():
    '''
    Tests the send function with a valid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    assert dm.send('Test', 'asdf') is True
    assert dm2.send('Test2', 'qwer') is True


def test_send_fail():
    '''
    Tests the send function with an invalid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    assert dm.send('FailTest', 'asdfqw') is False
    assert dm2.send('FailTest', 'qwerty') is False


def test_retrieve_new():
    '''
    Tests the retrieve_new function with a valid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()

    assert isinstance(msgs1, list)
    assert len(msgs1) == 1
    assert isinstance(msgs1[0], DirectMessage)
    assert msgs1[0].sender == 'asdf'
    assert msgs1[0].message == 'Test2'
    assert isinstance(msgs2, list)
    assert len(msgs2) == 1
    assert isinstance(msgs2[0], DirectMessage)
    assert msgs2[0].sender == 'qwer'
    assert msgs2[0].message == 'Test'


def test_retrieve_all():
    '''
    Tests the retrieve_all function with a valid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    msgs1 = dm.retrieve_all()
    msgs2 = dm2.retrieve_all()

    assert isinstance(msgs1, list)
    assert len(msgs1) == 2
    assert isinstance(msgs1[0], DirectMessage)
    assert msgs1[0].recipient == 'asdf'
    assert msgs1[0].message == 'Test'
    assert msgs1[1].sender == 'asdf'
    assert msgs1[1].message == 'Test2'
    assert isinstance(msgs2, list)
    assert len(msgs2) == 2
    assert isinstance(msgs2[0], DirectMessage)
    assert msgs2[0].sender == 'qwer'
    assert msgs2[0].message == 'Test'
    assert msgs2[1].recipient == 'qwer'
    assert msgs2[1].message == 'Test2'


def test_retrieve_new_none():
    '''
    Tests retrieve_new with no new messages
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()

    assert isinstance(msgs1, list)
    assert len(msgs1) == 0
    assert isinstance(msgs2, list)
    assert len(msgs2) == 0


def test_retrieve_all_error():
    '''
    Tests retrieve_all with an invalid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    dm.token = "invalid"
    dm2.token = "invalid2"

    msgs1 = dm.retrieve_all()
    msgs2 = dm2.retrieve_all()
    assert msgs1 == 'Invalid user token.'
    assert msgs2 == 'Invalid user token.'


def test_retrieve_new_error():
    '''
    Tests retrieve_new with an invalid call
    '''
    dm = DirectMessenger('127.0.0.1', 'qwer', 'qwer')
    dm2 = DirectMessenger('127.0.0.1', 'asdf', 'asdf')
    dm.token = "invalid"
    dm2.token = "invalid2"
    msgs1 = dm.retrieve_new()
    msgs2 = dm2.retrieve_new()
    assert msgs1 == 'Invalid user token.'
    assert msgs2 == 'Invalid user token.'
