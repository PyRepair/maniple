Based on the provided GitHub issue and test cases, I will attempt to fix the bug. The bug in the function `apply` in the `CustomBusinessHour` class is due to incorrect logic in handling the rollover of the business day after the end of the day.

Here's a corrected version of the `apply` method:

```python
class BusinessHourMixin(BusinessMixin):
    #... (other methods)

    @apply_wraps
    def apply(self, other):
        other = datetime(other.year, other.month, other.day, other.hour, other.minute, other.second, other.microsecond)

        if self.n >= 0:
            if other.time() in self.end or not self.is_on_offset(other):
                other = self._next_opening_time(other)
            if not self.is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)
        else:
            if other.time() in self.start:
                other = other - timedelta(seconds=1)
            if not self.is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)

        businesshours = sum(self._get_business_hours_by_sec(st, en) for st, en in zip(self.start, self.end))
        bd, r = divmod(self.n * 60, businesshours // 60)
        if self.n < 0:
            bd, r = -bd, -r

        if bd!= 0:
            skip_bd = BusinessDay(n=bd)
            if not self.next_bday.is_on_offset(other):
                prev_open = self._prev_opening_time(other)
                remain = other - prev_open
                other = prev_open + skip_bd + remain
            else:
                other = other + skip_bd

        bhour_remain = timedelta(minutes=r)

        while bhour_remain!= timedelta(0):
            bhour = self._get_closing_time(self._prev_opening_time(other)) - other
            if bhour_remain < bhour:
                other = other + bhour_remain
                bhour_remain = timedelta(0)
            else:
                bhour_remain -= bhour
                other = self._next_opening_time(other + bhour)

        return other
```

This corrected version should handle the rollover of the business day correctly and produce the expected results. The test cases provided should pass with this correction.