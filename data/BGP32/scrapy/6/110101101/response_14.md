### Bug Explanation
The bug occurs in the `convert_image` function where the conditional check for PNG format and RGBA mode images is causing an issue. When the image format is PNG and the image mode is RGBA, the function creates a new image with RGBA mode filled with a white background, pastes the original image onto it, and then converts it to RGB mode. However, the issue lies in the `paste` method where it requires a mask argument to specify which portions of the pasted image will be pasted. Without this mask argument, the original image is not correctly pasted onto the white background.

### Bug Fix Strategy
To fix the bug, we need to provide a mask argument in the `paste` method to correctly paste the original image onto the white background when dealing with PNG format and RGBA mode images.

### Corrected Version of the Function
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

By providing the proper mask argument in the `paste` method, the corrected function should now correctly handle PNG format and RGBA mode images, addressing the bug.