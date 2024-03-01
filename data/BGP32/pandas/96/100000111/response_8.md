### Bug Explanation
The buggy function `apply` is supposed to adjust a given date and time according to business hours based on a specified offset. This function exhibits incorrect behavior when handling holiday situations, leading to unexpected output.

The bug seems to stem from how the function handles holidays within the offset calculation. Despite being specified in the holiday list, the function does not account for holidays correctly, resulting in the inclusion of extra periods in the output date range.

### Bug Fix Strategy
To fix the bug, the `apply` function needs to properly adjust for holidays to ensure that the correct number of periods is generated in the output date range. The holiday dates should be taken into consideration when calculating the business hours and adjusting the input date accordingly.

### Updated Function
Here is the corrected version of the `apply` function:

```python
from BusinessDay import BusinessDay

@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        n = self.n
        
        # Handle holidays
        if other.date() in self.holidays:
            other = self._next_opening_time(other)
        
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
        
        bhour_remain = timedelta(minutes=r)
        
        while bhour_remain != timedelta(0):
            bhour = (
                self._get_closing_time(self._prev_opening_time(other)) - other
            )
            if bhour_remain < bhour:
                other += bhour_remain
                break
            else:
                bhour_remain -= bhour
                other = self._next_opening_time(other + bhour)
        
        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This updated version of the function ensures that holidays are correctly considered when adjusting the input date and time based on business hours.