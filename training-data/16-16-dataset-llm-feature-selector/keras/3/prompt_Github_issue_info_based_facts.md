# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
def _clone_functional_model(model, input_tensors=None):
    """Clone a functional `Model` instance.

    Model cloning is similar to calling a model on new inputs,
    except that it creates new layers (and thus new weights) instead
    of sharing the weights of the existing layers.

    # Arguments
        model: Instance of `Model`.
        input_tensors: optional list of input tensors
            to build the model upon. If not provided,
            placeholders will be created.

    # Returns
        An instance of `Model` reproducing the behavior
        of the original model, on top of new inputs tensors,
        using newly instantiated weights.

    # Raises
        ValueError: in case of invalid `model` argument value.
    """
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
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    else:
        # Make sure that all input tensors come from a Keras layer.
        # If tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                # Cache newly created input layer.
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]
                # Don't call InputLayer multiple times.
                if isinstance(layer, InputLayer):
                    continue

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            # If all previous input tensors are available in tensor_map,
            # then call node.inbound_layer on them.
            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Call layer.
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_mask
                    output_tensors = to_list(
                        layer(computed_tensor, **kwargs))
                    output_masks = to_list(
                        layer.compute_mask(computed_tensor,
                                           computed_mask))
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_masks
                    output_tensors = to_list(
                        layer(computed_tensors, **kwargs))
                    output_masks = to_list(
                        layer.compute_mask(computed_tensors,
                                           computed_masks))
                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors,
                                      output_tensors,
                                      output_masks):
                    tensor_map[x] = (y, mask)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)

```

The github issue message is:
# A GitHub issue title for this bug
```text
'Could not compute output Tensor' error when I‘m using clone_model()
```

## The associated detailed issue description
```text
Hi guys, I think I just met a bug.
There was something wrong when I was using multi_gpu_model with cpu_relocation=True. After analyzing the traceback I think it is a bug inside keras.models.clone_model
The script below can reproduce it

from keras.models import Model, clone_model
from keras.layers import Input, Add, Lambda
from keras.utils import multi_gpu_model


def build_model():
    input_layer = Input(shape=(1,))
    test1, test2 = Lambda(lambda x: [x, x])(input_layer)
    add = Add()([test1, test2])
    model = Model(inputs=[input_layer], outputs=[add])
    return model


if __name__ == '__main__':
    model = build_model()
    model = clone_model(model)
    # model = multi_gpu_model(model, cpu_relocation=True)  # it uses clone_model when set cpu_relocation=True
If I didn't make any mistake, the script will raise AssertionError: Could not compute output Tensor("add_1/add:0", shape=(?, 1), dtype=float32)

My environment:

Keras 2.2.4
tensorflow 1.12.0
I met the error on both 4 GTX1080tis and my own laptop with a GTX1060MQ

I noticed that output_masks here will always be [None](but [None, None] is expected)
keras/keras/models.py

Line 157 in a139716

 for x, y, mask in zip(reference_output_tensors, 
and that's because layer.compute_mask(...) will always return None since Lambda doesn't support using masks
keras/keras/models.py

Line 153 in a139716

 output_masks = to_list( 
So if I'm using a functional model with a layer which has more outputs without a mask support, I think the error can appear.

P.S. thanks a lot for your brilliant works :)
From my perspective, Keras is an amazing gift to everyone. Thank you all!
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


