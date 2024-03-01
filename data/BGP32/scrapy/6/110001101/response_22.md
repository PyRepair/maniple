### Analysis
The buggy function `convert_image` contains logic to convert images to RGB format and resize them. However, there are issues with the conditional checks and the image processing steps, leading to incorrect output in some cases.

#### Potential Error Locations:
1. The conditional check for PNG format and RGBA mode seems to have a bug since the background image creation and pasting operation are incorrect.
2. The conversion logic for non-RGB images needs to be reviewed.
3. Resizing the image based on the provided size parameter might not be functioning as expected.

### Bug Explanation
1. In Case 3, when the input image is in PNG format and RGBA mode, the background is created with a white color but fails to paste the original image onto it correctly. This results in an incorrectly processed image.
2. The conversion logic for non-RGB images seems problematic as the code currently converts them to RGB unconditionally, which may not be the intended behavior.
3. The resizing operation based on the provided size parameter might have issues as the output image size in Case 2 does not match the expected size.

### Solution Strategy
1. Fix the conditional check for PNG format and RGBA mode to correctly paste the original image onto the background.
2. Review and improve the conversion logic for non-RGB images to handle different modes effectively.
3. Ensure that the resizing operation resizes the image correctly as per the given size parameter.

### Corrected Version of the Function:
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

By making the above corrections, the function should now operate as expected for all the provided cases.