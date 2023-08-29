import importlib
import os, requests, sys
import concurrent.futures
import psycopg2
import stem.process
from loguru import logger
from stem.control import Controller
from stem.util import term
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from .search import register
from elasticsearch import Elasticsearch, AuthenticationException

# Setting the loging
logger.add(sys.stdout)


# Main class declaration
class ioc_crawll:
    def __init__(
        self,
        host,
        port,
        user,
        password,
        elasticSearchHost,
        elasticSearchPass,
        elasticSearchUser,
    ) -> None:
        self.port = "9051"
        self.elasticSearchHost = elasticSearchHost
        self.elasticSearchUser = elasticSearchUser
        self.elasticSearchPass = elasticSearchPass

        # importing search modules and setting up the objects
        self.search_engines = self.load_search_modules()
        self.torProcess = self.tor_proxy()
        self.browser = self.initBrowser()
        self.cur = self.initDatabase(host, port, user, password)
        self.es = self.initElasticSearch()

    def __del__(self):
        self.conn.close()
        self.browser.quit()
        self.es.close()

    # table defination
    def initTabel(self, cur) -> None:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS website(
                    id SERIAL PRIMARY KEY,
                    url VARCHAR(255) NOT NULL,
                    dir VARCHAR(255) DEFAULT 'NULL',
                    status varchar(10) DEFAULT 'ACTIVE')"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS keywords(
                    id SERIAL PRIMARY KEY,
                    word TEXT,
                    status varchar(10) DEFAULT 'ACTIVE')"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS ransomware_groups (
            id SERIAL PRIMARY KEY,
            name varchar(20),
            link varchar,
            status varchar(10) DEFAULT 'ACTIVE',
            CONSTRAINT unique_group_links UNIQUE (name, link)
        );
"""
        )

    # setting up the database connection and creating the neccessart table and database
    def initDatabase(self, host, port, user, password):
        logger.info("setting up the database-----------------------------------")
        self.DATABASE = "ioc"

        try:
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=self.DATABASE,
            )
            cur = self.conn.cursor()
            self.conn.autocommit = True
            self.initTabel(cur)
            return cur
        except psycopg2.OperationalError:
            # Handeling if the database is not created
            logger.error("database not found")
            logger.info("creating database")
            try:
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                )
                cur = conn.cursor()
            except Exception as e:
                logger.critical(f"Can't connect with the database: {e}")
                del self
                os._exit(1)

            conn.autocommit = True
            cur.execute(f"CREATE DATABASE {self.DATABASE}")
            cur.close()
            conn.close()
            cur = self.initDatabase(
                host=host,
                port=port,
                user=user,
                password=password,
            )
        return cur

    def initElasticSearch(self):
        es = Elasticsearch(
            [f"https://{self.elasticSearchHost}:9200"],
            verify_certs=False,
            # basic_auth=(self.elasticSearchpass, self.elasticSearchuser),
            http_auth=(self.elasticSearchUser, self.elasticSearchPass),
        )
        index_name = "ransom_groups_data1"
        index_body = {
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            "mappings": {
                "properties": {
                    "URL": {"type": "text"},
                    "contents": {"type": "text"},
                    "date": {"type": "date"},
                }
            },
        }
        try:
            response = es.indices.create(index=index_name, body=index_body)
            logger.success("Index is created")
        except AuthenticationException as e:
            logger.critical(
                f"The user name or the password is wrong for elasticSearch {e}"
            )
        except Exception as e:
            logger.critical(f"something is wrong with the elastic cluster {e}")
        logger.info("ELASTIC cluster is connected")
        return es

    def load_search_modules(self):
        search_modules = []
        search_dir = os.path.join(os.path.dirname(__file__), "search")

        for file_name in os.listdir(search_dir):
            if (
                file_name.endswith(".py")
                and file_name != "__init__.py"
                and file_name != "register.py"
            ):
                module_name = file_name[:-3]  # Remove the '.py' extension
                module_path = f"IOC.search.{module_name}"

                module = importlib.import_module(module_path)
                search_modules.append(module)

        return search_modules

    def search_all(self, query):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for engine in self.search_engines:
                future = executor.submit(
                    self.search, query, engine.__name__.split(".")[-1]
                )
                futures.append(future)
                results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
            return results

    def search(self, query, searchEngine=""):
        results = []
        if not searchEngine:
            results = self.search_all(query)
            # results.append(self.search_all(query))
        else:
            for engine in self.search_engines:
                if engine.string() == searchEngine:
                    if searchEngine in register.registered_search_engine:
                        results.append(engine.search(IOC=self, query=query))
                    else:
                        logger.debug(f"the engine {searchEngine} is not registered yet")
                else:
                    pass

        return results

    def tor_proxy(self):
        try:
            tor_process = stem.process.launch_tor_with_config(
                config={
                    "SocksPort": self.port,
                    # "ExitNodes": "{US}",
                },
                init_msg_handler=self.print_bootstrap_lines,
            )
        except OSError:
            tor_process = None
            logger.error("tor is alredy running")
        return tor_process

    def print_bootstrap_lines(self, line) -> None:
        # print(term.format(line, term.Color.BLUE))
        logger.info(line)

    def simple_req(self, query):
        response = requests.get(
            query, proxies={"http": f"socks5://localhost:{self.port}"}
        )
        return query

    def get_relay_count(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                circuit_id = controller.get_circuits()[0]  # Get the first circuit ID
                circuit = controller.get_circuit(circuit_id)
                relay_count = len(circuit.path)
                return relay_count
        except Exception as e:
            logger.error(f"{e}")
            return None

    def tor_req(self):
        proxy_ip = "127.0.0.1"  # Tor proxy IP address
        proxy_port = self.port  # Tor proxy port

        # Create a session and set the proxy
        session = requests.session()
        session.proxies.update(
            {
                "http": f"socks5h://{proxy_ip}:{proxy_port}",
                "https": f"socks5h://{proxy_ip}:{proxy_port}",
            }
        )
        return session

    # setting up the headless browser
    def initBrowser(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        fireFoxOptions.set_preference("network.dns.blockDotOnion", False)
        fireFoxOptions.set_preference("network.http.sendRefererHeader", 0)
        fireFoxOptions.set_preference("places.history.enabled", False)
        fireFoxOptions.set_preference("privacy.clearOnShutdown.offlineApps", True)
        fireFoxOptions.set_preference("network.cookie.lifetimePolicy", 2)
        fireFoxOptions.set_preference("network.dns.disablePrefetch", True)
        fireFoxOptions.set_preference("network.proxy.socks_remote_dns", True)
        proxy = Proxy()
        proxy.proxyType = ProxyType.MANUAL
        proxy.socksProxy = f"127.0.0.1:{self.port}"
        proxy.socks_version = 5
        proxy.no_proxy = ["localhost", "172.0.0.1"]
        fireFoxOptions.proxy = proxy
        logger.info("initing Browser")
        browser = None
        try:
            browser = webdriver.Firefox(
                options=fireFoxOptions,
                service=Service(executable_path=GeckoDriverManager().install()),
            )
        except Exception as e:
            logger.critical(f"failed to start the browser : {e}")
            del self
            sys.exit(1)
        logger.success("browser is running")
        return browser
