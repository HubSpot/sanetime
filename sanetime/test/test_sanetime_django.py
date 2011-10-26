import unittest2
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sanetime.test.test_sqlite'
from django.conf import settings
filename = os.path.join(os.path.dirname(__file__), 'test.db')
settings.DATABASES['default']['NAME'] = filename
from django.db.models.loading import get_apps
get_apps()



from sanetime import sanetime
from sanetime import sanetime_django
from django.db import models


class SaneTimeModel(models.Model):
    time = sanetime_django.SaneTimeField()

class SaneTimeDjangoTest(unittest2.TestCase):
    def setup(self):
        pass

    def test_sanetime_field(self):
        st = sanetime()
        o = SaneTimeModel.objects.create(time=st)
        o = SaneTimeModel.objects.get()
        self.assertEqual(st.us, o.time.us)


