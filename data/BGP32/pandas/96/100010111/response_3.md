### Bug analysis
- The `apply` function is intended to handle business hours with datetime objects but it fails to correctly adjust the datetime based on business hours.
- The error message indicates a `ValueError` is raised during the execution of the test, specifically when validating the frequency.
- The function seems to be calculating business days and hours adjustments incorrectly.

### Bug location
- The bug might be located in the adjustment of business days and hours within the `apply` function.
- Specifically, the logic for adjusting timedelta based on business hours seems to be causing the incorrect calculations.

### Bug explanation
- The bug causes the function to incorrectly calculate the adjusted datetime when dealing with business hours and holidays.
- The incorrect adjustment results in more periods being generated than expected, leading to the failing test and the `ValueError`.

### Bug fix strategy
To fix the bug:
1. Adjust the logic for calculating business days and hours based on the provided business hours and holidays.
2. Ensure that the adjustment logic correctly handles the case when holidays are involved.

### Corrected function
Here is the corrected version of the `apply` function:

```python
@apply_wraps
def apply(self, other):
    
    if isinstance(other, datetime):
        n = self.n
        nanosecond = getattr(other, "nanosecond", 0)

        __next_opening_time=lambda x: x.replace(minute=0, second=0, microsecond=0)+timedelta(hours=1) if x.minute>0 else x

        if n >= 0: # For positive n
            if other.time() in self.end or not self._is_on_offset(other):
                other = __next_opening_time(other)
        else: # For negative n
            if other.time() in self.start: 
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)
        
        businesshours = sum(self._get_business_hours_by_sec(st, en) for st, en in zip(self.start, self.end))

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r
        
        if bd != 0: # Adjust by business days
            skip_bd = BusinessDay(n=bd)
            if not self.next_bday.is_on_offset(other):
                prev_open = self._prev_opening_time(other)
                remain = other - prev_open
                other = prev_open + skip_bd + remain
            else:
                other = other + skip_bd

        bhour_remain = timedelta(minutes=r) # Remaining business hours
        
        if n >= 0: # For positive n
            while bhour_remain.total_seconds() != 0:
                bhour = self._get_closing_time(self._prev_opening_time(other)) - other
                if bhour_remain < bhour:
                    other += bhour_remain
                    bhour_remain = timedelta(0)
                else:
                    bhour_remain -= bhour
                    other = __next_opening_time(other + bhour)
        else: # For negative n
            while bhour_remain.total_seconds() != 0:
                bhour = self._next_opening_time(other) - other
                if bhour_remain >= bhour or (bhour_remain == bhour and nanosecond != 0):
                    other += bhour_remain
                    bhour_remain = timedelta(0)
                else:
                    bhour_remain -= bhour
                    other = self._get_closing_time(self._next_opening_time(other + bhour - timedelta(seconds=1)))

        return other
    
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version should address the bug and pass the failing test case while considering the expected input/output values and the related GitHub issue.