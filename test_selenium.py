from selenium import webdriver
import simplejson as json
import urlparse

_multiprocess_shared_ = True

def setup():
    global config
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

class TestBasic(SeleniumTestCase):

    def test_search(self):
        self.get_path('/')

        search_box = self.driver.find_element_by_name('q')
        search_box.send_keys('Selenium')
        search_box.submit()

        results = self.driver.find_element_by_id('links')

        assert 'Selenium' in self.driver.title 
        assert 'Selenium' in results.text

class TestGenerator(SeleniumTestCase):

    def test_search(self):
        for search_term in ['Python', 'Selenium', 'San Francisco', 'Sauce Labs']:
            yield self.verify_search, search_term

    def verify_search(self, search_term):
        self.get_path('/')

        search_box = self.driver.find_element_by_name('q')
        search_box.send_keys(search_term)
        search_box.submit()

        results = self.driver.find_element_by_id('links')

        assert search_term in self.driver.title 
        assert search_term in results.text
