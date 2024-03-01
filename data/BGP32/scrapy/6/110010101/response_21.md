### Analysis
The `convert_image` function within the `ImagesPipeline` class is intended to convert an image to RGB mode and resize it if necessary. However, there are several issues in the current implementation that cause it to fail in certain scenarios. The function incorrectly handles PNG images with RGBA mode and fails to properly convert them to RGB mode. Additionally, when resizing images, it does not maintain the aspect ratio, leading to incorrect image sizes.

### Bugs
1. Incorrect handling of PNG images with RGBA mode: The function does not properly convert these images to RGB mode, resulting in incorrect colors.
2. Incorrect resizing of images: When a size is specified for resizing the image, the function does not maintain the aspect ratio, leading to distorted images.

### Bug Fixes
1. For PNG images with RGBA mode, create a new white background image in RGBA mode to properly paste the original image onto it before converting it to RGB mode.
2. When resizing the image, maintain the aspect ratio by using the `thumbnail` method with the `Image.ANTIALIAS` option to prevent distortion.

### Corrected Code
Here is the corrected version of the `convert_image` function:

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

With these changes, the `convert_image` function should now handle PNG images with RGBA mode correctly and maintain the aspect ratio when resizing images. It should pass all the mentioned test cases and produce the expected output.