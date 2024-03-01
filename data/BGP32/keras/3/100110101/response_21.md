### Analysis
The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights instead of sharing them. The function iterates over the nodes of the model in depth order, creating new layers for each node and storing the relationships between input and output tensors in `layer_map` and `tensor_map`.

The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple output tensors and then attempts to clone the model using the buggy function `clone_model`, which internally calls `_clone_functional_model`. The error occurs when trying to compute the output tensors for the new model, indicating that the function fails to correctly handle the computation.

### Bug Explanation
The bug arises due to an issue in the handling of input tensors and creating the new layers during the cloning process. The function fails to properly set up the new layers and their relationships with the input and output tensors, leading to the error when trying to compute the output tensors for the cloned model.

### Bug Fix Strategy
To fix the bug, the function `_clone_functional_model` needs to ensure that the created layers are correctly connected to input and output tensors. The mapping between input and output tensors should be accurately maintained during the depth-first iteration over the nodes of the model.

### Corrected Function
Here is the corrected version of the `_clone_functional_model` function based on the analysis:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape, dtype=layer.dtype) for layer in model._input_layers]
        
    for original_input_layer, tensor in zip(model._input_layers, input_tensors):
        layer_map[original_input_layer] = tensor
        tensor_map[tensor] = tensor

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort()
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                
                output_tensors = layer(computed_tensors, **kwargs)
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected function ensures that the mapping between input and output tensors is accurately preserved during the cloning process, allowing the function to correctly compute the output tensors for the cloned model.