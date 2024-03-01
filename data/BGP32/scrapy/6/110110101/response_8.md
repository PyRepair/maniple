### Analysis
The buggy function `convert_image` in the `ImagesPipeline` class is responsible for converting images to a specific format and size. The bug is related to incorrect handling of images with format 'PNG' and mode 'RGBA'. The function incorrectly converts such images to 'RGB' without considering the transparency channel.

### Bug
The bug occurs in the code block where the function checks for PNG format images with RGBA mode and converts them to RGB mode. This conversion leads to a loss of transparency information, causing the conversion to be incorrect.

### Fix Strategy
1. Check if the image format is PNG and the mode is RGBA.
2. If the conditions are met, create a new RGBA image with a white background and paste the original image onto it.
3. Convert the background to RGB if the size is provided.
4. If the image is not PNG RGBA, check if it is not in RGB mode and convert it.
5. Finally, resize the image if a size is provided and save it as 'JPEG'.

### The Corrected Version
```python
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))  # Fix transparency channel
            background.paste(image, (0, 0))
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

By fixing the bug in the `convert_image` function as shown above, the function should now correctly handle images with PNG format and RGBA mode, ensuring that transparency is maintained during the conversion process.