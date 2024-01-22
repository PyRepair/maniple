Useful facts to help fix the bug in the `_get_time_bins` function:
- The bug is causing an `AmbiguousTimeError`.
- The call to groupby in the failing test raises the `AmbiguousTimeError`.
- The timezone in use is 'America/Havana'.
- The bug stems from the handling of ambiguous times, specifically on clock change day in Cuba, such as the ambiguous timestamp at midnight local time on 2018-11-04.


Additional fact:
- The input parameter `ax` is of type `DatetimeIndex` and contains 49 elements.