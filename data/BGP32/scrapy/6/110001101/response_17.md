## Bug Explanation
The bug in the `convert_image` function is in the conditional check for PNG images with RGBA mode. When the condition `image.format == 'PNG' and image.mode == 'RGBA'` is true, it creates a new RGBA background image and tries to paste the original image onto it using `background.paste(image, image)`, which is incorrect. It should be `background.paste(image)` to paste the original image onto the background. This incorrect paste operation results in distorted images.

## Bug Fix Strategy
To fix the bug, the correct paste operation should be applied to avoid image distortion. Additionally, the bug might be related to the incorrect image conversion logic. It is better to handle the RGB conversion separately if needed based on the image's mode.

## Corrected Version of the Function

```python
# The corrected version of the function

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