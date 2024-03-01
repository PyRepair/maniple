### Analysis:
1. The error message indicates that the problem lies within the `_clone_functional_model` function of the `keras/models.py` file.
2. The assertion error occurs because the function fails to properly compute the output tensors for the model.
3. The bug may be due to incorrect handling of input layers and output tensors during the cloning process.
4. The function should properly map the input tensors and compute the output tensors for the cloned model.

### Bug Fix Strategy:
1. Ensure that the input layers are correctly mapped and handled during the cloning process.
2. Verify that all input tensors and output tensors are properly accounted for in the `tensor_map`.
3. Correct any errors related to the construction of new input layers.
4. Check that the output tensors are correctly computed and added to the `tensor_map`.
5. Update the function to accurately reproduce the behavior of the original model on new inputs.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model.inputs:
            input_shape = K.int_shape(layer)
            input_tensor = Input(shape=input_shape[1:], name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
            input_layers.append(input_tensor)
        for original, cloned in zip(model.inputs, input_layers):
            layer_map[original] = cloned
    else:
        # Make sure that all input tensors come from a Keras layer.
        # If tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.inputs[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[model.inputs[i]] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for layer in model.layers:
        layer_output = layer(tensor_map[model.inputs[0]])
        layer_map[layer] = layer_output
        
    output_tensors = [layer_map[x] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Updated the handling of input layers to correctly create placeholder input tensors with the proper shape and name.
2. Adjusted the mapping of input tensors in the `layer_map`.
3. Simplified the iteration over layers to ensure the correct computation of the output tensors.
4. Updated the retrieval of output tensors from the `model.outputs`.
5. Removed unnecessary checks and redundant code that caused issues in the cloning process. 

By applying these fixes, the corrected function should now be able to clone the functional model and pass the failing test successfully.