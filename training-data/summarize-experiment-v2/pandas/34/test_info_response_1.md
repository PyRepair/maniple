Fault location:
  File "pandas/core/resample.py", line 1425, in _get_time_bins
  binner = labels = date_range(
  
Original error message:
  raise pytz.AmbiguousTimeError(
  pytz.exceptions.AmbiguousTimeError: Cannot infer dst time from 2018-11-04 00:00:00 as there are no repeated times

Simplified error message:
  AmbiguousTimeError: Cannot infer dst time from 2018-11-04 00:00:00, no repeated times.