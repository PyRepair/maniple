### Analysis:
1. The `_clone_functional_model` function is used to create a deep copy of a functional model, ensuring new layers and weights are instantiated instead of sharing them with the original model.
2. The failing test `test_clone_functional_model_with_multi_outputs` demonstrates an issue when trying to clone a model containing multiple outputs and using a `Lambda` layer.
3. The error message indicates a failure in computing the output of a specific tensor.
4. The expected outputs of relevant variables are provided for each case to guide the correction.

### Bug Cause:
The bug arises from `Lambda` layers not supporting masks, causing the `output_masks` to be set as `None`. This leads to an assertion error when checking for computed model outputs.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle cases where `output_masks` are `None` properly and ensure the model outputs are correctly computed. We can modify the code so that it can handle scenarios where masks are not present for certain layers.

### Corrected Function:
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
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[x._keras_history[0]] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)

    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]

                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

### Correction Rationale:
- Updated the creation of input tensor mappings to handle cases where input tensors are provided.
- Modified the node processing loop to correctly handle layers that don't support masks, such as `Lambda`.
- Adjusted the output tensor computation for layers with multiple outputs and no mask support.
- Ensured the correct mapping and return of output tensors for the new cloned model.