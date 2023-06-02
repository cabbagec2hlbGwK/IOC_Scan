import importlib
import os
from search.register import registered_search_engine


class OCI_crawll:
    def __init__(self) -> None:
        self.search_engine = self.load_search_modules()

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
                module_path = f"search.{module_name}"

                module = importlib.import_module(module_path)
                search_modules.append(module)

        return search_modules

    def search(self, searchEngine="") -> dict():
        if not searchEngine:
            for engine in self.search_engine:
                engine.search()
        else:
            print(self.search_engine)
            for engine in self.search_engine:
                if searchEngine in engine.string():
                    engine.search()
        return dict()


if __name__ == "__main__":
    OCI = OCI_crawll()
    OCI.search("test")
