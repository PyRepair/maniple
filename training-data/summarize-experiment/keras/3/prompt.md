Please correct the malfunctioning function provided below by using the relevant information listed to address this bug. Then, produce a revised version of the function that resolves the issue. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.

Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
from . import backend as K
from .utils.generic_utils import has_arg
from .utils.generic_utils import to_list
from .engine.input_layer import Input
from .engine.input_layer import InputLayer
from .engine.training import Model
from .engine.sequential import Sequential
```

The following is the buggy function that you need to fix:
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



## Test Functions and Error Messages Summary
The followings are test functions under directory `tests/keras/test_sequential_model.py` in the project.
```python
def test_clone_functional_model_with_multi_outputs():
    input_layer = keras.Input(shape=(4,))

    # Layer with single input and multiple outputs
    layer1 = keras.layers.Lambda(lambda x: [x + 1, x],
                                 lambda shapes: [shapes, shapes])
    x_a, x_b = layer1(input_layer)

    class SwapLayer(keras.layers.Layer):
        def call(self, inputs, **kwargs):
            return [inputs[1], inputs[0]]

        def compute_output_shape(self, input_shape):
            return [input_shape[1], input_shape[0]]

    # Layer with multiple inputs and outputs
    x_a, x_b = SwapLayer()([x_a, x_b])
    model = keras.Model(inputs=[input_layer], outputs=[x_a, x_b])
    new_model = keras.models.clone_model(model)

    x_test = np.random.random((10, 4))
    pred_a, pred_b = model.predict(x_test)
    pred_new_a, pred_new_b = new_model.predict(x_test)
    assert(pred_a.all() == pred_new_a.all())
    assert(pred_b.all() == pred_new_b.all())
```

Here is a summary of the test cases and error messages:
From the given source code and error messages, we can discern that there is an issue with the `clone_functional_model` function within the `keras/models.py` file. The error message originates from the test function `test_clone_functional_model_with_multi_outputs` within the `test_sequential_model.py` file.

The purpose of the `clone_functional_model` function is to create a new instance of the `Model` class by cloning the functional model. The error message indicates that the assertion `assert x in tensor_map` failed, citing a specific output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` which could not be computed.

In order to understand this error, we need to analyze the code in the `test_clone_functional_model_with_multi_outputs` function and the structure of the functional model being used.

Looking at the test function, it involves creating a functional model with multiple inputs and outputs, using layers like `Lambda` and `SwapLayer`. It asserts that the output of the cloned model is equal to the original model for given input data. The error occurs when the `clone_model` function is called on the `model`.

The error messages instantly reveal that the issue arises from the `clone_model` function calling the `_clone_functional_model` function. Within the `_clone_functional_model` function, there are multiple stages involved such as caching created layers, mapping input tensors, iterating through the reference model nodes, and creating the corresponding layers in the cloned model.

From the error message, the specific output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` indicates that there might be an issue with the `SwapLayer` and its output being properly computed or mapped with the `tensor_map`.

The failure of the assertion `assert x in tensor_map` means that there is a missing output tensor i.e., it was not properly computed or mapped during the process of cloning the model.

To effectively diagnose and resolve the issue, we need to carefully examine the following:
1. The creation and computation of the layers in the functional model, especially the ones with multiple inputs/outputs and custom behavior such as the `Lambda` and `SwapLayer`.
2. The caching and mapping of the input and output tensors in the `_clone_functional_model` function.
3. The process of iterating through the nodes of the reference model and creating corresponding layers in the cloned model.
4. The specific handling of complex layers such as `SwapLayer`, ensuring that their input and output tensors are properly considered and mapped during the cloning process.

By understanding and debugging these specific sections, we can identify the root cause of the error and introduce the necessary corrections to ensure the successful clone of the functional model.



## Summary of Runtime Variables and Types in the Buggy Function

Looking at the provided function code and the variable logs, it is evident that the function `_clone_functional_model` is not working as expected. Let's go through the input parameter values and variable runtime values to understand where the issue might be.

1. We have a model object of type `Model` with input layers, nodes by depth, outputs, and a name.
2. The `layer_map` and `tensor_map` are dictionaries used to cache created layers and map tensor references to corresponding newly created tensors.
3. The `input_tensors` list contains tensors to build the model upon.
4. We see the creation of `input_tensor` and caching of newly created input layer in the `layer_map`.
5. There is a loop over depth keys and nodes within each depth. Inside this loop, the corresponding layers are recovered and cloned.
6. The reference input and output tensors are gathered, and if all previous input tensors are available in `tensor_map`, then the node's `inbound_layer` is called using the input tensors.

Given the variable runtime values, we know that the `layer_map` and `input_tensors` are being modified inside the function - new layers are being created and input tensors updated. The cloned layers, input tensor mappings, and computation of output tensors seem to be working fine based on the variable logs.

Upon careful examination, it seems that the issue could be related to the final instantiation of the new model from inputs and outputs. The `output_tensors` are being checked for computation, and then a new model is instantiated using these inputs and outputs.

However, in the specific failing test case, the problem might be related to the `output_tensors` not being properly computed or matched with the original model's outputs. We need to verify that the `tensor_map` is correctly mapping the original outputs to the computed output tensors. Additionally, we need to ensure that the new model is being instantiated correctly from the updated `input_tensors` and `output_tensors`.

Further debugging and testing are required to identify the exact cause of the failing test cases and to fix the function `_clone_functional_model` accordingly.



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





# Instructions

1. Analyze the test case and its relationship with the error message, if applicable.
2. Identify the potential error location within the problematic function.
3. Explain the reasons behind the occurrence of the bug.
4. Suggest possible approaches for fixing the bug.
5. Present the corrected code for the problematic function.