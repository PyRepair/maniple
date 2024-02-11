The error occurs in the `clone_model` function of `keras.models.py` at line 166. The error is raised when attempting to compute the outputs of the model. It fails at the assertion check where it cannot compute the output for the specified tensor.

The error message in the failing test script points to the `clone_model` function and identifies a specific tensor for which the output cannot be computed.

Simplified Error Message:
```
Assert Error: Could not compute output for tensor "swap_layer_1/Identity:0"
```