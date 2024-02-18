The relevant input/output values are
- self.blocks, value: (IntBlock: slice(0, 1, 1), 1 x 2, dtype: int64, ObjectBlock: slice(1, 2, 1), 1 x 2, dtype: object), type: tuple
- other.blocks, value: (IntBlock: slice(1, 2, 1), 1 x 2, dtype: int64, ObjectBlock: slice(0, 1, 1), 1 x 2, dtype: object), type: tuple
Rational: The bug is likely related to the comparison of blocks within the tuples. Both tuples contain blocks of the same type and shape, but in a different order, which could lead to a false negative in the equality check.