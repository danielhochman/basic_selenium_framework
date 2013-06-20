import testcases

class DuckDuckGoTestCase(testcases.SeleniumTestCase):

    def search(self, search_term):
        self.get_path('/')

        search_box = self.driver.find_element_by_name('q')
        search_box.send_keys(search_term)
        search_box.submit()

        results = self.driver.find_element_by_id('links')

        return results

class TestBasic(DuckDuckGoTestCase):

    def test_search(self):
        """
        Description: Test search functionality

        """
        # step: Search for Selenium
        results = self.search('Selenium')

        # assert: Title contains Selenium
        assert 'Selenium' in self.driver.title 
        # assert: Results contain Selenium
        assert 'Selenium' in results.text

class TestGenerator(DuckDuckGoTestCase):

    def test_search(self):
        """
        Description: Generate multiple search tests

        """
        for search_term in ['Python', 'Selenium', 'San Francisco', 'Sauce Labs']:
            yield self.verify_search, search_term

    def verify_search(self, search_term):
        results = self.search(search_term)

        assert search_term in self.driver.title
        assert search_term in results.text
