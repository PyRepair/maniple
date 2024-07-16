The bug lies in the `apply` method of the `BusinessHourMixin` class, specifically in how it handles the adjustment of the `other` datetime object when the number of business hours `n` is negative.

The issue arises when `n` is negative, and `other` is on a business day but not within business hours. In this case, the code tries to adjust `other` to the previous business day's closing time, but it doesn't correctly handle the case where `other` is exactly on the previous business day's closing time.

To fix the bug, we need to modify the `apply` method to correctly handle this edge case. Here's the corrected version:
```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        #... (rest of the code remains the same until the adjustment logic)

        if n < 0:
            if other.time() in self.start:
                # adjustment to move to previous business day
                other = other - timedelta(seconds=1)
            if not self._is_on_offset(other):
                other = self._prev_opening_time(other)
                if other == self._get_closing_time(other):
                    # Edge case: other is exactly on the previous business day's closing time
                    other = self._prev_opening_time(other) - timedelta(minutes=1)
                else:
                    other = self._get_closing_time(other)

        #... (rest of the code remains the same)
```
The key change is the addition of the `if other == self._get_closing_time(other)` check, which handles the edge case where `other` is exactly on the previous business day's closing time. In this case, we adjust `other` to be one minute before the closing time, ensuring that we correctly move to the previous business day.

With this fix, the `date_range` function should now work correctly even when adding holidays.