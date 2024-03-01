### Analysis
The `convert_image` function is supposed to convert an image to RGB format and resize it if a size is provided. However, there are some issues in the implementation:
1. The condition for handling PNG images with RGBA mode seems to be incorrect.
2. The background image is not added correctly when converting PNG images with RGBA mode.
3. The image mode check seems problematic, as it doesn't consider all cases.

### Bug Explanation
1. The condition `if image.format == 'PNG' and image.mode == 'RGBA':` is incorrect because `image.format` refers to the file format, not the image mode. Thus, this condition will never be satisfied, leading to incorrect handling of PNG images with RGBA mode.
2. In the incorrect condition, when creating the `background` image to paste the original image on it, the `background.paste(image, image)` call is incorrect. It should be `background.paste(image, (0, 0), image)`.
3. The second condition `elif image.mode != 'RGB':` is also incorrect as it doesn't handle images with other modes properly. It should convert all non-RGB images to RGB.
4. Additionally, when saving the image in JPEG format, the function is hardcoded to always save as JPEG, regardless of the original image format.

### Proposed Fix
1. Update the condition to check if the image mode is 'RGBA' when the format is 'PNG'.
2. Correct the `background.paste` call by providing the correct position.
3. Update the image mode check to convert all non-RGB images to RGB.
4. Update the image save format to match the original image format.

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
    image.save(buf, image.format)
    return image, buf
```