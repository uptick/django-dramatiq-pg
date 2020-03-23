"""
Dramatiq queue worker

Pass this to the dramatiq command line :

$ dramatiq django_dramatiq_pg.worker
"""

import django
from django.conf import settings
from django.utils.module_loading import autodiscover_modules

django.setup()  # NOQA

autodiscover_modules(getattr(settings, "DRAMATIQ_ACTORS_MODULE", "actors"))
