from selenium import webdriver
import simplejson as json
import urlparse

with open('config.json') as f:
    config = json.load(f)

class SeleniumTestCase(object):

    def setup(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(config['timeout'])

    def teardown(self):
        self.driver.quit()

    def get_path(self, path):
        url = urlparse.urljoin(config['endpoint'], path)
        self.driver.get(url)
