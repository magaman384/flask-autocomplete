from flask import url_for
from tests.test import WebTestCase

class AutocompleteFormTest(WebTestCase):

    def test_form(self):
        response = self.client.get(url_for('form'))
        self.assert200(response)
        self.assertEqual('Not validated', response.data)

        response = self.client.post(url_for('form'), data={'user': '0'})
        self.assert200(response)
        self.assertEqual('Not validated', response.data)

        response = self.client.post(url_for('form'), data={'user': ''})
        self.assert200(response)
        self.assertEqual('Validated', response.data)

        response = self.client.post(url_for('form'), data={'user': '1'})
        self.assert200(response)
        self.assertEqual('Validated', response.data)

        response = self.client.post(url_for('form'), data={'user': '2'})
        self.assert200(response)
        self.assertEqual('Validated', response.data)
