### Bug Explanation
The bug in the `convert_image` function lies in the conditional statement that checks if the image format is 'PNG' and the mode is 'RGBA'. In this case, it creates a new background and pastes the image on that background, but instead of using the pasted image, it reassigns the converted background without the pasted image back to the `image` variable. This leads to losing the alpha channel information when converting RGBA images to RGB.

### Fix Strategy
To fix the bug, we need to correctly paste the image on the new background and then save that image. Another issue is with the use of `paste` method, which should be changed to `alpha_composite` as the former does not work as intended. Additionally, when saving the image, we should check the format of the original image to maintain consistency.

### Corrected Version
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.alpha_composite(image)
        image = background.convert('RGB')
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)

    buf = BytesIO()
    if image.format:
        image.save(buf, image.format)
    else:
        image.save(buf, 'JPEG')

    return image, buf
``` 

By making these changes, the function should now correctly handle RGBA images when converting them to RGB without losing the alpha channel information.