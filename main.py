from IOC.IOC_crall import ioc_crawll

if __name__ == "__main__":
    OCI = ioc_crawll()
    list = OCI.search(query="card")
    print(list)
    del OCI
