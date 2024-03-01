## Bug Explanation
The bug in the `convert_image` function lies in the condition where it checks if the image format is `'PNG'` and the mode is `'RGBA'`. In this condition, it creates a new background image and pastes the original image onto it. However, the paste function is called incorrectly with `background.paste(image, image)`, which causes the original image to be pasted on top of itself, resulting in no visible change. This is incorrect and defeats the purpose of creating a new background image.

## Bug Fix Strategy
To fix this bug, we need to correct the paste function call to paste the original image onto the newly created background image correctly. We also need to ensure the rest of the logic works as expected based on the provided failing test cases.

## The corrected version of the function
```python
# The corrected convert_image function
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

This corrected version of the function properly pastes the original image onto the newly created background image by specifying the position `(0, 0)` and the image to paste. It also ensures the conversion and thumbnailing logic work as expected based on the provided failing test cases.