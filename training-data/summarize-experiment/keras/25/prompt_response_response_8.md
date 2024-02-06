```python
import numpy as np

def _preprocess_numpy_input(x, data_format, mode):
    """Preprocesses a Numpy array encoding a batch of images.

    # Arguments
        x: Input array, 3D or 4D.
        data_format: Data format of the image array.
        mode: One of "caffe", "tf" or "torch".
            - caffe: will convert the images from RGB to BGR,
                then will zero-center each color channel with
                respect to the ImageNet dataset,
                without scaling.
            - tf: will scale pixels between -1 and 1,
                sample-wise.
            - torch: will scale pixels between 0 and 1 and then
                will normalize each channel with respect to the
                ImageNet dataset.

    # Returns
        Preprocessed Numpy array.
    """
    if mode == 'tf':
        x = x / 127.5 - 1.  # Scale pixels between -1 and 1
        return x

    if mode == 'torch':
        x = x / 255.  # Scale pixels between 0 and 1
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        # Normalize each channel with respect to the ImageNet dataset
        if data_format == 'channels_first':
            for i in range(3):
                x[:, i, :, :] -= mean[i]
                x[:, i, :, :] /= std[i]
        else:
            for i in range(3):
                x[..., i] -= mean[i]
                x[..., i] /= std[i]
        return x

    # Preprocessing for 'caffe' mode
    if data_format == 'channels_first':
        # 'RGB'->'BGR' for channels_first format
        if x.ndim == 3:
            x = x[::-1, ...]
        else:
            x = x[:, ::-1, ...]
    else:
        # 'RGB'->'BGR' for channels_last format
        x = x[..., ::-1]
    mean = [103.939, 116.779, 123.68]
    
    # Zero-center by mean pixel
    for i in range(3):
        x[..., i] -= mean[i]
    return x
```