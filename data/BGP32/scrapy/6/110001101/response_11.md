### Bug Explanation
The bug in the `convert_image` function occurs due to the condition `if image.format == 'PNG' and image.mode == 'RGBA'` being checked for PNG format and RGBA mode, but then trying to convert the background image back to RGB format. This results in an incorrect conversion and could potentially cause issues with the image processing.

### Bug Fix Strategy
To fix the bug, we need to ensure that when the image format is PNG and mode is RGBA, we correctly handle the conversion to RGB format. We also need to address the conversion to RGB for images that are not in RGB mode.

### Corrected Function
```python
# The declaration of the class containing the corrected function
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """
    
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
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

By making these adjustments to the condition and handling of the image conversion, the `convert_image` function should now correctly process images of different formats and modes as expected.