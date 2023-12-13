import re, datetime, sys, json
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



def update(IOC):
    session = IOC.tor_req()
    data = json.loads(session.get(
            "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/groups.json"
    ).text)

    for group in data:
        name = group["name"]
        [insert(IOC=IOC, group = name,link=location["fqdn"]) for location in group["locations"]]
        print(f"{name} DONE")


def list(IOC):
    IOC.cur.execute("SELECT * FROM ransomware_groups")
    return IOC.cur.fetchall()



def index_group(IOC,link):
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
            logger.success(f"{link} indexed successfully.")
        else:
            logger.warning("{link} indexing failed.")
        return True
    except Exception as e:
        logger.info(e)
        return False

def index_ing(IOC):
    groups = list(IOC=IOC)
    done = True
    for group in groups:
        link = group[2]
        if link == "7k4yyskpz3rxq5nyokf6ztbpywzbjtdfanweup3skctcxopmt7tq7eid.onion":
            done = False
        if done:
            continue
        print(link)
        if not index_group(IOC, link=f"https://{link}") :
            _ = index_group(IOC,link=f"http://{link}")


if __name__ == "__main__":
    pass
