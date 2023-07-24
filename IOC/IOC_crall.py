import importlib
import os, requests
import concurrent.futures
import stem.process
from stem.control import Controller
from stem.util import term
import psycopg2


from .search import register


# Main class declaration
class ioc_crawll:
    def __init__(self, host, port, user, password) -> None:
        # importing search modules
        self.search_engines = self.load_search_modules()
        # starting tor proxy
        self.port = "9051"
        self.torProcess = self.tor_proxy()
        self.cur = self.initDatabase(host, port, user, password)

    def __del__(self):
        self.torProcess.kill()

    # table defination
    def initTabel(self, cur):
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
        # cur.execute("""""")

    # setting up the database connection and creating the neccessart table and database
    def initDatabase(self, host, port, user, password):
        print("setting up the database-----------------------------------")
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
            print("creating database")
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
            )
            cur = conn.cursor()
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
                        print("the engine is not registered yet")
                else:
                    pass

        return results

    def registerKeyword(self, keyword):
        pass

    def registerSite(self, site):
        pass

    def tor_proxy(self):
        tor_process = stem.process.launch_tor_with_config(
            config={
                "SocksPort": self.port,
                # "ExitNodes": "{US}",
            },
            init_msg_handler=self.print_bootstrap_lines,
        )
        return tor_process

    def print_bootstrap_lines(self, line):
        print(term.format(line, term.Color.BLUE))

    def simple_req(self, query):
        response = requests.get(query, proxies={"http": "socks5://localhost:9050"})
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
            print("Error: {}".format(e))
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
