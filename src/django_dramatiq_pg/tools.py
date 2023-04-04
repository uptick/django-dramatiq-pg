from urllib.parse import urlunparse

__all__ = (
    'make_url',
)


def make_url(**config):
    user = config.get('USER', '')
    password = config.get('PASSWORD', '')
    host = config.get('HOST') or '__no_host__'
    port = config.get('PORT', '')
    options = config.get('OPTIONS', {})
    path = config.get('NAME', '')

    creds = f'{user}:{password}' if (user and password or password) else user
    conn = f'{host}:{port}' if (host and port or port) else host
    netloc = f'{creds}@{conn}' if creds and conn else conn

    query = '&'.join([f'{k}={v}' for k, v in options.items()])

    url = urlunparse(('postgresql', netloc, path, '', query, ''))

    return url.replace('__no_host__', '')
