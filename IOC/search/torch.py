import re
from bs4 import BeautifulSoup


def search(IOC, query):
    session = IOC.tor_req()
    print(session)
    url = f"http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P={query.replace(' ','+')}&DEFAULTOP=and&DB=default&FMT=query&xP"
    parameters = ""
    for word in query.replace(" ", "+").split("+"):
        parameters = parameters + f"P=ZB{word}%09ZF{word}%09ZS{word}%09Z{word}"
    try:
        source = session.get(
            "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega"
        )
    except:
        print("TORCH is OFFLINE")
        return
    soup = BeautifulSoup(source.text, "html.parser")
    val = soup.find("input", {"id": "tkn"}).get("value").strip()
    rest = f"DB=default&xFILTERS=.%7E%7E&tkn={val}"

    content = session.get(url + parameters + rest)
    links = []
    soup = BeautifulSoup(content.text, "html.parser")
    for tr in soup.find_all("tr"):
        [
            links.append(
                link.get("href").replace("http://", "").replace("https://", "")
            )
            for link in tr.find_all("a")
        ]
    session.close()
    return links


def string():
    return "torch"
