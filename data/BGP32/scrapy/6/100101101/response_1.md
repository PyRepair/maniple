### Bug Explanation
The bug in the `convert_image` function occurs due to incorrect handling of images with format PNG and mode RGBA. When the input image has format PNG and mode RGBA, the function should create a new RGBA image with a white background and then convert it to RGB format. However, the function is incorrectly pasting the original RGBA image onto a new RGBA background image. This causes the resulting image to have an RGBA mode instead of RGB as expected.

### Bug Fix Strategy
To fix the bug, we need to create a new RGBA background image with a white background and paste the original image onto it. Then, convert the resulting background image to RGB format.

### Corrected Version of the Function
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

By correcting the pasting operation and converting the background image to RGB, the function will now handle PNG images with RGBA mode correctly and pass the failing test cases.