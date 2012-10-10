flask-autocomplete
==================


Installation
------------

```
$ pip install git+git://github.com/magaman384/flask-autocomplete.git
```

Usage
-----

In form:
```python
from flask.ext.wtf import Form
from autocomplete.forms import AutocompleteField

class User(object):

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


def get_user_by_id(id):
    users = {1: User(1, 'Joe', 'Doe'), 2: User(2, 'Mary', 'Alice')}
    return users.get(id, None)

class UserSearch(Form):
    user = AutocompleteField('User',
        url='users.autocomplete',
        get_label='full_name',
        getter=get_user_by_id
    )
```

In views:
```python
from autocomplete.views import autocomplete_view

def find_user(query):
    # put your database magic here to fetch items
    return [{'id': 1, 'title': 'Joe Doe', 'data': []}]

@app.route('/users/autocomplete')
def autocomplete():
    return autocomplete_view(find_user, 'templates/render-user.html')
```

In `templates/render-user.html`:
```html
<div class="big">{{ title }}</div>
```

Don't forget to include JavaScripts in your base template:

-    static/jquery.js
-    static/jquery-autocomplete.js
-    static/load.js