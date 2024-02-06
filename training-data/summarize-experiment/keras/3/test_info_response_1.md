From the error message, we can tell that the problem happens during the execution of the test case `test_clone_functional_model_with_multi_outputs` in the file `tests/keras/test_sequential_model.py`, specifically at line 360, which is the line where `keras.models.clone_model(model)` is called.

The specific assertion error is raised from the `_clone_functional_model` function in `keras.models.py` file at line 166. The assertion error is triggered by the line `assert x in tensor_map, 'Could not compute output ' + str(x)`.

By looking at the test function `test_clone_functional_model_with_multi_outputs`, we see that it is testing the cloning of a functional model with multiple outputs. The test involves creating some layers, defining the model, then cloning the model using `keras.models.clone_model(model)`.

The `keras.models.clone_model` function internally calls `_clone_functional_model` function, which is the source of the error. The error message indicates that there is an issue with computing the output tensor from the `clone_model` operation, as the specific tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` could not be found in the `tensor_map`.

The problem could be rooted in the construction of the `new_model` and particularly in how the tensors are mapped during the cloning process. 

We would need to inspect the `clone_model` operation in more detail and possibly trace back to the core of the `_clone_functional_model` function to identify why the output tensor is unable to be computed. It's possible that there's an issue with how the `tensor_map` is being populated or used during the cloning process. Further diagnosis would require a deep dive into the internals of the `clone_model` function and the `_clone_functional_model` function, possibly involving debugging and stepping through the code to understand how the tensors are being handled and why the specific output tensor cannot be computed.