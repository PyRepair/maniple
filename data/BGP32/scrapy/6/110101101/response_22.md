### Cause of the bug:
The bug in the `convert_image` function arises from the condition where the image format is 'PNG' and mode is 'RGBA'. In this case, it attempts to create a new image with a white background and paste the original image on top of it, but it mistakenly uses `background.paste(image, image)` instead of `background.paste(image)` which causes the paste operation to go wrong.

### Strategy for fixing the bug:
To fix the bug, we need to correct the line where the image is pasted onto the background by removing the extra `image` argument from the `paste` function when the format is 'PNG' and mode is 'RGBA'.

### The corrected version of the `convert_image` function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image)
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