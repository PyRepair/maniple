The error message is pointing to a failure in the `test_clone_functional_model_with_multi_outputs` test function, specifically in the call to `keras.models.clone_model(model)`.

Upon inspecting the implementation of the `_clone_functional_model` function, there are two key points of interest that relate to the error message:

1. Checking Input Model Type:
The `_clone_functional_model` function starts by checking whether the `model` argument is an instance of the `Model` class. If it is not, a `ValueError` is raised. This check is performed using the `isinstance(model, Model)` statement, which indicates that it expects the `model` argument to be an instance of the `Model` class.

2. Iterating through Model Nodes:
Within the `_clone_functional_model` function, there is a section that iterates through the nodes of the reference model in order to clone the layers and build a new model based on the input tensors. At the end of the iteration, the function checks that the model outputs have been computed properly. If an output tensor is not found in the `tensor_map`, an assertion error is raised with the message "Could not compute output" followed by the tensor value that could not be computed.

From the test function, the `model` that is being passed to `keras.models.clone_model` is created using `keras.Model`. This model involves the use of a Lambda layer and a custom `SwapLayer`.

Now, examining the specific error message, it states:
```
E           AssertionError: Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)
```
This means that the function was unable to compute the output for the given tensor, which represents the swap operation performed by the `SwapLayer` defined in the test function.

In conclusion, the error is related to the `SwapLayer` and how its output is being handled during the model cloning process. The specific conditions under which the output of the `SwapLayer` is being processed within the `_clone_functional_model` function might be causing the failure. Investigating the handling of the `SwapLayer` within the model cloning process would be an appropriate next step for debugging and resolving the issue.