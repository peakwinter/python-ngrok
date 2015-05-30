# python-ngrok

Python bindings for ngrok local and Link APIs


## Use with local ngrok setups

If your ngrok server is not running at `http://localhost:4040` you need to set your base url like so:
```
>>> import ngrok
>>> ngrok.client.BASE_URL = "http://localhost:8765"
```

#### Tunnels
- Get all tunnels: `ngrok.client.get_tunnels()`
- Get tunnel by ID: `ngrok.client.get_tunnel(id)`

#### Requests
Only available on introspected tunnels.
- Get all requests: `ngrok.client.get_requests()`
- Get all requests for a specific tunnel: `ngrok.client.get_tunnel(id).get_requests()`
- Get request by ID: `ngrok.client.get_request(id)`
- Replay request: `ngrok.client.get_request(id).replay()`


## Use with ngrok link

First set your public ID and secret tokens like so:

```
>>> import ngrok
>>> ngrok.link.PUBLIC_ID = "my_public_id"
>>> ngrok.link.SECRET_TOKEN = "my_secret_token"
```

#### Tunnels
 - Get all tunnels: `ngrok.link.get_tunnels()`
 - Get tunnel by ID: `ngrok.link.get_tunnel(id)`

#### Domains
 - Get all reserved domains: `ngrok.link.get_domains()`
 - Get reserved domain by ID: `ngrok.link.get_domain(id)`
 - Reserve new domain: `ngrok.link.Domain("mydomain.net").reserve()`
 - Release existing reservation: `ngrok.link.get_domain(id).release()`

#### TCP Addresses
 - Get all reserved TCP addresses: `ngrok.link.get_tcp_addresses()`
 - Get reserved TCP address by ID: `ngrok.link.get_tcp_address(id)`
 - Reserve new TCP address: `ngrok.link.Address().reserve()`
 - Release existing TCP address reservation: `ngrok.link.get_tcp_address(id).release()`

#### Credentials
 - Get all client credentials: `ngrok.link.get_credentials()`
 - Get client credential by ID: `ngrok.link.get_credential(id)`
 - Create a new client credential: `ngrok.link.Credential(description, acl).create()`
 - Revoke an existing client credential: `ngrok.link.get_credential(id).revoke()`
