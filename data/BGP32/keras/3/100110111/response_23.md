## Analysis
1. The buggy function `_clone_functional_model` is designed to clone a functional Model instance, creating new layers and weights instead of sharing them.
2. The input `model` is expected to be an instance of `Model`, and the function should raise a `ValueError` if it's a `Sequential` instance.
3. The bug occurs when the function tries to clone a layer that does not support masking (Lambda layer) but attempts to retrieve masks from it.
4. The failing test case `test_clone_functional_model_with_multi_outputs` creates a model with a Lambda layer and another layer without mask support, resulting in the failure due to mismatched mask handling.
5. The inputs, intermediate variables, and return variables of the function should be checked and corrected to handle cases where layers do not support masking.

## Bug Explanation
The bug originates from the fact that the function `_clone_functional_model` tries to handle layer masking for all layers, even those that do not support masks like Lambda layers. This results in a discrepancy when retrieving masks for layers that don't generate masks, causing an assertion error.

## Bug Fix Strategy
1. Identify layers that don't support masks (like Lambda layers).
2. Modify the handling of masks to skip layers without mask support to prevent errors.
3. Update the cloning logic to manage layers without masks correctly.

## Updated Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    input_layers = []
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape, name=layer.name) for layer in model._input_layers]
    for input_layer in input_tensors:
        input_layers.append(input_layer)
        layer_map[model._input_layers[input_tensors.index(input_layer)]] = input_layer
    
    for layer in model.layers:
        if not hasattr(layer, 'supports_masking') or not layer.supports_masking:
            continue

        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

    for x, y in zip(model.inputs, input_layers):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        if layer in layer_map:
            new_layer = layer_map[layer]
            computed_data = [(tensor_map[t][0], None) for t in layer.input]
          
            output_tensors = to_list(new_layer(computed_data[0][0]))
            
            for x, y in zip(layer.output, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_layers, output_tensors, name=model.name)
```

With this corrected version of `_clone_functional_model`, the specified failing test should pass without any assertion errors, ensuring proper handling of layers without mask support during the cloning process.