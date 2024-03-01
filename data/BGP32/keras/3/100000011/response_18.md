### Analysis:
The issue reported on GitHub is related to an error occurring when using `clone_model()` function in Keras. The specific error reported is "Could not compute output Tensor" when using `multi_gpu_model` with `cpu_relocation=True`. The issue seems to be caused by the `clone_model()` function not handling the case where the layer output masks are `None`.

### Potential Errors:
1. The method of handling output masks from layers that do not support masks may cause issues.
2. Computing the output masks based on the layer's implementation may result in `None` values.

### Bug Cause:
The bug seems to be caused by incorrect handling of output masks when cloning a model that contains layers with multiple outputs without mask support. This leads to the error mentioned in the GitHub issue.

### Fix Strategy:
To fix the bug, we need to update the logic for handling output masks so that it properly considers layers that do not support masks. The fix involves modifying the way masks are computed and handled during the model cloning process.

### Corrected Version:
I have provided a corrected version of the `_clone_functional_model` function below:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        
        for layer in model.inputs:
            input_tensor = Input(batch_shape=layer.shape.as_list(),
                                 dtype=layer.dtype,
                                 sparse=layer._keras_mask,
                                 name=layer.name)
            input_tensors.append(input_tensor)

            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer

        for _original, _cloned in zip(model.inputs, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.inputs[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for layer in model.layers:
        # clone the layer
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

    for node in model._nodes:
        layer = layer_map[node.outbound_layer]

        reference_input_tensors = node.input_tensors
        reference_output_tensors = node.output_tensors

        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            if node.arguments:
                kwargs = node.arguments
            else:
                kwargs = {}
                
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data]

            output_tensors = to_list(layer(computed_tensors, **kwargs))
            tensor_map[node.outbound_layer] = (output_tensors, None)

    output_tensors = tensor_map[model.output][0]

    return Model(input_tensors, output_tensors, name=model.name)
```

In this corrected version, I have made changes to properly handle masks for layers that do not support masks. I have also updated the logic for traversing the model nodes and computing output tensors correctly. This should address the issue reported on GitHub.