### Bug Explanation:
The buggy function `apply` is designed to adjust a given `datetime` object based on the business hour offsets specified in the `CustomBusinessHour` class. However, it fails to handle the specific case where the adjustment results in moving to the next business day correctly. This is evident from the failing test `test_date_range_with_custom_holidays`.

### Bug Location:
The bug primarily lies in the logic for adjusting the business days and remaining business hours within the `apply` function. When the adjustment requires moving to the next business day, the function does not handle it appropriately.

### Bug Fix Strategy:
To fix the bug, a proper handling mechanism needs to be implemented for cases where the adjustment moves to the next business day. This can be achieved by ensuring that the date is correctly adjusted to the next business day if needed and then adjusting the remaining business hours accordingly.

### Corrected Version of the Function:
Here is the corrected version of the `apply` function:

```python
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

        if n >= 0:
            if other.time() in self.end or not self._is_on_offset(other):
                other = self._next_opening_time(other)
        else:
            if other.time() in self.start:
                other -= timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)

        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        skip_bd = BusinessDay(n=bd)

        if bd != 0:
            if not self.next_bday.is_on_offset(other):
                other = other.replace(hour=0, minute=0, second=0, microsecond=0)
                other = other + skip_bd.shift(1) + timedelta(hours=other.hour, minutes=other.minute, seconds=other.second, microseconds=other.microsecond)
            else:
                other += skip_bd

        bhour_remain = timedelta(minutes=r)

        while bhour_remain.total_seconds() != 0:
            if n >= 0:
                bhour = self._get_closing_time(self._prev_opening_time(other)) - other
            else:
                bhour = self._next_opening_time(other) - other

            if bhour_remain >= bhour or (bhour_remain == bhour and nanosecond != 0):
                other += bhour
                bhour_remain -= bhour
            else:
                other += bhour_remain
                bhour_remain = timedelta(0)

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version of the function should now handle the case of moving to the next business day correctly and pass the failing test provided.