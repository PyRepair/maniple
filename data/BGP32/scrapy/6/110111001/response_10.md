### Bug Explanation
The bug in the `convert_image` function arises from the conditional check on `image.format` and `image.mode`. The condition `if image.format == 'PNG' and image.mode == 'RGBA':` is causing the issue. In some cases, images might have a format of PNG and mode RGBA, but they are not actually transparent images. Therefore, the logic within this conditional block is incorrect, resulting in incorrect image conversion.

### Bug Fix Strategy
To fix the bug, we need to modify the condition that checks the image format and mode to correctly handle transparent and non-transparent images. We should also ensure that the image conversion logic is executed appropriately for different image types.

### Corrected Version of the Function
```python
def convert_image(self, image, size=None):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    if size:
        image = image.copy()
        image.thumbnail(size, Image.ANTIALIAS)
    
    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

After implementing this fix, the function should now correctly handle different image types and sizes, as well as save the image in JPEG format. This corrected version should pass the failing test cases provided.