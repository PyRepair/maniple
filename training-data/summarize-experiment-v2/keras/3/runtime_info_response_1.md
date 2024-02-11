Shortened version of the input and output pair related to the failing test cases for Case 1 is given below.

**Input:**

model._input_layers: `[<keras.engine.input_layer.InputLayer object at 0x7f21169baa10>]`

model.inputs: `[<tf.Tensor 'input_1:0' shape=(?, 4) dtype=float32>]`


**Output:**

layer_map: `{<keras.engine.input_layer.InputLayer object at 0x7f21169baa10>: <keras.engine.input_layer.InputLayer object at 0x7f21169bf0d0>}`

input_tensors: `[<tf.Tensor 'input_1_1:0' shape=(?, 4) dtype=float32>]`

input_layers: `[]`

layer.name: `'swap_layer_1'`

x: `<tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>`

y: `<tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>`

nodes: `[<keras.engine.base_layer.Node object at 0x7f211717eed0>]`

reference_input_tensors: `[<tf.Tensor 'lambda_1/add:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'lambda_1/Identity:0' shape=(?, 4) dtype=float32>]`

reference_output_tensors: `[<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>]`

computed_tensors: `[<tf.Tensor 'lambda_1_1/add:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'lambda_1_1/Identity:0' shape=(?, 4) dtype=float32>]`

tensor: `<tf.Tensor 'swap_layer_1_1/Identity_1:0' shape=(?, 4) dtype=float32>`