### Bug Explanation
The bug in the `convert_image` function lies in the condition where it checks if the input image format is `'PNG'` and the mode is `'RGBA'`. In this case, it creates a new image with a white background and pastes the original image onto it before converting it to `'RGB'`. However, the `paste` method should take an image instance as the second argument, not the original image variable `image`.

### Fix Strategy
To fix this bug, we need to correct the way the original image is pasted onto the new background image in the code block for PNG images with RGBA mode. 

### Corrected Version
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