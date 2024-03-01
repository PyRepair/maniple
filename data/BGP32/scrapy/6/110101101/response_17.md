### Bugs Identified:
1. In the if condition where the format is 'PNG' and mode is 'RGBA', the `background.paste(image, image)` is incorrect. It should be `background.paste(image, (0, 0))` to properly paste the image onto the background.
2. In the test case where size is specified for thumbnail generation, the function itself is not preserving the aspect ratio correctly.

### Bug Explanation:
1. The buggy function incorrectly handles the case when the image format is 'PNG' and mode is 'RGBA' by pasting the image onto the background using the image object itself rather than positioning it at `(0, 0)`. This results in an improper transformation of the image.
2. When generating a thumbnail with a specified size, the function fails to adjust the dimensions properly, leading to incorrect resizing and aspect ratio preservation issues.

### Bug Fix Strategy:
1. Update the code in the first condition to correctly paste the image onto the background by specifying the position as `(0, 0)` instead of using the image object.
2. Modify the code to properly adjust the image size while generating a thumbnail to maintain the correct aspect ratio based on the specified size.

### Corrected Version of the Buggy Function:
```python
class ImagesPipeline(FilesPipeline):
    """
    Abstract pipeline that implement the image thumbnail generation logic
    """
    
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0))
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

By making the above corrections, the `convert_image` function should now correctly handle cases where the image format is 'PNG' and mode is 'RGBA', and it should also preserve the aspect ratio when generating thumbnails with specified sizes.