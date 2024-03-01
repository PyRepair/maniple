### Bug Explanation
The bug in the `convert_image` function arises from the condition checking for the image format and mode, specifically with regards to PNG images in RGBA mode. The bug causes the function to incorrectly convert PNG RGBA images to RGB without maintaining transparency.

- In Case 3, the input image is a PNG image in RGBA mode. The function wrongly converts it to RGB without preserving the alpha channel, potentially causing transparency issues.

### Bug Fix Strategy
To fix the bug, we need to address the incorrect conversion of PNG images in RGBA mode to RGB. We should modify the logic to handle PNG RGBA images appropriately, ensuring that transparency is maintained.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        image = image.convert('RGBA')  # Ensure the image is in RGBA mode for transparency
        background = Image.new('RGBA', image.size, (255, 255, 255, 0))  # Create a transparent background
        background.paste(image, (0, 0), image)  # Paste the RGBA image on the background
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

In this corrected version:
- For PNG images in RGBA mode, we convert the image to RGBA explicitly, create a transparent background, and paste the RGBA image on the background to maintain transparency.
- Other image modes are converted to RGB as before.
- The rest of the function logic remains the same to handle resizing and saving images.