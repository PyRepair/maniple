### Explanation:
The bug in the `convert_image` function arises from the incorrect handling of PNG images with RGBA mode. When the input image format is PNG and its mode is RGBA, the function attempts to convert it to RGB by creating a new RGBA background and pasting the original image onto it. However, the image is pasted on top of itself (by using the same image object `image`), resulting in an incorrect conversion.

### Bug Fix Strategy:
1. When dealing with PNG images in RGBA mode, a new image object should be created to store the converted image.
2. Use the `Image.alpha_composite()` method to correctly composite the images and handle transparency in RGBA images.

### The corrected version of the function:
```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background = Image.alpha_composite(background, image)  # Composite the images correctly
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

This corrected version of `convert_image` addresses the bug by correctly handling RGBA to RGB conversion for PNG images and uses `alpha_composite` to paste the images without the original image being affected by the conversion process.