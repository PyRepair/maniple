### Bug Explanation:
The bug in the `apply` function occurs when adjusting the offset by business days. The logic for handling the adjustment of business days is incorrect, leading to incorrect output. This bug is triggered when the offset `self.n` is set to a positive value, causing a faulty adjustment in the calculation.

### Bug Fix Strategy:
To fix the bug, we need to correct the code related to adjusting by business days when `self.n` is greater than or equal to 0. It seems that the code incorrectly handles the adjustment when `self.n` is positive. We need to adjust the logic for adding business days when `self.n` is positive to ensure the correct outcome.

### Corrected Function:
Here is the corrected version of the `apply` function:
```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        # used for detecting edge condition
        nanosecond = getattr(other, "nanosecond", 0)
        # Reset timezone and nanosecond
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
            # Adjust by business days first
            if n > 0:
                other += BusinessDay(n=n)
                other = self._next_opening_time(other)
        
        # Remaining business hours to adjust
        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )
        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        if bd != 0:
            if bd > 0:
                other += BusinessDay(n=bd)
                other = self._next_opening_time(other)
        
        bd_remain = timedelta(minutes=r)

        # Adjust remaining business hours
        if bd == 0:
            business_hour = self._get_business_hour(other)
            if n >= 0:
                other += min(bd_remain, business_hour)
            else:
                other -= min(bd_remain, business_hour)

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

By making these adjustments to the code, the `apply` function should now produce the correct output and pass the failing test cases.