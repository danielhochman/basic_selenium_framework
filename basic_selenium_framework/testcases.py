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

        test_header = { 
            'module': self.__module__,
            'class': self.__class__.__name__,
            'job_id': self.driver.session_id
        }
        if config['use_sauce']:
            test_header['Job URL'] = "https://saucelabs.com/tests/%s" % self.driver.session_id

        print "### testinfo", json.dumps(test_header, indent=2), "\n###"

    def teardown(self):
        self.driver.quit()

    def get_path(self, path):
        url = urlparse.urljoin(config['endpoint'], path)
        self.driver.get(url)
