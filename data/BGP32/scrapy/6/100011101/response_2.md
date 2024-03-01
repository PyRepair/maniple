## Bug Explanation
The bug in the `convert_image` function occurs when dealing with images in RGBA mode and PNG format. When the condition `if image.format == 'PNG' and image.mode == 'RGBA':` is true, the code creates a new RGBA background, pastes the original image onto it, and then converts the result to RGB using `background.convert('RGB')`. However, the issue arises in the `background.paste(image, image)` call, where the original RGBA image is mistakenly used as both the image and the mask argument, causing the image to be pasted incorrectly onto the background.

This incorrect pasting operation results in unexpected colors in the converted image, leading to failing tests as the expected colors are not achieved.

## Bug Fix Strategy
To fix the bug in the `convert_image` function, the correct approach is to provide the image and mask arguments separately in the `background.paste()` method. By doing this, the image will be correctly pasted onto the background, ensuring that the conversion from RGBA to RGB retains the expected colors.

## The Corrected Function
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
    image.save(buf, 'JPEG')
    return image, buf
``` 

By updating the `convert_image` function as shown above, ensuring the correct usage of `background.paste()` with separate image and mask arguments, the bug causing incorrect colors in the converted images is resolved.