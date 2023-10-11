```python
def build(self, input_shape):
    for cell in self.cells:
        if isinstance(cell, Layer):
            cell.build(input_shape)
        if hasattr(cell, 'state_size') and isinstance(cell.state_size, tuple):
            output_dim = cell.state_size[0]
        else:
            output_dim = cell.state_size
        input_shape = (input_shape[0], input_shape[1], output_dim)
    self.built = True
```
The bug in the original code is that it checks if `cell.state_size` has a `__len__` attribute