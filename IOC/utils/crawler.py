from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import Proxy


def getData(url):
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    proxy = Proxy()
    proxy.httpProxy = "127.0.0.1:9050"
    proxy.sslProxy = "127.0.0.1:9050"
    proxy.sslProxy = "127.0.0.1:9050"
    proxy.ftpProxy = "127.0.0.1:9050"
    fireFoxOptions.set_capability("proxy", proxy)
    fireFoxOptions.proxy = proxy
    print(fireFoxOptions.proxy)
    brower = webdriver.Firefox(
        options=fireFoxOptions,
        service=Service(executable_path=GeckoDriverManager().install()),
    )
    brower.get(url)
    r = brower.page_source
    brower.quit()
    return r


if __name__ == "__main__":
    getData("https://ifconfig.me/ip")
