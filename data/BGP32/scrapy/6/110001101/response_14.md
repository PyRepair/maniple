### Bug Explanation
The bug in the `convert_image` function lies in the condition where it checks if the image format is 'PNG' and the mode is 'RGBA'. If this is the case, it creates a new image with a white background and pastes the original image onto it. However, the way it pastes the image is incorrect, leading to incorrect results. Additionally, the save method specifies 'JPEG' format regardless of the original image format.

### Bug Fix Strategy
1. Correctly paste the image onto the background image.
2. Ensure that the saved format matches the original image format if no resizing is done.

### Corrected Function
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
    # Save in the original format if size is not specified
    if not size:
        image.save(buf, image.format)
    else:
        image.save(buf, 'JPEG')
    return image, buf
``` 

By employing the corrected function above, the bug should be successfully fixed by ensuring the correct pasting logic and saving image format.