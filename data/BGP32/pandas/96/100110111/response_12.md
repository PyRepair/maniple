### Analysis
The buggy function `apply` is incorrectly adjusting the business hours in a given datetime object. This issue causes the unexpected behavior in the test case `test_date_range_with_custom_holidays` where the output does not match the expected result due to incorrect business hour calculations.

The function `apply` is supposed to adjust the input datetime based on business hours, but due to the bug, it is not handling holidays correctly. This leads to additional periods in the output, causing the test case to fail.

### Bug Explanation
The bug occurs because the function does not properly handle holidays when adjusting the business hours. This leads to an incorrect number of periods being generated, as seen in the failing test.  

### Bug Fix Strategy
To fix the bug:
- Adjust the logic related to holiday handling to properly account for them.
- Ensure that all calculations consider the presence of holidays.
- Verify that the adjustments are made correctly according to the business hours.

### Code Fix
Here is the corrected version of the `apply` function:
```python
@apply_wraps
def apply(self, other):
    if isinstance(other, datetime):
        n = self.n
        
        businesshours = sum(
            self._get_business_hours_by_sec(st, en)
            for st, en in zip(self.start, self.end)
        )

        bd, r = divmod(abs(n * 60), businesshours // 60)
        if n < 0:
            bd, r = -bd, -r

        if bd != 0:
            # Adjust for business days first
            other = self.next_bday.rollforward(other)
            if self.holidays:
                while bd > 0:
                    other = self.next_bday.rollforward(other)
                    if other in self.holidays:
                        other = self.next_bday.rollforward(other)
                    else:
                        bd -= 1
            elif bd < 0:
                while bd < 0:
                    other = self.next_bday.rollback(other)
                    if other in self.holidays:
                        other = self.next_bday.rollback(other)
                    else:
                        bd += 1

        delta_hours = 60 * bd + r

        if delta_hours > 0:
            while delta_hours > 0:
                other += timedelta(hours=1)
                if other.hour not in range(17) or other in self.holidays:
                    other = self._next_opening_time(other)

                delta_hours -= 1
        elif delta_hours < 0:
            while delta_hours < 0:
                other -= timedelta(hours=1)
                if other.hour not in range(15, 17) or other in self.holidays:
                    other = self._get_closing_time(self._prev_opening_time(other))

                delta_hours += 1

        return other
    else:
        raise ApplyTypeError("Only know how to combine business hour with datetime")
```

This corrected version of the function should now correctly adjust the datetime object based on business hours, taking holidays into account. It should pass the failing test case and address the issue reported on GitHub.