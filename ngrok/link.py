import base64
import datetime
import json
import urllib.request, urllib.error, urllib.parse


PUBLIC_ID = ""
SECRET_TOKEN = ""

class Tunnel:
    def __init__(self, id, clients, proto, public_url, metadata, started_at):
        self.id = id
        self.clients = [Client(x["id"], x["ip"]) for x in clients]
        self.proto = proto
        self.public_url = public_url
        self.metadata = metadata
        self.started_at = datetime.datetime.strptime(started_at, "%Y-%m-%dT%H:%M:%SZ")

    def __repr__(self):
        return "<Tunnel id %s>" % self.id

    def refresh(self):
        data = api("tunnels/%s" % self.id)
        self.clients = [Client(x["id"], x["ip"]) for x in data["clients"]]
        self.proto = data["proto"]
        self.metadata = data["metadata"]


class Client:
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip

    def __repr__(self):
        return "<Client id %s>" % self.id


class Domain:
    def __init__(self, domain, id=None, region="us", uri=None, created_at=None):
        self.id = id
        self.domain = domain
        self.region = region
        self.uri = uri
        self.created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ") \
            if created_at else None

    def __repr__(self):
        return ("<Domain id %s>" % self.id) if self.id else "<pending Domain>"

    def reserve(self):
        if self.id:
            raise Exception("Domain already reserved")
        data = api("reserved_domains", "POST", {"name": self.domain, "region": self.region})
        self.id = data["id"]
        self.uri = data["uri"]
        self.created_at = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    def release(self):
        if not self.id:
            raise Exception("Domain not yet reserved")
        api("reserved_domains/%s" % self.id, "DELETE")
        self.id = None
        self.uri = None
        self.created_at = None


class Address:
    def __init__(self, addr=None, id=None, region="us", uri=None, created_at=None):
        self.id = id
        self.addr = addr
        self.region = region
        self.uri = uri
        self.created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ") \
            if created_at else None

    def __repr__(self):
        return ("<Address id %s>" % self.id) if self.id else "<pending Address>"

    def reserve(self):
        if self.id:
            raise Exception("Address already reserved")
        data = api("reserved_addrs", "POST", {"region": self.region})
        self.id = data["id"]
        self.addr = data["addr"]
        self.uri = data["uri"]
        self.created_at = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    def release(self):
        if not self.id:
            raise Exception("Address not yet reserved")
        api("reserved_addrs/%s" % self.id, "DELETE")
        self.id = None
        self.addr = None
        self.uri = None
        self.created_at = None


class Credential:
    def __init__(
            self, id=None, uri=None, token="", description=None, acl=["*"],
            created_at=None):
        self.id = id
        self.uri = uri
        self.token = token
        self.description = description
        self.acl = acl
        self.created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ") \
            if created_at else None

    def __repr__(self):
        return ("<Credential id %s>" % self.id) if self.id else "<pending Credential>"

    def create(self):
        if self.id:
            raise Exception("Credential already created")
        data = api("credentials", "POST",
            {"description": self.description, "acl": self.acl})
        self.id = data["id"]
        self.token = data["token"]
        self.uri = data["uri"]
        self.created_at = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    def revoke(self):
        if not self.id:
            raise Exception("Credential not yet created")
        api("credentials/%s" % self.id, "DELETE")
        self.id = None
        self.uri = None
        self.token = None
        self.description = None
        self.acl = ["*"]
        self.created_at = None


def api(endpoint, method="GET", data=None):
    if not PUBLIC_ID or not SECRET_TOKEN:
        raise Exception("Public ID and secret token must be declared")
    authstr = base64.encodestring('%s:%s' % (PUBLIC_ID, SECRET_TOKEN)).replace('\n', '')
    request = urllib.request.Request("https://api.ngrok.com/%s" % endpoint)
    if method != "GET":
        request.get_method = lambda: method
    request.add_header("Authorization", "Basic %s" % authstr)
    request.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(request, json.dumps(data) if data else None)
    try:
        return json.loads(response.read())
    except:
        return None

def get_tunnels():
    tunnels = []
    for x in api("tunnels")["tunnels"]:
        tunnel = Tunnel(x["id"], x["clients"], x["proto"], x["public_url"],
            x["metadata"], x["started_at"])
        tunnels.append(tunnel)
    return tunnels

def get_tunnel(id):
    try:
        data = api("tunnels/%s" % str(id))
        return Tunnel(data["id"], data["clients"], data["proto"], data["public_url"],
            data["metadata"], data["started_at"])
    except:
        return None

def get_domains():
    domains = []
    for x in api("reserved_domains")["reserved_domains"]:
        domain = Domain(x["domain"], x["id"], x["region"], x["uri"], x["created_at"])
        domains.append(domain)
    return domains

def get_domain(id):
    try:
        data = api("reserved_domains/%s" % str(id))
        return Domain(data["domain"], data["id"], data["region"], data["uri"],
            data["created_at"])
    except:
        return None

def get_tcp_addresses():
    addresses = []
    for x in api("reserved_addrs")["reserved_addrs"]:
        address = Address(x["addr"], x["id"], x["region"], x["uri"], x["created_at"])
        addresses.append(address)
    return addresses

def get_tcp_address(id):
    try:
        data = api("reserved_addrs/%s" % str(id))
        return Address(data["addr"], data["id"], data["region"], data["uri"],
            data["created_at"])
    except:
        return None

def get_credentials():
    credentials = []
    for x in api("credentials")["credentials"]:
        credential = Credential(x["id"], x["uri"], x["token"], x["description"],
            x["acl"], x["created_at"])
        credentials.append(credential)
    return credentials

def get_credential(id):
    try:
        data = api("credentials/%s" % str(id))
        return Credential(data["id"], data["uri"], data["token"], data["description"],
            data["acl"], data["created_at"])
    except:
        return None
