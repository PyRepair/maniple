The issue in the function `_clone_functional_model` arises from how it handles the cloning process of layers, specifically when dealing with layers that don't support masks, causing an AssertionError. To fix this issue, we need to modify the logic for handling output masks when calling layers with multiple outputs.

### Bug Explanation:
- The failing test case involves a model containing layers that don't support mask computation.
- The function `_clone_functional_model` tries to compute masks for the output tensors of such layers, leading to an AssertionError because these layers cannot generate masks.
- When calling a layer with multiple inputs for which masks are not available, the function incorrectly tries to compute and store masks, leading to the failure.

### Fix Strategy:
- Modify the logic in the function to avoid attempting to compute masks for layers that don't support them.
- Update the code to handle the case of layers without mask support to prevent the generation of masks for their outputs.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = [Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name if not K.is_keras_tensor(x) else '') for i, x in enumerate(to_list(input_tensors))]
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in model._nodes_by_depth.keys():
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
                    continue
            
            reference_input_tensors = node.input_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [data[0] for data in computed_data]
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the `_clone_functional_model` function with these modifications, the issue reported in the GitHub post should be resolved, the failing test case should pass, and the expected input/output values should be satisfied.