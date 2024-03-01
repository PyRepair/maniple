### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing the existing ones. The function attempts to clone layers and manage input/output tensors through a layer map and a tensor map. However, there are a few issues in the implementation that cause the function to fail when cloning a model with multiple outputs.

### Issues:
1. The function fails when dealing with models that have multiple output tensors.
2. The code does not handle multiple output tensors processing correctly, leading to mismatches when comparing the predicted outputs of the original and cloned models.

### Bug Cause:
The primary cause of the bug is the incomplete handling of models with multiple output tensors during the cloning process. The code does not properly update the tensor map for multiple output tensors, resulting in incorrect associations between input and output tensors.

### Strategy for Fix:
To fix the bug, we need to adjust the logic for handling multiple output tensors correctly. This involves updating the tensor map and mapping input tensors to output tensors when processing models with multiple outputs.

### Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
  
    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            name = model._input_layers[i].name
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = y

    for depth in model._nodes_by_depth:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            if all(x in tensor_map for x in reference_input_tensors):
                for x in reference_input_tensors:
                    computed_data.append(tensor_map[x])

                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer(computed_data, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the `_clone_functional_model` function as shown above, we ensure correct handling of models with multiple output tensors during the cloning process. This corrected version should pass the failing test `test_clone_functional_model_with_multi_outputs`.