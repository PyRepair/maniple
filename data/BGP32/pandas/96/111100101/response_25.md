### Bug Analysis:
The bug in the `apply` function lies in the calculation of the adjustment for business hours. The function fails to handle negative values of `n` correctly, leading to incorrect adjustments.

### Bug Cause:
1. When `n` is negative, the function incorrectly adjusts the `other` datetime by moving to the previous business day, but then fails to apply the correct adjustments for the remaining business hours.
2. The logic for adjusting the remaining business hours in negative `n` scenarios is flawed, leading to incorrect results.

### Bug Fix Strategy:
1. Adjust the logic for negative `n` values to correctly calculate adjustments for the remaining business hours.
2. Update the code to handle negative `n` values more effectively and accurately.

### Corrected Function:
Here is the corrected version of the `apply` function:

```python
    @apply_wraps
    def apply(self, other):
        if isinstance(other, datetime):
            # used for detecting edge condition
            nanosecond = getattr(other, "nanosecond", 0)
            
            # adjust other to reduce number of cases to handle
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
    
            # adjust other based on the offset conditions
            if n >= 0:
                if other.time() in self.end or not self._is_on_offset(other):
                    other = self._next_opening_time(other)
            else:
                if other.time() in self.start:
                    other = other - timedelta(seconds=1)
                if not self._is_on_offset(other):
                    other = self._next_opening_time(other)
                    other = self._get_closing_time(other)
            
            # get total business hours by sec in one business day
            businesshours = sum(
                self._get_business_hours_by_sec(st, en)
                for st, en in zip(self.start, self.end)
            )
    
            bd, r = divmod(abs(n * 60), businesshours // 60)
    
            if n < 0:
                # For negative n, adjust by business days first
                if bd != 0:
                    skip_bd = BusinessDay(n=bd)
                    prev_open = self._prev_opening_time(other)
                    remain = other - prev_open
                    other = prev_open + skip_bd + remain
                
                # Handle remaining business hours to adjust
                bhour_remain = timedelta(minutes=r)
                while bhour_remain != timedelta(0):
                    bhour = self._next_opening_time(other) - other
                    if bhour_remain <= bhour or (bhour_remain == bhour and nanosecond != 0):
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._get_closing_time(self._next_opening_time(other + bhour - timedelta(seconds=1)))
            else:
                # For positive n, adjust by business days first
                if bd != 0:
                    skip_bd = BusinessDay(n=bd)
                    other = other + skip_bd
                
                # Handle remaining business hours to adjust
                bhour_remain = timedelta(minutes=r)
                while bhour_remain != timedelta(0):
                    bhour = self._get_closing_time(self._prev_opening_time(other)) - other
                    if bhour_remain <= bhour:
                        other += bhour_remain
                        bhour_remain = timedelta(0)
                    else:
                        bhour_remain -= bhour
                        other = self._next_opening_time(other + bhour)
    
            return other
        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")

```

By applying the suggested fixes, the corrected version should now handle negative values of `n` correctly and produce the expected output for all test cases.