You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

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

