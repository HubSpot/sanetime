from sanetime import sanetime,SaneTime
try:
    from django.db import models
    from django import forms
except ImportError:
    raise RuntimeError('Django is required for sanetime.dj.')

class SaneTimeFormField(forms.DateTimeField):
    pass

class SaneTimeField(models.BigIntegerField):

    description = "A field to hold sanetimes (i.e. microseconds since epoch)."

    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        if auto_now or auto_now_add:
            kwargs['editable'] = False
            kwargs['blank'] = True
        super(SaneTimeField, self).__init__(verbose_name, name, **kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = sanetime()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(SaneTimeField, self).pre_save(model_instance, add)

    def to_python(self, value):
        if value is not None:
            if not isinstance(value, SaneTime):
                value = sanetime(value)
            return value
        return super(SaneTimeField,self).to_python(value)

    def get_prep_value(self, value):
        if value is not None:
            return int(value)
        return super(SaneTimeField,self).get_prep_value(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^sanetime\.dj\.SaneTimeField"])
    

