def search(IOC, query):
    IOC.cur.execute("SELECT url FROM website WHERE status = 'ACTIVE'")
    links = [
        link[0].replace("https://", "").replace("http://", "")
        for link in IOC.cur.fetchall()
    ]
    return links


def string():
    return "regpages"
