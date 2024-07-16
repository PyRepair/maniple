You can fix the bug by adjusting the `_next_opening_time` and `_prev_opening_time` calculations in the `apply` method. Here is the corrected version of the function:

```
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
            while n > 0:
                bhour = self._get_closing_time(other) - other
                if timedelta(minutes=n * 60) <= bhour:
                    other += timedelta(minutes=n * 60)
                    break
                else:
                    n -= (bhour.seconds // 3600) + 1
                    other = self._next_opening_time(other + bhour)
        else:
            if other.time() in self.start:
                other -= timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._prev_opening_time(other)
            while n < 0:
                bhour = other - self._prev_opening_time(other)
                if timedelta(minutes=-n * 60) >= bhour:
                    other -= timedelta(minutes=-n * 60)
                    break
                else:
                    n += (bhour.seconds // 3600) + 1
                    other = self._prev_opening_time(other - bhour)
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This fix ensures that the `apply` method correctly handles the business hour offset operations. The `_next_opening_time` and `_prev_opening_time` methods are called recursively to adjust the time until the desired number of business hours is reached.