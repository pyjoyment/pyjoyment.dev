import pytest


# A failed assertion of the chain raises AssertionError, with what it got and what it expected
def test_hello(t):
    t.get_ok('/hello').status_is(200).json_is('/hello', 'World')


@pytest.mark.parametrize('name', ['Sara', 'Zoë'])
def test_hello_name(t, name):
    t.get_ok(f'/hello/{name}').status_is(200).json_is({'hello': name})


def test_echo(t):
    t.websocket_ok('/echo').send_ok('hi').message_ok().message_is('echo: hi').finish_ok()
