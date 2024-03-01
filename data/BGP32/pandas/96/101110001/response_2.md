### Analysis:
The buggy function `apply` in the `BusinessHourMixin` class is supposed to adjust the input `datetime` object based on business hours specified by `self.start` and `self.end` lists. However, the bug seems to be causing incorrect adjustments leading to failures in the test case `test_date_range_with_custom_holidays`.

### Bug Location:
The bug seems to be related to the adjustment logic within the `apply` function, where the calculations for adjusting business days and remaining business hours are not correctly handling the edge cases.

### Cause of the Bug:
1. The bug causes the adjustment of business days to work incorrectly when the `other` input is not on the offset. This leads to errors in calculating the adjusted datetime.
2. The computation of remaining business hours is not properly handling the adjustment, causing a miscalculation of the final adjusted datetime.

### Strategy for Fixing the Bug:
1. Ensure that the adjustment of business days correctly handles cases where the input datetime is not on the offset.
2. Improve the logic for adjusting remaining business hours to accurately calculate the final adjusted datetime.

### Corrected Version of the `apply` Function:
```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        n = self.n

        if n > 0 or (n == 0 and not self.is_on_offset(other)):
            other = self._next_opening_time(other)

        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )
        
        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        business_time_delta = timedelta(minutes=r)

        if bd != 0:
            skip_bd = BusinessDay(n=bd)
            if not self.is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)
            other = other + skip_bd

        while business_time_delta != timedelta(0):
            bhour = self._get_closing_time(self._prev_opening_time(other)) - other
            if business_time_delta <= bhour:
                other += business_time_delta
                business_time_delta = timedelta(0)
            else:
                business_time_delta -= bhour
                other = self._next_opening_time(other) + business_time_delta
        
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

Applying the corrections above should resolve the bug and ensure that the adjusted datetime is calculated correctly, passing the failing test case `test_date_range_with_custom_holidays`.