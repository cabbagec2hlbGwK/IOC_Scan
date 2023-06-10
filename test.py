import requests
import socks

# Set the proxy information
proxy_ip = "127.0.0.1"  # Tor proxy IP address
proxy_port = 9050  # Tor proxy port

# Create a session and set the proxy
session = requests.session()
session.proxies = {
    "http": f"socks5://{proxy_ip}:{proxy_port}",
    "https": f"socks5://{proxy_ip}:{proxy_port}",
}

# Perform a request through the Tor proxy
response = session.get("https://google.com")

# Print the response content
print(response.content)
