import datetime
import json
import urllib2
from urllib import urlencode

from collections import namedtuple


BASE_URL = ""

class Tunnel:
    def __init__(
            self, config={}, name=None, uri=None, public_url=None,
            proto=None, metrics=None):
        self.config = config
        self.name = name
        self.uri = uri
        self.public_url = public_url
        self.proto = proto
        self.metrics = metrics

    def __repr__(self):
        return ("<Tunnel '%s'>" % self.config["addr"]) \
            if self.config.get("addr", None) else "<pending Tunnel>"

    def _set(self, data={}):
        self.config = data["config"] if data else {}
        self.name = data["name"] if data else None
        self.uri = data["uri"] if data else None
        self.public_url = data["public_url"] if data else None
        self.proto = data["proto"] if data else None
        self.metrics = data["metrics"] if data else None

    def refresh(self):
        if not self.name:
            raise Exception("Tunnel not yet started")
        data = api("tunnels/%s" % self.name)
        self._set(data)

    def start(self):
        if self.name:
            raise Exception("Tunnel already started")
        data = api("tunnels", "POST", self.config)
        self._set(data)

    def stop(self):
        api("tunnels/%s" % self.name, "DELETE")
        self._set()


class Request:
    def __init__(self, id, tunnel, remote_addr, start, duration, request, response):
        self.id = id
        self.remote_addr = remote_addr
        self.start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        self.duration = duration
        self.request = namedtuple("Request", request.keys())(**request)
        self.response = namedtuple("Response", response.keys())(**response)
        try:
            data = api("tunnels/%s" % tunnel)
            self.tunnel = Tunnel(data["config"], data["name"], data["uri"],
                data["public_url"], data["proto"], data["metrics"])
        except:
            self.tunnel = None

    def __repr__(self):
        return "<Request id %s>" % self.id

    def replay(self):
        api("requests/http", "POST",
            {"id": self.id, "tunnel_name": self.tunnel.name if self.tunnel else None})


def api(endpoint, method="GET", data=None, params=[]):
    base_url = BASE_URL or "http://127.0.0.1:4040/"
    request = urllib2.Request("%sapi/%s" % (base_url, endpoint))
    if method != "GET":
        request.get_method = lambda: method
    if params:
        endpoint += "?%s" % urlencode([(x, params[x]) for x in params])
    request.add_header("Content-Type", "application/json")
    response = urllib2.urlopen(request, json.dumps(data) if data else None)
    try:
        return json.loads(response.read())
    except:
        return None

def get_tunnels():
    tunnels = []
    for x in api("tunnels")["tunnels"]:
        tunnel = Tunnel(x["config"], x["name"], x["uri"], x["public_url"],
            x["proto"], x["metrics"])
        tunnels.append(tunnel)
    return tunnels

def get_tunnel(id):
    try:
        data = api("tunnels/%s" % str(id))
        return Tunnel(data["config"], data["name"], data["uri"], data["public_url"],
            data["proto"], data["metrics"])
    except:
        return None

def get_requests():
    requests = []
    for x in api("requests/http")["requests"]:
        request = Request(x["id"], x["tunnel_name"], x["remote_addr"], x["start"],
            x["duration"], x["request"], x["response"])
        requests.append(request)
    return requests

def get_tunnel(id):
    try:
        data = api("requests/http/%s" % str(id))
        return Request(x["id"], x["tunnel_name"], x["remote_addr"], x["start"],
            x["duration"], x["request"], x["response"])
    except:
        return None
