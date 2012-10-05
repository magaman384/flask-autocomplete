from flask import url_for
from wtforms import  StringField, ValidationError
from wtforms.widgets import TextInput

InvalidValue = -1

class AutocompleteInput(TextInput):

    def __init__(self, placeholder, url):
        self.url = url
        self.placeholder = placeholder
        super(AutocompleteInput, self).__init__()

    def __call__(self, field, **kwargs):
        css_class = kwargs.get('class', '')
        css_class = '%s %s' % (css_class, 'autocomplete')
        kwargs['class'] = css_class.strip()
        if field.data != InvalidValue and field.data is not None:
            kwargs['data-value'] = field.data.id
        kwargs['value'] = field.entity_title
        kwargs['data-autocomplete-url'] = url_for(self.url)
        kwargs['placeholder'] = self.placeholder
        kwargs['autocomplete'] = 'off'
        return super(AutocompleteInput, self).__call__(field, **kwargs)

class AutocompleteField(StringField):

    def __init__(self, label=u'', validators=None, get_label=unicode, placeholder='Start typing and select...', url='', getter=None, *args, **kwargs):
        # override widget
        if not kwargs.has_key('widget'):
            kwargs['widget'] = AutocompleteInput(placeholder, url)

        self.getter = getter
        self.entity_title = ''

        # construct label getter
        if isinstance(get_label, basestring):
            _get_label = get_label
            get_label = lambda a:_getattr(a, _get_label)
        self.get_label = get_label

        super(AutocompleteField, self).__init__(label, validators, *args, **kwargs)


    def process_data(self, value):
        super(AutocompleteField, self).process_data(value)
        if self.data is not None and self.data is not InvalidValue:
            self.entity_title = self.get_label(self.data)

    def process_formdata(self, valuelist):
        super(AutocompleteField, self).process_formdata(valuelist)
        self.entity_title = self.data
        if self.data == '':
            self.data = None
        elif self.data.isdigit():
            entity = self.getter(self.data)
            if entity is None:
                self.entity_title = self.data
                self.data = InvalidValue
            else:
                self.data = entity
                self.entity_title = self.get_label(entity)
        else:
            self.data = InvalidValue

    def validate(self, form, extra_validators=tuple()):
        if isinstance(extra_validators, tuple):
            validators = extra_validators + (_validate_autocompleted, )
        else:
            validators = extra_validators + [_validate_autocompleted]
        return super(AutocompleteField, self).validate(form, validators)


def _validate_autocompleted(form, field):
    if field.data == InvalidValue:
        raise ValidationError('Invalid value')

def _getattr(obj, attribute):
    if obj is not None:
        return getattr(obj, attribute)