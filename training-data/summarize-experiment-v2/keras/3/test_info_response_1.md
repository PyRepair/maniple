The error message is indicating that an `AssertionError` occurred in the file `keras/models.py` at line 166. The specific error message is "Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)".

The error occurred during the execution of the function `_clone_functional_model` in the file `keras/models.py` at line 166. The error is due to the assertion that the output tensor is not present in the `tensor_map`.

Simplified error message:
```
AssertionError: Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)
```