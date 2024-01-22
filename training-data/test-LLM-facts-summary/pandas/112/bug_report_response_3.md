```python
from typing import Optional
import numpy as np

class IntervalIndex:
    def __init__(self):
        pass

    def _check_method(self, method):
        # do something
        pass

    def equals(self, other):
        # do something
        pass

    @property
    def left(self):
        # return left attribute
        pass

    @property
    def right(self):
        # return right attribute
        pass

    @property
    def is_overlapping(self):
        # return is_overlapping attribute
        pass

    def _maybe_convert_i8(self, target_as_index):
        # convert target_as_index to i8
        pass

    def get_indexer(self, target: np.array, method: Optional[str] = None, limit: Optional[int] = None, tolerance: Optional[Any] = None) -> np.ndarray:
        if method:
            self._check_method(method)

        if self.is_overlapping:
            msg = (
                "cannot handle overlapping indices; use "
                "IntervalIndex.get_indexer_non_unique"
            )
            raise Exception("InvalidIndexError", msg)

        target_as_index = ensure_index(target)

        if isinstance(target_as_index, IntervalIndex):
            if self.equals(target_as_index):
                return np.arange(len(self), dtype="intp")
            common_subtype = find_common_type(
                [self.dtype.subtype, target_as_index.dtype.subtype]
            )
            if self.closed != target_as_index.closed or is_object_dtype(common_subtype):
                return np.repeat(np.intp(-1), len(target_as_index))
            left_indexer = self.left.get_indexer(target_as_index.left)
            right_indexer = self.right.get_indexer(target_as_index.right)
            indexer = np.where(left_indexer == right_indexer, left_indexer, -1)
        elif not is_object_dtype(target_as_index):
            target_as_index = self._maybe_convert_i8(target_as_index)
            indexer = np.where(self.values == target_as_index)
        else:
            indexer = np.where(self.values == target_as_index)

        return indexer
```