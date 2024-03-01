### Explanation:
The buggy function `convert_image` is intended to convert images to RGB mode and resize them if a `size` parameter is provided. However, there are a few issues in the implementation that cause incorrect behavior:
1. In the first `if` condition, the image format check is incorrect. The condition checks whether the image format is 'PNG' instead of 'JPEG', leading to unexpected behavior.
2. In the same `if` condition, when the image mode is 'RGBA', the pasting logic is incorrect, causing the image to be converted to RGB with a white background.
3. The `background` image is then used for the subsequent conversion, leading to issues if the image mode is already 'RGB'.
4. In the resizing logic, the function creates a copy of the image before resizing, which may not be necessary and could lead to unexpected behavior.

### Strategy for fixing the bug:
1. Fix the image format check in the first `if` condition to compare the format with 'JPEG'.
2. Adjust the code inside the `if` block to correctly handle the conversion of RGBA images to RGB without changing the background.
3. Check if the image mode is 'RGB' before attempting to convert it to RGB.
4. Remove the unnecessary image copy operation before resizing if not required.

### Corrected version of the function:
```python
def convert_image(self, image, size=None):
    if image.format == 'JPEG':  # Fix image format check
        if image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, (0, 0, image.size[0], image.size[1]))
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')
            
    if size:
        image.thumbnail(size, Image.ANTIALIAS)
        
    buf = BytesIO()
    image.save(buf, 'JPEG')
    return image, buf
```

By making these corrections, the function should now correctly handle images in different formats and modes, ensuring proper conversions and resizing as needed.