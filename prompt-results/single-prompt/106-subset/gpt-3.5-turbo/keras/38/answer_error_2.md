```python
def build(self, input_shape):
    for cell in self.cells:
        if isinstance(cell, Layer):
            cell.build(input_shape)
        if hasattr(cell.state_size, '__len__'):
            output_dim = cell.state_size[0]
        else:
            output_dim = cell.state_size
        input_shape = input_shape[:2] + (output_dim,)
    self.built = True
```

The buggy code is failing at the line `assert len(input_shape) == 2` because the input shape has dimensions `(None, 5, 8)` which