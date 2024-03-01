### Explanation of the bug
The bug in the `convert_image` function lies in the conditional check for PNG images with RGBA mode. If an image is PNG format and RGBA mode, the function attempts to convert it to RGB by creating a new image with a white background and pasting the original image onto it. However, the `paste` method uses two arguments, the image to paste and a tuple representing the position to paste it at. In this case, it should be `(0, 0)` to start pasting at the top-left corner.

### Strategy for fixing the bug
To fix the bug, we need to correct the usage of the `paste` method by providing the correct position to paste the image onto the background image.

### Corrected version of the function
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0))  # Correct the paste method with the correct position
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

By correcting the position argument in the `paste` method to `(0,0)`, the function will correctly create a new RGB image from PNG images in RGBA mode without any errors.