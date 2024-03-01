The bug in the provided function lies in the way the image is being pasted onto a new background in the case where the image format is 'PNG' and mode is 'RGBA'. The mistake occurs in the line `background.paste(image, image)`. 

The correct way to paste the image onto the background is `background.paste(image, (0, 0), image)`.

Here is the corrected version of the function:

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

This corrected function should now fulfill all the expected input/output values mentioned in the test cases.