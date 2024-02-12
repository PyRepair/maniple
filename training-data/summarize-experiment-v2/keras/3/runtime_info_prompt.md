You have been given the source code of a function that is currently failing its test cases.

Image you are in the middle of debugging process and you have logged the variable values from this buggy function. Your mission involves analyzing each test case of runtime input/output values step by step and compare it with the core logic of the function. Using this comparisons, formulate the reason for the discrepancy and
summarise it.


# Runtime value and type of variables inside the buggy function
Each case below includes input parameter value and type, and the value and type of relevant variables at the function's return, derived from executing failing tests. If an input parameter is not reflected in the output, it is assumed to remain unchanged. Note that some of these values at the function's return might be incorrect. Analyze these cases to identify why the tests are failing to effectively fix the bug.

## Case 1
### Runtime value and type of the input parameters of the buggy function
model._input_layers, value: `[<keras.engine.input_layer.InputLayer object at 0x7f21169baa10>]`, type: `list`

model.inputs, value: `[<tf.Tensor 'input_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

model._nodes_by_depth, value: `{0: [<keras.engine.base_layer.Node object at 0x7f211717eed0>], 1: [<keras.engine.base_layer.Node object at 0x7f211717ead0>], 2: [<keras.engine.base_layer.Node object at 0x7f211717e910>]}`, type: `dict`

model.outputs, value: `[<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

model.name, value: `'model_1'`, type: `str`

### Runtime value and type of variables right before the buggy function's return
layer_map, value: `{<keras.engine.input_layer.InputLayer object at 0x7f21169baa10>: <keras.engine.input_layer.InputLayer object at 0x7f21169bf0d0>, <keras.layers.core.Lambda object at 0x7f211717ef10>: <keras.layers.core.Lambda object at 0x7f21169bf310>, <test_sequential_model.test_clone_functional_model_with_multi_outputs.<locals>.SwapLayer object at 0x7f211717ea90>: <test_sequential_model.test_clone_functional_model_with_multi_outputs.<locals>.SwapLayer object at 0x7f21169bac90>}`, type: `dict`

tensor_map, value: `{<tf.Tensor 'input_1:0' shape=(?, 4) ... (<tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>, None)}`, shape: `5`, type: `dict`

input_tensors, value: `[<tf.Tensor 'input_1_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

input_layers, value: `[]`, type: `list`

input_tensor, value: `<tf.Tensor 'input_1_1:0' shape=(?, 4) dtype=float32>`, type: `Tensor`

layer.name, value: `'swap_layer_1'`, type: `str`

input_tensor._keras_history, value: `(<keras.engine.input_layer.InputLayer object at 0x7f21169bf0d0>, 0, 0)`, type: `tuple`

x, value: `<tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>`, type: `Tensor`

x._keras_history, value: `(<test_sequential_model.test_clone_functional_model_with_multi_outputs.<locals>.SwapLayer object at 0x7f211717ea90>, 0, 1)`, type: `tuple`

y, value: `<tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>`, type: `Tensor`

depth_keys, value: `[2, 1, 0]`, type: `list`

depth, value: `0`, type: `int`

nodes, value: `[<keras.engine.base_layer.Node object at 0x7f211717eed0>]`, type: `list`

reference_input_tensors, value: `[<tf.Tensor 'lambda_1/add:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'lambda_1/Identity:0' shape=(?, 4) dtype=float32>]`, type: `list`

node.input_tensors, value: `[<tf.Tensor 'lambda_1/add:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'lambda_1/Identity:0' shape=(?, 4) dtype=float32>]`, type: `list`

reference_output_tensors, value: `[<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

node.output_tensors, value: `[<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

computed_data, value: `[(<tf.Tensor 'lambda_1_1/add:0' shape=(?, 4) dtype=float32>, None), (<tf.Tensor 'lambda_1_1/Identity:0' shape=(?, 4) dtype=float32>, None)]`, type: `list`

node.arguments, value: `{}`, type: `dict`

kwargs, value: `{}`, type: `dict`

computed_tensor, value: `<tf.Tensor 'input_1_1:0' shape=(?, 4) dtype=float32>`, type: `Tensor`

output_tensors, value: `[<tf.Tensor 'swap_layer_1_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>]`, type: `list`

layer.supports_masking, value: `False`, type: `bool`

output_masks, value: `[None, None]`, type: `list`

computed_tensors, value: `[<tf.Tensor 'lambda_1_1/add:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'lambda_1_1/Identity:0' shape=(?, 4) dtype=float32>]`, type: `list`

computed_masks, value: `[None, None]`, type: `list`

tensor, value: `<tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>`, type: `Tensor`