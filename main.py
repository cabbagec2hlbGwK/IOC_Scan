from IOC.IOC_crall import ioc_crawll

if __name__ == "__main__":
    OCI = ioc_crawll()
    OCI.search(query="card", searchEngine="ahmia")
    print(OCI.get_relay_count())
