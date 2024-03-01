### Explanation of the bug
The buggy function `convert_image` in the `ImagesPipeline` class is meant to process images before saving them. The bug occurs when the input image's format is 'PNG' and mode is 'RGBA'. In that case, the function attempts to convert the image to 'RGB' format, but it mistakenly pastes the original image onto a new background image. This leads to unexpected behavior and incorrect image processing.

### Bug location
The bug is located in the conditional block where the image format is 'PNG' and mode is 'RGBA'. Specifically, the code `background.paste(image, image)` is incorrect as it pastes the image on itself.

### Bug cause
The bug is caused by incorrect handling of the image conversion in the case of PNG images with RGBA mode. Instead of directly converting the image to 'RGB', the code mistakenly tries to paste it onto a new background.

### Fix strategy
To fix the bug, we need to correct the way the image is converted when its format is 'PNG' and mode is 'RGBA'. Instead of pasting the image onto a new background, we should directly convert it to 'RGB'. Additionally, it's important to ensure that the image is copied before processing it further to avoid unintentionally modifying the original image.

### Corrected version of the function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

In this corrected version, the image is directly converted to 'RGB' when its format is 'PNG' and mode is 'RGBA. Additionally, we ensure that the image is copied before performing any modifications to avoid altering the original image.