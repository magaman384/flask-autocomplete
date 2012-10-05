from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.wtf import Form
from autocomplete.forms import AutocompleteField
from autocomplete.views import autocomplete_view

def find_user_mock(query):
    if query == 'joe':
        return [{'id': 1, 'title': 'Joe Doe', 'description': 'This is Joe!'}]
    elif query == 'ali':
        return [{'id': 2, 'title': 'Mary Alice', 'description': 'And this is Alice!'}]
    else:
        return []


class WebTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True

        @app.route('/autocomplete')
        def autocomplete():
            return autocomplete_view(find_user_mock, 'row.html')

        @app.route('/form', methods=['GET', 'POST'])
        def form():
            form = UserSearch(csrf_enabled=False)
            if form.validate_on_submit():
                return 'Validated'
            return 'Not validated'

        return app


class User(object):
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


def get_user_by_id(id):
    users = {'1': User(1, 'Joe', 'Doe'), '2': User(2, 'Mary', 'Alice')}
    return users.get(id, None)

class UserSearch(Form):
    user = AutocompleteField('User',
        url='autocomplete',
        get_label='full_name',
        getter=get_user_by_id
    )