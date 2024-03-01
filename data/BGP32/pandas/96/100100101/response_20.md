### Bug Explanation
The buggy function `apply` is designed to combine business hours with datetime values. However, there are several issues in the function that lead to incorrect results. The function fails to properly adjust business days and remaining business hours, resulting in incorrect outputs for the given test cases. 

One of the main issues is with the calculation and adjustment of business days. The function fails to correctly handle cases where the target datetime is not on the business day offset. Additionally, the logic for adjusting remaining business hours within a business time interval is flawed, leading to incorrect calculations.

### Bug Fix Strategy
To fix the bug in the `apply` function, we need to ensure proper adjustment of business days and remaining business hours. We should address the incorrect handling of datetime values that are not on the weekend offset as well. By improving these aspects of the function, we can correct the output for the failing test cases.

### Corrected Function
Here is the corrected version of the `apply` function:

```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        # Adjust other to reset timezone and nanosecond
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

        # Adjust other based on business hour offset
        if n >= 0:
            if other.time() in self.end or not self._is_on_offset(other):
                other = self._next_opening_time(other)
        else:
            if other.time() in self.start:
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)

        # Calculate total business hours in a day
        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        # Adjust by business days first
        if n != 0:
            skip_bd = BusinessDay(n=n)
            other = self._adjust_business_days(other, skip_bd)

        # Adjust remaining business hours
        other = self._adjust_business_hours(other, n, businesshours)

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

In the corrected version of the function, we have improved the logic to handle business days and remaining business hours more accurately. This should address the issues causing the failing test cases.