You have been given the source code of a function that is currently failing its test cases.

Your mission involves analyzing each test case of expected input/output values step by step and compare it with the core logic of the function. Using this comparisons, formulate the reason for the discrepancy and summarise it.


# Expected value and type of variables during the failing test execution
Each case below includes input parameter value and type, and the expected value and type of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

## Expected case 1
### Input parameter value and type
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F05549DED00>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

## Expected case 2
### Input parameter value and type
image.format, value: `'JPEG'`, type: `str`

image, value: `<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=100x100 at 0x7F05549DED00>`, type: `JpegImageFile`

image.mode, value: `'RGB'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

size, value: `(10, 25)`, type: `tuple`

### Expected value and type of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=10x10 at 0x7F0554967310>`, type: `Image`

image.size, expected value: `(10, 10)`, type: `tuple`

## Expected case 3
### Input parameter value and type
image.format, value: `'PNG'`, type: `str`

image, value: `<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=100x100 at 0x7F05549677C0>`, type: `PngImageFile`

image.mode, value: `'RGBA'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

### Expected value and type of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F05549DED90>`, type: `Image`

image.mode, expected value: `'RGB'`, type: `str`

background, expected value: `<PIL.Image.Image image mode=RGBA size=100x100 at 0x7F0554967CA0>`, type: `Image`

## Expected case 4
### Input parameter value and type
image, value: `<PIL.Image.Image image mode=P size=100x100 at 0x7F055495DE80>`, type: `Image`

image.mode, value: `'P'`, type: `str`

image.size, value: `(100, 100)`, type: `tuple`

### Expected value and type of variables right before the buggy function's return
image, expected value: `<PIL.Image.Image image mode=RGB size=100x100 at 0x7F0554967370>`, type: `Image`

image.mode, expected value: `'RGB'`, type: `str`