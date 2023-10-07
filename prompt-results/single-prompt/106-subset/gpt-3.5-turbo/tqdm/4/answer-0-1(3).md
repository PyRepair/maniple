The bug in the code is that the variable `total` is being multiplied by `unit_scale` when `total` is `None`. This causes a `TypeError` because `None` cannot be multiplied by an integer.

To fix this bug, we can add a check before multiplying `total` by `unit_scale`. If `total` is `None`, we can simply assign `total` to be `None