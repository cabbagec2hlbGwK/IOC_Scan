from bs4 import BeautifulSoup


def search(IOC, query):
    session = IOC.tor_req()
    links = []
    MAX_LOOP = 100
    offset = 0
    for a in range(MAX_LOOP):
        url = f"http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q={query.replace(' ','+')}&offset={offset}"
        offset += 20
        source = session.get(url)
        soup = BeautifulSoup(source.text, "html.parser")
        results = soup.find_all("div", {"class": "result"})
        if not results:
            break
        for result in results:
            links.append(
                result.find("i").text.replace("http://", "").replace("https://", "")
            )
    return links


def string():
    return "haystack"
