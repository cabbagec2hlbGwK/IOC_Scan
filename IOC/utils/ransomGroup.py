import re, datetime, sys
from loguru import logger

# Setting the loging
logger.add(sys.stdout)


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


def index_search(IOC, search_word):
    index_name = "ransom_groups_data"
    links = []
    # Search query
    # search_query = {"query": {"term": {"contents.keyword": search_word.lower()}}}
    search_query = {"query": {"match": {"contents": search_word}}}
    # search_query = {"query": {"wildcard": {"contents": f"*{search_word}*"}}}

    try:
        response = IOC.es.search(index=index_name, body=search_query)
        hits = response["hits"]["hits"]

        # Print the search results
        for hit in hits:
            source = hit["_source"]
            if source.get("URL", "NULL") not in links:
                links.append(source.get("URL", "NULL"))
        return links
    except Exception as e:
        print(f"Error: {e}")


def index_update(IOC):
    done = False
    groups = list(IOC=IOC)
    logger.debug(groups)
    for group in groups:
        link = group[2]
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
                logger.success(
                    f"Document indexed successfully. for ID:{group[0]} name:{group[1]}"
                )
            else:
                print("Document indexing failed.")
        except Exception as e:
            logger.debug(e)
            pass


if __name__ == "__main__":
    pass
