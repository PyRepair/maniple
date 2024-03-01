### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with transparency (alpha channel). When the input image has the format 'PNG' and mode 'RGBA', the function attempts to convert it to an RGB image by creating a new RGBA background and pasting the original image onto it. However, this operation does not correctly handle transparency, leading to unexpected results.

### Bug Fix Strategy
To fix the bug, we need to ensure that transparency is handled properly when converting images from RGBA to RGB. One common approach is to use the `convert` method with the `mode` parameter set to 'RGB' directly, which will automatically handle transparency conversion.

### Corrected Function

```python
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """
    
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            image = image.convert('RGB')  # Convert RGBA to RGB properly
        elif image.mode != 'RGB':
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

By using the `convert` method with the appropriate `mode` parameter, we ensure that images with transparency are correctly converted to RGB format. This should fix the bug and make the function behave as expected in all test cases.