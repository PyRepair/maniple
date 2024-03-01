### Bug Analysis
The bug seems to be occurring because the `BusinessHourMixin` class does not have an implementation of the `_get_business_hours_by_sec` method, which is used in the `apply` method. This missing method is causing the `apply` method to fail when trying to calculate the total business hours by seconds in one business day.

### Bug Fix Strategy
To fix the bug, we need to implement the `_get_business_hours_by_sec` method in the `BusinessHourMixin` class. This method should return the total business hours in seconds for the given start and end time of a business hour.

### Corrected Version
Here is the corrected version of the `BusinessHourMixin` class with the implemented `_get_business_hours_by_sec` method:

```python
class BusinessHourMixin(BusinessMixin):
     @apply_wraps
     def apply(self, other):
        if isinstance(other, datetime):
            ... # existing code
        
            # get total business hours by sec in one business day
            def _get_business_hours_by_sec(start_time, end_time):
                start_seconds = start_time.hour * 3600 + start_time.minute * 60
                end_seconds = end_time.hour * 3600 + end_time.minute * 60
                return max(end_seconds - start_seconds, 0)
            
            businesshours = sum(
                _get_business_hours_by_sec(st, en)
                for st, en in zip(self.start, self.end)
            )
            
            ... # existing code

        else:
            raise ApplyTypeError("Only know how to combine business hour with datetime")
```

By adding the `_get_business_hours_by_sec` method to calculate the business hours in seconds, it should now correctly calculate the business hours and return the expected output for the failing test case.