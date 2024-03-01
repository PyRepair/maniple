### Analysis:
- The function `_clone_functional_model` is intended to clone a functional Model instance by recreating the model using new layers with new weights.
- The failing test `test_clone_functional_model_with_multi_outputs` creates a functional model with layers having multiple outputs.
- The error message indicates that a Tensor output from a layer (`swap_layer_1/Identity:0`) could not be computed, leading to an assertion error.
- The GitHub issue reports a similar problem where `clone_model` fails when used with `multi_gpu_model` and `cpu_relocation=True`.
- The bug is likely related to how the model's inputs, layers, and outputs are handled during the cloning process.
  
### Potential Error Locations:
1. Handling of input tensors and layer mapping.
2. Retrieving and processing input and output tensors of model nodes.
3. Assertion on computing model outputs.

### Bug Cause:
The bug arises due to incorrect handling of input tensors, layer mapping, and output computation in the `_clone_functional_model` function. As a result, some output tensors cannot be computed correctly, leading to an assertion error when trying to instantiate the new model.

### Bug Fix Strategy:
1. Ensure correct mapping of layers and input tensors during cloning.
2. Properly handle retrieving and processing input and output tensors.
3. Validate the computation of all model outputs before instantiating the new model.

### Corrected Version:
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
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for depth in reversed(range(len(model._nodes_by_depth))):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue
            
            reference_input_tensors = node.input_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks[0] if len(computed_masks) == 1 else computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the corrections to the `_clone_functional_model` function, it should be able to correctly clone the functional model in the provided test case and resolve the reported GitHub issue.