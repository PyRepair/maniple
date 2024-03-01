### Explanation of the bug
The bug occurs in the logic of checking and converting the image mode within the `convert_image` function. In the buggy version:
1. If the image format is 'PNG' and the mode is 'RGBA', the function attempts to create a new RGBA background image filled with white, paste the original image onto it, and then convert it to RGB. This process is incorrect and can lead to issues.
2. If the image mode is not 'RGB', the function directly converts the image to RGB, which is not necessary in all cases and may not handle other color modes properly.

### Bug Fix Strategy
To fix the bug, we should update the conditional checks and conversion logic for different image modes and formats. Here is the corrected version of the `convert_image` function:

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

This corrected version simplifies the image mode checks and handles the format and mode conversions appropriately. Now, the function won't create unnecessary intermediate images or incorrect mode conversions.