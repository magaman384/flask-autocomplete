import json
from flask import url_for
from tests.test import WebTestCase

class AutocompleteViewTest(WebTestCase):

    def test_view_do_nothing(self):
        response = self.client.get(url_for('autocomplete'))
        self.assert400(response)
        response = self.client.get(url_for('autocomplete', query='nothing'))
        self.assert200(response)
        self.assertEqual([], json.loads(response.data))

    def test_view_formatting(self):
        response = self.client.get(url_for('autocomplete', query='joe'))
        self.assert200(response)
        expected = [{
            'id': 1,
            'title': 'Joe Doe',
            'html': '<div class="big">Joe Doe</div>\n<div class="small">This is Joe!</div>'
        }]
        self.assertEqual(expected, json.loads(response.data))
        response = self.client.get(url_for('autocomplete', query='ali'))
        self.assert200(response)
        expected = [{
            'id': 2,
            'title': 'Mary Alice',
            'html': '<div class="big">Mary Alice</div>\n<div class="small">And this is Alice!</div>'
        }]
        self.assertEqual(expected, json.loads(response.data))
