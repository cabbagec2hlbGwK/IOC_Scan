import re, datetime


def insert(IOC, group, link):
    IOC.cur.execute(
        f"""INSERT INTO ransomware_groups (name, link)
    VALUES ('{group}','{link}')
    ON CONFLICT (name, link)
    DO NOTHING;"""
    )


def update(IOC):
    session = IOC.tor_req()
    data = session.get(
        "https://ransom.insicurezzadigitale.com/stats.php?page=groups-stats"
    )
    pattern = r"data:\s*{\s*labels:\s*\[([^\]]*)\]"
    match = re.search(pattern, data.text)
    for group in match.group(1).replace('"', "").split(","):
        data = session.get(
            f"https://ransom.insicurezzadigitale.com/stats.php?page=group-profile&group={group}"
        )
        pattern = r"https?://(?:[a-zA-Z0-9.-]+\.)?onion(?:/[a-zA-Z0-9./?%&_=-]*)?"
        links = re.findall(pattern, data.text)
        for link in links:
            insert(IOC, group=group, link=link)


def list(IOC):
    IOC.cur.execute("SELECT * FROM ransomware_groups")
    return IOC.cur.fetchall()


def group_search(IOC, name):
    IOC.cur.execute(f"SELECT * FROM ransomware_groups WHERE name like {name}")
    return IOC.cur.fetchall()


def keyword_search(IOC, keyword):
    done = False
    groups = list(IOC=IOC)
    for group in groups:
        link = group[2]
        if (
            link
            in "http://blogvl7tjyjvsfthobttze52w36wwiz34hrfcmorgvdzb6hikucb7aqd.onion/"
        ):
            # done = False
            print("cjan")
        if done:
            continue
        try:
            IOC.browser.get(link)
            data = IOC.browser.page_source
            document = {
                "URL": link,
                "contents": data,
                "date": datetime.datetime.now().isoformat(),
            }
            response = IOC.es.index(index="ransom_groups_data", body=document)
            if "result" in response and response["result"] == "created":
                print("Document indexed successfully.")
            else:
                print("Document indexing failed.")
        except Exception as e:
            pass


if __name__ == "__main__":
    pass
