### Bug Explanation
The bug in the `convert_image` function is caused by the condition `if image.format == 'PNG' and image.mode == 'RGBA'`. This condition checks if the image format is PNG and the mode is RGBA, but in the buggy function, if the image format is not PNG, then it will never enter the block to convert the image to RGB mode. This can cause issues and unexpected behavior when processing images of different formats.

### Bug Fix Strategy
To fix the bug, we should change the condition to handle cases when the image format is not PNG. Additionally, we should ensure that the image is always converted to RGB mode if it's not already in that mode. 

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background.convert('RGB')
        else:
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
``` 

By incorporating the else statement for cases when the image format is not PNG, we ensure that all images are converted to RGB mode if needed, providing a more robust and correct behavior for the function.