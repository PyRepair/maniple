### Analysis:
1. The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance, creating new layers and new weights instead of sharing them with the original model.
2. The test function `test_clone_functional_model_with_multi_outputs` involves creating a model with multiple input and output layers, including a custom `Lambda` layer and a `SwapLayer` custom layer.
3. The test fails when `new_model = keras.models.clone_model(model)` is called, leading to an assertion error stating that a certain output tensor could not be computed.
4. The error message is due to issues with layer cloning, especially in cases where the layer does not support masks.
5. The GitHub issue provides a similar scenario where using multi_gpu_model with `cpu_relocation=True` leads to the same error message when calling `clone_model` on a model containing a `Lambda` layer with multiple outputs.
6. The key problem lies in how the function handles layers with multiple outputs and mask support issues. Since the Lambda layer does not support masks, this causes the failure.

### Bug Cause:
The bug occurs due to how the function handles layers with multiple outputs, specifically when dealing with the `Lambda` layer that does not support masks. The error in the failing test and the GitHub issue provides a clear indication of the problem.

### Strategy for Fixing the Bug:
1. Check for layers that do not support masks, such as the Lambda layer, and handle them appropriately.
2. Ensure that proper handling of input and output tensors is done in cases where masks are not supported by the layers.

### Corrected Version of the Function:
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
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                 sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  
    
    for depth in range(len(model._nodes_by_depth)-1, -1, -1):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
    
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
                
                computed_tensors = [x[0] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function addresses the issues related to cloning layers with multiple output tensors, ensuring that layers without mask support, like the `Lambda` layer, are handled correctly.