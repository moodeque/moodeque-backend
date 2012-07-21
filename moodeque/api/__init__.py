import re
import logging
from moodeque.stereomood import StereoMoodClient
from redis import StrictRedis
from pyramid.config import Configurator
log = logging.getLogger(__name__)

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
    config.scan("moodeque.api.views")
    return config.make_wsgi_app()


def redis_connect(request):
    conf = {k.replace("redis.", ""): request.registry.settings[k]
            for k in request.registry.settings
            if k.startswith("redis")}
    log.debug("Connecting to redis: {}".format(conf))
    for opt in ("port", "db"):
        if opt in conf:
            conf[opt] = int(conf[opt])
    conn = StrictRedis(**conf)
    return conn

def stereomood_connect(request):
    conf = {k.replace("stereomood.", ""): request.registry.settings[k]
            for k in request.registry.settings
            if k.startswith("stereomood")}
    log.debug("Connecting to stereomood: {}".format(conf))

    conn = StereoMoodClient(**conf)
    return conn


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.set_request_property("moodeque.api.redis_connect", name="db",
                                reify=True)
    config.set_request_property("moodeque.api.stereomood_connect",
                                name="stereomood", reify=True)
    config.add_route('root', '/')
    config.add_route('venues', '/venues')
    config.add_route('venue', '/venues/{venueid}')
    config.add_route('playlist', '/venues/{venueid}/playlist')
    config.add_route('song', '/venues/{venueid}/playlist/{method}')
    config.add_route('customers', '/venues/{venueid}/people')
    config.add_route('customer', '/venues/{venueid}/people/{uid}')
    config.add_route('people', '/people')
    config.add_route('person', '/people/{uid}')
    config.add_route('login', '/people/{uid}/login')
