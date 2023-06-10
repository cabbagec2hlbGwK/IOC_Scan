import requests, re


def search(IOC, query):
    url = f"https://ahmia.fi/search/?q={query.replace(' ','+')}"
    MAX_RESULTS = 10
    # re.compile()
    session = IOC.tor_req()
    print(session)

    headers = {
        "Host": "ahmia.fi",
        "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": f"https://ahmia.fi/search/?q={query.replace(' ','+')}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    response = session.get(url, headers=headers)

    print(response.text)


def string():
    return "ahmia"


if __name__ == "__main__":
    search("a", "card")
