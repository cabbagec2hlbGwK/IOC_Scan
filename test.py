from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType


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
    print("initing Browser")
    try:
        browser = webdriver.Firefox(
            options=fireFoxOptions,
            service=Service(executable_path=GeckoDriverManager().install()),
        )
    except:
        pass
    print("browser is running")
    return browser
