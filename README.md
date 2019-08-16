# Icon Extractor

![](https://travis-ci.com/beaverden/icon_extractor.svg?branch=master)

Extracts icons of the desired width and height from the executables in a directory
If there are no icons of such size, no icons will be extracted

To extract all icons and bitmaps, specify width and height as 0
The script loads `bin/icon_extractor.dll` as it's much easier and faster to operate with native ole automation functions

## Usage

`icon_extractor.py <path_to_files> <desired_width|0> <desired_height|0>`


## Examples

`icon_extractor.py path/to/files 32 64` - will extract all icons of the size 32x32 (height is doubled when it comes to resources, apparently)

`icon_extractor.py path/to/files 0 0` - will extract all icons



## Build

The binaries are built using cmake. Use `build.bat` to run the build. After it's done, the binaries will be moved to the `bin/` folder
