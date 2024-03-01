The buggy function `convert_image` has a few issues that need to be addressed to handle the different image formats and modes correctly.

1. In Case 1 and Case 2, the function does not handle images with format 'JPEG' correctly. It unnecessarily converts the image to JPEG format even when the format is already 'JPEG'.
2. In Case 2, when resizing the image, the function does not update the size of the image properly based on the provided `size`.

To fix the function, we need to adjust the conditions for format handling and correctly resize the image based on the provided `size`.

Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)
    
    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

With these corrections, the function should handle the different image formats and modes correctly and resize the image as specified in the `size` parameter.