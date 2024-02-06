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
        x /= 127.5
        x -= 1.
        return x
    elif mode == 'torch':
        x = x.astype('float32') # explicitly cast to float32
        x /= 255.
    else:
        if data_format == 'channels_first':
            # 'RGB'->'BGR'
            if x.ndim == 3:
                x = x[:, ::-1, ...]
            else:
                x = x[:, :, ::-1, ...]
        else:
            # 'RGB'->'BGR'
            x = x[..., ::-1]

    mean = np.array([103.939, 116.779, 123.68], dtype=np.float32)
    std = None
    if mode == 'torch':
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    # Zero-center by mean pixel
    x -= mean
    if std is not None:
        x /= std

    return x
```