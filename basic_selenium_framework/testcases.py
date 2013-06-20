from selenium import webdriver
import simplejson as json
import urlparse

with open('config.json') as f:
    config = json.load(f)

class SeleniumTestCase(object):

    def setup(self):
        if config['use_sauce']:
            desired_capabilities = getattr(webdriver.DesiredCapabilities, config['sauce_browser'])
            self.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (
                    config['sauce_username'], config['sauce_access_key']
                )
            )
        else:
            self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(config['timeout'])

    def teardown(self):
        self.driver.quit()

    def get_path(self, path):
        url = urlparse.urljoin(config['endpoint'], path)
        self.driver.get(url)
