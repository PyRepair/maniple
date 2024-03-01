The issue reported on GitHub indicates that using `pd.date_range` with custom business hours and holidays can lead to unexpected behavior where more periods are generated than expected. This is likely due to a bug in the `apply` function of custom business hours within pandas.

### Bug Analysis:
1. The `apply` function doesn't handle adjustments related to holidays correctly, which leads to additional periods being generated when holidays are present.
2. The logic for adjusting `other` based on holidays is missing in the function, causing the unexpected behavior reported in the GitHub issue.

### Bug Fix Strategy:
To fix the bug, we should include logic to adjust the `other` datetime based on holidays present in the custom business hours. This adjustment should ensure that the calculation of periods aligns with the expected behavior even in the presence of holidays.

### Corrected Function:
```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        # used for detecting edge condition
        nanosecond = getattr(other, "nanosecond", 0)
        # add holiday adjustment
        if other.date() in self.holidays:
            other += timedelta(days=1)

        # reset timezone and nanosecond
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

        # adjust other to reduce number of cases to handle
        if n >= 0:
            if other.time() in self.end or not self._is_on_offset(other):
                other = self._next_opening_time(other)
        else:
            if other.time() in self.start:
                # adjustment to move to previous business day
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._next_opening_time(other)
                other = self._get_closing_time(other)

        # remaining code remains the same...

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

By including the holiday adjustment logic within the `apply` function, the corrected version should now handle periods calculation accurately even when holidays are present in the custom business hours definition.