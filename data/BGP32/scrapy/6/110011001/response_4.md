### Explanation:
The bug in the `convert_image` function lies in the condition where it checks if the image format is 'PNG' and the mode is 'RGBA'. In this case, it creates a new background image of mode 'RGBA' and pastes the original image on it. However, when trying to save it as JPEG, it raises an error since the conversion to RGBA is not allowed for the JPEG format.

### Strategy for Fixing the Bug:
1. Fix the condition that handles the PNG format and RGBA mode appropriately.
2. Update the conversion logic to handle this case correctly by converting the image to RGB before resizing.
3. Ensure that the final image is saved in the desired JPEG format.

### The corrected version of the function:

```python
class ImagesPipeline(FilesPipeline):

    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background
        elif image.mode not in ['RGB', 'L']:
            image = image.convert('RGB')
    
        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)
    
        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf
```

By updating the condition to check for 'PNG' format and 'RGBA' mode to create a background image in 'RGB' mode and paste the original image correctly, we ensure that the function handles this case appropriately. Additionally, by only converting to RGB or L mode and resizing the image as needed, we avoid format conversion issues when saving in JPEG format.