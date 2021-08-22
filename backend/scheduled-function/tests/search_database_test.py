import unittest

from database import Database
from search_database import SearchDatabase


class SearchDatabaseTestCase(unittest.TestCase):
    def test_update(self):
        database = Database('purplePolitics', 'events')
        events = database.get_events(False)
        search_database = SearchDatabase()
        search_database.update(events)


if __name__ == '__main__':
    unittest.main()
