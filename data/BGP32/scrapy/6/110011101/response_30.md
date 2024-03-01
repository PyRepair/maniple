### Bug Explanation
The bug in the `convert_image` function arises from the incorrect handling of images with transparency. When the input image format is PNG and mode is RGBA, the function is supposed to convert the image to RGB and handle the transparency. However, in the current implementation, it incorrectly converts the image format to RGB while ignoring the transparency.

### Bug Fix Strategy
To fix the bug, we need to correctly handle the transparency in RGBA images by creating a new background and pasting the image over it before converting it to RGB.

### The corrected version of the function
```python
def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
``` 

By making the mentioned changes, the function should now correctly handle images with transparency and pass the failing test cases.