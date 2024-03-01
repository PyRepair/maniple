### Bug Analysis:
The bug in the `apply` function arises from incorrectly handling the `businesshours` calculation, which results in incorrect adjustments to the `other` datetime object. This bug causes the function to produce wrong output when dealing with CustomBusinessHour offsets, as demonstrated in the failing test.

### Bug Fix Strategy:
To fix the bug, we need to correct the calculation of `businesshours` and adjust the logic for handling `bhour` and `bhour_remain` to ensure proper adjustments to the `other` datetime object based on the given BusinessHour offset.

### Corrected Version of the `apply` Function:
```python
from pandas.tseries.offsets import BusinessDay

@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        # reset timezone and nanosecond
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

        businesshours = self._get_business_hours_by_sec()

        bd, r = divmod(abs(n), businesshours // 3600)
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

        bhour_remain = r * 60

        if n >= 0:
            while bhour_remain != 0:
                bhour = self._get_closing_time(self._prev_opening_time(other)) - other
                if bhour_remain < bhour.total_seconds() / 60:
                    other += timedelta(minutes=bhour_remain)
                    bhour_remain = 0
                else:
                    bhour_remain -= bhour.total_seconds() / 60
                    other = self._next_opening_time(other + bhour)
        else:
            while bhour_remain != 0:
                bhour = self._next_opening_time(other) - other
                if bhour_remain >= bhour.total_seconds() / 60:
                    other += timedelta(minutes=bhour_remain)
                    bhour_remain = 0
                else:
                    bhour_remain -= bhour.total_seconds() / 60
                    other = self._get_closing_time(self._next_opening_time(other))

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

With these changes, the corrected function should now handle the CustomBusinessHour offsets correctly and pass the failing test case provided.