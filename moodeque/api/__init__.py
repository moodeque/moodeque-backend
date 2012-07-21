import re
from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    version = settings['moodeque.api.version']
    base_url = settings.get('moodeque.api.prefix', 'api')
    base_url = base_url if not base_url.startswith("/") else base_url[1:]
    if not re.match("v\d", version):
        raise ValueError("Invalid version {0}", version)
    prefix = "/{0}/{1}".format(base_url, version)
    config.include(includeme, route_prefix=prefix)
    config.scan()
    return config.make_wsgi_app()

def includeme(config):
    add_routes(config)

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')
    config.add_route('venues', '/venues')
    config.add_route('venue', '/venues/{venueid}')
    config.add_route('playlist', '/venues/{venue}/playlist')
    config.add_route('song', '/venues/{venue}/playlist/{method}')
    config.add_route('customers', '/venues/{venue}/people')
    config.add_route('customer', '/venues/{venue}/people/{uid}')
    config.add_route('people', '/people')
    config.add_route('person', '/people/{uid}')
    config.add_route('login', '/people/{uid}/login')
    config.add_route('mood', '/people/{uid}/mood')
