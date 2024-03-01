### Bug Explanation
The bug occurs in the `convert_image` function where it incorrectly converts images with a format of 'PNG' and mode of 'RGBA'. In the provided code, there are two main issues:
1. When the image format is 'PNG' and mode is 'RGBA', the code tries to convert the image format to 'RGB' by creating a white background and pasting the original image on top of it. However, the `paste` function should take coordinates as the first argument, but it's using the image object itself, causing improper conversion.
2. The code doesn't handle the transparency aspect of images properly. It merely converts to 'RGB' without accounting for the alpha channel, resulting in unexpected color values after the conversion.

### Fix Strategy
To address the issues mentioned above, the following fixes can be implemented:
1. Correct the usage of the `paste` function by passing coordinates for the image instead of the image object itself.
2. Handle the transparency of images correctly by considering the alpha channel when converting images.
3. Ensure that the correct image format is preserved after conversion.

### Corrected Code
```python
class ImagesPipeline(FilesPipeline):
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255, 255))
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

After applying these changes, the `convert_image` function should now correctly handle images with transparency and preserve the expected format and color values during conversions.