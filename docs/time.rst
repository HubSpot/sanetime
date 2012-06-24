.. _time:

construction
============

conversion
==========

display
=======



The time class represents a moment in time, internally stored as microseconds since epoch.
A time object also has an associated timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks. 
A moment in time experienced in America/New_York is equal to the same moment in time experienced in Europe/Dublin.

API
===

.. module:: sanetime

.. autoclass:: time
   :inherited-members:

