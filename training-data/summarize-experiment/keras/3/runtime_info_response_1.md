Looking at the provided function code and the variable logs, it is evident that the function `_clone_functional_model` is not working as expected. Let's go through the input parameter values and variable runtime values to understand where the issue might be.

1. We have a model object of type `Model` with input layers, nodes by depth, outputs, and a name.
2. The `layer_map` and `tensor_map` are dictionaries used to cache created layers and map tensor references to corresponding newly created tensors.
3. The `input_tensors` list contains tensors to build the model upon.
4. We see the creation of `input_tensor` and caching of newly created input layer in the `layer_map`.
5. There is a loop over depth keys and nodes within each depth. Inside this loop, the corresponding layers are recovered and cloned.
6. The reference input and output tensors are gathered, and if all previous input tensors are available in `tensor_map`, then the node's `inbound_layer` is called using the input tensors.

Given the variable runtime values, we know that the `layer_map` and `input_tensors` are being modified inside the function - new layers are being created and input tensors updated. The cloned layers, input tensor mappings, and computation of output tensors seem to be working fine based on the variable logs.

Upon careful examination, it seems that the issue could be related to the final instantiation of the new model from inputs and outputs. The `output_tensors` are being checked for computation, and then a new model is instantiated using these inputs and outputs.

However, in the specific failing test case, the problem might be related to the `output_tensors` not being properly computed or matched with the original model's outputs. We need to verify that the `tensor_map` is correctly mapping the original outputs to the computed output tensors. Additionally, we need to ensure that the new model is being instantiated correctly from the updated `input_tensors` and `output_tensors`.

Further debugging and testing are required to identify the exact cause of the failing test cases and to fix the function `_clone_functional_model` accordingly.