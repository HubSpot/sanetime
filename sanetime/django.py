from django.db import models
from django import forms
from sanetime import sanetime

class SaneTimeFormField(forms.DateTimeField):
    pass

class SaneTimeField(models.BigInteger):

    description = "A field to hold the micros part of a sanetime.  The timezone is forced to be UTC."

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(SaneTimeField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, sanetime):
            value = sanetime(value)
        return value.with_tz('UTC')

    def get_prep_value(self, value):
        return value.us

    def formfield(self, **kwargs):
        defaults = {'form_class': SaneTimeFormField}
        defaults.update(kwargs)
        return super(SaneTimeFormField, self).formfield(**defaults)



