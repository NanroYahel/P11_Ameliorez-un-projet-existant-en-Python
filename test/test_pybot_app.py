"""File containing all the unit tests for the application"""

import unittest
from unittest.mock import patch
import json

from pybot import utils
from pybot.views import app as app


class TestFlaskApp(unittest.TestCase):
    """Unit test class for """

    def setUp(self):
        app.testing = True
        self.app = app.test_client()


    def test_index_by_default_url(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_index_by_index_url(self):
        rv = self.app.get('/index')
        self.assertEqual(rv.status_code, 200)


class TestUtils(unittest.TestCase):
    """test all functions in the 'utils.py' file"""

    def test_parser(self):
        """Test the parser function"""
        test_result = utils.parser("Je suis allé au marché")
        self.assertEqual(test_result,"allé marché")

    def test_parser_for_wiki(self):
        """Test the parser for the wiki request"""
        test_result = utils.parser_for_wiki("9, rue Albert Einstien, 75000 Paris")
        self.assertEqual(test_result, "rue Albert Einstien Paris")

    def test_parser_for_name_road(self):
        """Test the parser to get only the name of a road in an address"""
        test_result = utils.parser_for_name_of_road("rue Albert Einstien")
        self.assertEqual(test_result, "Albert Einstien")


    @patch('pybot.utils.request_api')
    def test_get_data_from_google_maps(self, mock_request_api):
        """Test the Google map api request function"""
        mock_result = {"results": [{"geometry": {"location": \
            {"lat": 47.231849, "lng": -1.5584598}}, "formatted_address": "France"}]}
        mock_request_api.return_value = mock_result
        test_lat, test_long, address = utils.get_data_from_google_maps("test")
        self.assertEqual(test_lat, 47.231849)
        self.assertEqual(test_long, -1.5584598)
        self.assertEqual(address, "France")


    @patch('pybot.utils.request_api')
    def test_get_title_from_wiki(self, mock_request_api):
        """Test function to see if it select the correct title for 'Paris' keywords"""
        mock_result = ["paris",["Paris",],["Paris (prononc\u00e9 [pa.\u0281i] ) est la capitale de la France. Elle se situe au c\u0153ur d\'un vaste bassin s\u00e9dimentaire aux sols fertiles et au climat temp\u00e9r\u00e9, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l\'Oise.",],["https://fr.wikipedia.org/wiki/Paris",]]
        mock_request_api.return_value = mock_result
        test_result = utils.get_title_from_wiki('test')
        self.assertEqual(test_result, 'Paris')

    @patch('pybot.utils.get_title_from_wiki')
    @patch('pybot.utils.request_api')
    def test_get_data_from_wiki(self, mock_request_api, mock_get_title_from_wiki):
        """Test function to see if it select the correct information from an article datas"""
        mock_request_result = {"batchcomplete":"","warnings":{"extracts":{"*":"\"exlimit\" was too large for a whole article extracts request, lowered to 1."}},"query":{"normalized":[{"from":"paris","to":"Paris"}],"pages":{"681159":{"pageid":681159,"ns":0,"title":"Paris","extract":"Paris (prononc\u00e9 [pa.\u0281i] ) est la capitale de la France."}}}}
        mock_get_title_from_wiki.return_value = 'Paris'
        mock_request_api.return_value = mock_request_result
        test_result = utils.get_data_from_wiki("test")
        self.assertEqual(test_result, 'Paris (prononcé [pa.ʁi] ) est la capitale de la France.')


if __name__ == "__main__":
    unittest.main()



