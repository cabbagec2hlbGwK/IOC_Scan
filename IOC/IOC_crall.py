import importlib
import os
import concurrent.futures

from .search import register


class ioc_crawll:
    def __init__(self) -> None:
        self.search_engines = self.load_search_modules()

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

    def search_all(self) -> list():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for engine in self.search_engines:
                future = executor.submit(self.search, engine.__name__.split(".")[-1])
                futures.append(future)
                results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
            print(results)
            return results

    def search(self, searchEngine=""):
        # print(not searchEngine)
        results = []
        if not searchEngine:
            results.append(self.search_all())
        else:
            for engine in self.search_engines:
                # print(f"{engine.string()} {searchEngine}")
                if engine.string() == searchEngine:
                    if "test" in register.registered_search_engine:
                        results.append(engine.search())
                    else:
                        print("the engine is not registered yet")
                else:
                    pass
            return results
