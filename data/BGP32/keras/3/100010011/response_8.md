### Analysis:
1. The bug occurs when using `clone_model()` with a multi-output functional model that includes a Lambda layer without mask support.
2. The error message indicates that the computation of one of the output tensors fails because the tensor is not found in the `tensor_map`.
3. The Lambda layer in the model is causing the issue as it does not support masks, resulting in the output_masks being `None`.
4. The bug originates from the handling of the output masks in functional models with layers that do not support masks, leading to missing output tensors in the `tensor_map`.
   
### Fixing Strategy:
1. Ensure that the tensor_map is correctly updated even if the output masks are None.
2. Handle the case where the output masks are None for layers that do not support masks.
3. Update the code to build the functional model clone without encountering the missing output tensor issue.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=(None,) + x.shape[1:]) for x in model.inputs]

    # Iterated over every node in the reference model, in depth order.
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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                
                computed_tensors = [x[0] for x in computed_data]
                
                if len(computed_data) == 1:
                    computed_tensor = computed_data[0][0]
                    if has_arg(layer.call, 'mask'):
                        kwargs['mask'] = None
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    if has_arg(layer.call, 'mask'):
                        kwargs['mask'] = [None] * len(computed_tensors)
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
``` 

Now, the updated `_clone_functional_model` function should handle the multi-output functional model with layers that don't support masks correctly without encountering the "Could not compute output Tensor" error.