There is a bug in the `format_meter` method where the variable `total` is assigned `None` and then multiplied by `unit_scale` which is an integer. This raises a `TypeError` since `None` cannot be multiplied by an integer.

To fix this bug,