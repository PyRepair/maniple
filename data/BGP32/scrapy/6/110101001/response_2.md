### Bug Explanation
The bug in the `convert_image` function lies in the condition checking for PNG format and RGBA mode images. When the condition is met, it creates a new RGBA background image, pastes the original RGBA image on it, and then converts it to RGB. However, the `paste` method expects a box parameter specifying where to paste the image, but instead, the entire image object `image` is being passed as the box parameter, resulting in an incorrect conversion.

### Bug Fix Strategy
To fix the bug, we need to correct the use of the `paste` method by specifying the box parameter correctly. Additionally, we need to handle the conversion from RGBA to RGB appropriately.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
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

With the above correction, the function will now correctly handle images in both RGBA and RGB modes and ensure proper conversion and thumbnail creation. This corrected version should pass the failing test cases provided.