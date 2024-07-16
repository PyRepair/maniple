Here is a corrected version of the `apply` function:
```python
def apply(self, other):
    if isinstance(other, datetime):
        # used for detecting edge condition
        nanosecond = getattr(other, "nanosecond", 0)
        # reset timezone and nanosecond
        # other may be a Timestamp, thus not use replace
        other = datetime(
            other.year,
            other.month,
            other.day,
            other.hour,
            other.minute,
            other.second,
            other.microsecond,
        )

        if self.n >= 0:
            if other.time() in self.end or not self._is_on_offset(other):
                other = self._next_opening_time(other)
        else:
            if other.time() in self.start:
                # adjustment to move to previous business day
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)

        # get total business hours by sec in one business day
        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        bd, r = divmod(abs(self.n * 60), businesshours // 60)
        if self.n < 0:
            bd, r = -bd, -r

        if bd!= 0:
            skip_bd = self._next_opening_time(other)
            while bd > 0:
                bhour = self._get_business_hours_by_sec(
                    other.time(), self._get_closing_time(other)
                )
                if bhour <= timedelta(minutes=r):
                    other = self._get_closing_time(other)
                else:
                    other = skip_bd - timedelta(minutes=bhour.seconds // 60)
                    bd -= 1
                    skip_bd = other
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```
The corrected function takes into account the custom business hours and holidays correctly. It also handles the case where the input `other` is a `datetime` object with a custom business hour frequency.