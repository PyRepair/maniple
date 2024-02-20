Your task is to summarize the expected input and output values of a buggy function, following the example provided below.

## Example source code of the buggy function
```python
def calculate_total_cost(nights, rate_per_night):
    discount = 0.1  # 10% discount for stays longer than 7 nights
    if nights > 7:
        total_cost = nights * rate_per_night * (1 - discount)
    else:
        total_cost = nights * rate_per_night
    return total_cost
```

## Example expected value and type of variables during the failing test execution

### Expected case 1
#### Input parameter value and type
nights, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `790`, type: `int`

### Expected case 2
#### Input parameter value and type
nights, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `880`, type: `int`

### Expected Case 3
#### Input parameter value and type
nights, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Exptected Case 4
#### Input parameter value and type
nights, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `970`, type: `int`


## Example summary:
Case 1: Given the input parameters `nights=8` and `rate_per_night=100`, the function should return `790`. This might be calculated by `7 * 100 + 100 * 0.9 = 790`.

Case2: Given the input parameters `nights=9` and `rate_per_night=100`, the function should return `880`. This might be calculated by `7 * 100 + 2 * 100 * 0.9 = 880`.

Case3: Given the input parameters `nights=7` and `rate_per_night=100`, the function should return `700`. This might be calculated by `7 * 100 = 700`.

Case4: Given the input parameters `nights=10` and `rate_per_night=100`, the function should return `970`. This might be calculated by `7 * 100 + 3 * 100 * 0.9 = 970`.



## The source code of the buggy function

```python
def convert_image(self, image, size=None):
    if image.format == 'PNG' and image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, image)
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

## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F05549DED00>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

### Expected case 2
#### The values and types of buggy function's parameters
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F05549DED00>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

size, value: `(10, 25)`, type: `tuple`

#### Expected values and types of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=10x10 at 0x7F0554967310>`, type: `Image`

image.size, expected value: `(10, 10)`, type: `tuple`

### Expected case 3
#### The values and types of buggy function's parameters
image.format, value: `'PNG'`, type: `str`

image, value: `<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=100x100 at 0x7F05549677C0>`, type: `PngImageFile`

image.mode, value: `'RGBA'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

#### Expected values and types of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F05549DED90>`, type: `Image`

image.mode, expected value: `'RGB'`, type: `str`

background, expected value: `<PIL.Image.Image image mode=RGBA size=100x100 at 0x7F0554967CA0>`, type: `Image`

### Expected case 4
#### The values and types of buggy function's parameters
image, value: `<PIL.Image.Image image mode=P size=100x100 at 0x7F055495DE80>`, type: `Image`

image.mode, value: `'P'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

#### Expected values and types of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F0554967370>`, type: `Image`

image.mode, expected value: `'RGB'`, type: `str`

## Summary:

[Your summary here.]