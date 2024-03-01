## Analysis
1. The bug occurs in the `apply()` method of the `BusinessHourMixin` class in the `pandas/tseries/offsets.py` file.
2. The buggy function fails to handle the calculation of the correct datetime while applying a custom business hour offset with holidays.
3. The bug leads to incorrect adjustments in the datetime calculation, causing the returned datetime index to have more than the expected periods, as reported in the GitHub issue.
4. To fix the bug, adjustments in the logic of handling holidays and business hours need to be made in the `apply()` method.
5. The corrected version of the `apply()` function should accurately adjust the datetime when considering both business hours and holidays.

## Correction
Here's the corrected version of the `apply()` function with fixes to address the issue and satisfy the expected input/output values and the GitHub issue.

```python
def apply(self, other):
    if isinstance(other, datetime):
        n = self.n
        
        if n >= 0 and not self._is_on_offset(other):
            other = self._next_opening_time(other)
        elif n < 0:
            if other.time() in self.start:
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)
        
        skip_bd = BusinessDay(n=n)
        if not self.next_bday.is_on_offset(other):
            prev_open = self._prev_opening_time(other)
            remain = other - prev_open
            other = prev_open + skip_bd + remain
        else:
            other = other + skip_bd
        
        bhour_remain = timedelta(minutes=n * 60)
        
        while bhour_remain.total_seconds() != 0:
            bhour = self._get_closing_time(self._prev_opening_time(other)) - other
            if bhour_remain < bhour:
                other += bhour_remain
                bhour_remain = timedelta(0)
            else:
                bhour_remain -= bhour
                other = self._next_opening_time(other + bhour)
        
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

By replacing the buggy logic with the corrected logic above, the `apply()` method should now correctly adjust the datetime and handle holidays while applying the custom business hour offset. This correction should resolve the issue reported on GitHub and pass all the expected test cases.