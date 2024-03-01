### Bug Explanation
The bug in the `apply` function lies in the adjustment of the input `other` datetime when the offset `n` is negative. This is causing the function to miscalculate the time intervals and produce incorrect results.

### Bug Fix Strategy
To fix the bug:
1. Adjust the logic for handling the offset when `n` is negative to correctly move to the previous business day and handle the time intervals.
2. Ensure that the adjustments made to the `other` datetime are accurate and align with the intended functionality of the CustomBusinessHour offset.

### Corrected Version of the Function

```python
@apply_wraps
def apply(self, other):
    if isinstance(other, np.datetime64):
        n = self.n
        if n >= 0:
            if other.time() in self.end or not self._is_on_offset(other):
                other = self._next_opening_time(other)
        else:
            if other.time() in self.start:
                # adjustment to move to previous business day
                other -= np.timedelta64(1, 'D')
            if not self._is_on_offset(other):
                other = self._prev_opening_time(other)
                
        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        if bd != 0:
            skip_bd = BusinessDay(n=bd)
            other = other + skip_bd

        bhour_remain = np.timedelta64(r, 'm')

        if n >= 0:
            while bhour_remain != np.timedelta64(0, 'm'):
                bhour = self._next_opening_time(other) - other
                if bhour_remain < bhour:
                    other += bhour_remain
                    bhour_remain = np.timedelta64(0, 'm')
                else:
                    bhour_remain -= bhour
                    other = self._next_opening_time(other + bhour)
        else:
            while bhour_remain != np.timedelta64(0, 'm'):
                bhour = other - self._prev_opening_time(other)
                if bhour_remain > bhour:
                    other -= bhour_remain
                    bhour_remain = np.timedelta64(0, 'm')
                else:
                    bhour_remain -= bhour
                    other = self._prev_opening_time(other - bhour)
                    
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version of the function should now handle the offset calculation accurately and produce the expected results for the test cases provided.