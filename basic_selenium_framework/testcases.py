from selenium import webdriver
import simplejson as json
import urlparse

with open('config.json') as f:
    config = json.load(f)

class SeleniumTestCase(object):

    def setup(self):
        test_header = { 
            'module': self.__module__,
            'class': self.__class__.__name__,
            'job_id': self.driver.session_id
        }
        print "### testinfo", json.dumps(test_header, indent=2), "\n###"

        if config['use_sauce']:
            desired_capabilities = getattr(webdriver.DesiredCapabilities, config['sauce_browser'])
            desired_capabilities['name'] = '%s.%s.?' % (self.__module__, self.__class__.__name__)
            self.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (
                    config['sauce_username'], config['sauce_access_key']
                )
            )
            print 'Job URL: https://saucelabs.com/tests/%s' % self.driver.session_id
        else:
            self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(config['timeout'])


    def teardown(self):
        self.driver.quit()

    def get_path(self, path):
        url = urlparse.urljoin(config['endpoint'], path)
        self.driver.get(url)
