from django_dramatiq_pg.tools import make_url


def test_make_url__empty():
    config = {}

    result = make_url(**config)

    assert result == 'postgresql://'


def test_make_url__full():
    config = {
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {'connect_timeout': 10},
        'NAME': 'name'
    }

    result = make_url(**config)

    assert result == 'postgresql://user:password@localhost:5432/name?connect_timeout=10'


def test_make_url__partial():
    config = {
        'USER': 'user',
        'HOST': 'localhost',
        'NAME': 'name'
    }

    result = make_url(**config)

    assert result == 'postgresql://user@localhost/name'


def test_make_url__password_without_user():
    config = {
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'NAME': 'name'
    }

    result = make_url(**config)

    assert result == 'postgresql://:password@localhost/name'


def test_make_url__port_without_host():
    config = {
        'USER': 'user',
        'PORT': '5431',
        'NAME': 'name'
    }

    result = make_url(**config)

    assert result == 'postgresql://user@:5431/name'
