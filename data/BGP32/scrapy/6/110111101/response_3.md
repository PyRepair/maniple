### Explanation:
The bug in the `convert_image` function is due to incorrect handling of PNG images with RGBA mode. When the image format is PNG and mode is RGBA, the function creates a new RGBA background image to blend with the original image. However, when pasting the original image onto the background, the `image.paste()` method is incorrectly called with `image` as the second argument instead of `(0, 0)`, resulting in an incorrect blend.

### Fix strategy:
1. Check if the image format is `'PNG'` and the mode is `'RGBA'`.
2. If the conditions are met, create a new RGBA background image and correctly paste the original image onto it.
3. Convert the modified image to RGB.
4. Ensure to convert the image to RGB mode if it is not already in RGB mode.
5. If a specific size is provided, create a copy of the image and generate a thumbnail with the given size.

### Code Fix:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
        background.paste(image, (0, 0))
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

By fixing the `convert_image` function as described above, the function should now properly handle PNG images with RGBA mode and correctly generate thumbnails, passing the failing tests as well.