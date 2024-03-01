### Bug Explanation
The bug arises from the incorrect handling of PNG images with RGBA mode in the `convert_image` function. When the input image is of format "PNG" and mode "RGBA", the function incorrectly converts the image to RGB without taking into account the alpha channel.

### Bug Fix Strategy
To fix the bug, we need to ensure that when dealing with PNG images with RGBA mode, the alpha channel is properly handled. We should create a new RGBA image with a white background and paste the original RGBA image on top of it before converting it to RGB.

### Corrected Version
```python
# The declaration of the class containing the corrected function
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """
    
    # The corrected function
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))  # Adding alpha value for transparency
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

By updating the function to properly handle images with RGBA mode, the corrected version should now pass the failing test cases and provide the expected output values.