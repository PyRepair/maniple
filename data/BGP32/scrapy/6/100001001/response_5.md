### Analysis
1. The function `convert_image` is supposed to take an image, optionally resize it, convert it to RGB mode, and then save it in JPEG format.
2. The bug seems to be related to incorrectly handling PNG images in RGBA mode.
3. The bug causes incorrect handling of PNG images in RGBA mode when converting them to RGB.
4. To fix the bug, we need to correctly convert PNG images in RGBA mode to RGB mode before resizing and saving them in JPEG format.

### Bug Fix
Here is the corrected version of the function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGB', image.size, (255, 255, 255))  # Create a new RGB background image
        background.paste(image, (0, 0), image)  # Paste the RGBA image onto the background
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

In the fixed version:
- We create a new RGB background image for PNG images in RGBA mode.
- We paste the RGBA image onto this background to convert it to RGB.
- We adjust the paste method to correctly paste the RGBA image onto the RGB background.
- If the input image is not in RGB mode, we convert it to RGB as before.
- We generate the thumbnail based on the corrected image.
- Finally, we save the image in JPEG format as intended.