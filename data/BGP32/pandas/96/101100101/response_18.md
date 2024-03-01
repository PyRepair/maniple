### Bug Explanation:
The bug in the `apply` function is related to the incorrect calculation of `businesshours` variable, which leads to wrong adjustments made to the `other` variable. The issue arises from summing the results of `_get_business_hours_by_sec` while expecting the result in minutes instead of seconds. This causes discrepancies in the subsequent calculations and adjustment logic.

### Fix Strategy:
To fix the bug, we need to correct the calculation of `businesshours` by converting the result of `_get_business_hours_by_sec` from seconds to minutes before summing them up. Additionally, we need to ensure that all calculations involving time intervals are consistent with the expected units of time.

### Corrected Version of the `apply` function:

```python
# Import necessary modules
from pandas._libs.tslibs.offsets import ApplyTypeError
from datetime import timedelta

class BusinessHourMixin(BusinessMixin):
    @apply_wraps
    def apply(self, other):
        if isinstance(other, datetime):
            nanosecond = getattr(other, "nanosecond", 0)
            other = datetime(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            )
            n = self.n

            # Correcting calculation of businesshours by converting seconds to minutes
            businesshours = sum(
                self._get_business_hours_by_sec(st, en) // 60
                for st, en in zip(self.start, self.end)
            )

            bd, r = divmod(abs(n * 60), businesshours)
            if n < 0:
                bd, r = -bd, -r

            if bd != 0:
                skip_bd = BusinessDay(n=bd)
                if not self.next_bday.is_on_offset(other):
                    prev_open = self._prev_opening_time(other)
                    remain = other - prev_open
                    other = prev_open + skip_bd + remain
                else:
                    other = other + skip_bd

            bhour_remain = timedelta(minutes=r)

            if n >= 0:
                while bhour_remain != timedelta(0):
                    bhour = (
                        self._get_closing_time(self._prev_opening_time(other)) - other
                    )
                    if bhour_remain < bhour:
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._next_opening_time(other + bhour)
            else:
                while bhour_remain != timedelta(0):
                    bhour = self._next_opening_time(other) - other
                    if (
                        bhour_remain > bhour
                        or bhour_remain == bhour
                        and nanosecond != 0
                    ):
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._get_closing_time(
                            self._next_opening_time(
                                other + bhour - timedelta(seconds=1)
                            )
                        )

            return other
        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")
```

By incorporating the above corrections, the `apply` function should now work correctly and pass the failing test provided.