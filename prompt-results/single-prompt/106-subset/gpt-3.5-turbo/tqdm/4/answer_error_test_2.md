To fix the bug in the `format_meter` function, we need to modify the line where `total` is multiplied by `unit_scale`. The current code tries to multiply `total` by `unit_scale`, but if `total` is `None`, it raises a `TypeError`. 

We can fix this bug by modifying the line to first check if `total` is not `None` before multiplying it by