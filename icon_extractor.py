import pefile
import sys, os
from PIL import Image
import io
from PIL import ImageFile
import ctypes

greeting = """
  _____ _____ ____  _   _   ________   _________ _____            _____ _______ ____  _____  
 |_   _/ ____/ __ \| \ | | |  ____\ \ / /__   __|  __ \     /\   / ____|__   __/ __ \|  __ \ 
   | || |   | |  | |  \| | | |__   \ V /   | |  | |__) |   /  \ | |       | | | |  | | |__) |
   | || |   | |  | | . ` | |  __|   > <    | |  |  _  /   / /\ \| |       | | | |  | |  _  / 
  _| || |___| |__| | |\  | | |____ / . \   | |  | | \ \  / ____ \ |____   | | | |__| | | \ \ 
 |_____\_____\____/|_| \_| |______/_/ \_\  |_|  |_|  \_\/_/    \_\_____|  |_|  \____/|_|  \_\

                                                                                             
 Extracts icons of the desired width and height from the executables in a directory
 if there are no icons of such size, no icons will be extracted

 To extract all icons and bitmaps, specify width and height as 0    
 The script loads bin/icon_extractor.dll as it's much easier and faster to operate with native ole automation functions

 Usage: icon_extractor.py <path_to_files> <desired_width|0> <desired_height|0>   
 Examples: 
    icon_extractor.py path/to/files 32 64 - will extract all icons of the size 32x32 (height is doubled when it comes to resources, apparently)
    icon_extractor.py path/to/files 0 0 - will extract all icons
"""                        


hDll = None

def drop_from(full_path, data, width, height):
    # Find a good name that is not used
    dropid = 0
    name = ''
    short = ''
    display = ''
    while True:
        short = r'%d.%dx%d.dropped.ico' % (dropid, width, height)
        display = r'%s.%s' % (os.path.basename(full_path), short)
        name = r'%s.%s' % (full_path, short)
        if not os.path.exists(name):
            break
        dropid += 1
    # Load the library and call the drop function
    try:
        arr_type = ctypes.c_byte * len(data)
        arr = arr_type(*bytearray(data))
        sz = ctypes.c_uint32(len(data))
        res = hDll.SaveIconRes(arr, sz, name.encode('utf-8'))
        if res == 1:
            print('\t[+] Saved %s' % display)
            return True
        return False
    except Exception as e:
        print(repr(e))
        print('\t[-] There has been an error loading the dll and calling the function')
    return False


def process_file(full_path, width, height):
    pe = None
    try:
        pe = pefile.PE(full_path)
    except:
        print('\t[-] File %s is not a valid PE' % full_path)
        raise

    offset = 0x0
    size = 0x0
    for rsrc in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        for entry in rsrc.directory.entries:
            if entry.name is None:
                offset = entry.directory.entries[0].data.struct.OffsetToData
                size = entry.directory.entries[0].data.struct.Size
                data = pe.get_memory_mapped_image()[offset:offset+size]
                # BMP Image resource
                first = data[0]
                if isinstance(first, str):
                    first = ord(first)
                if first == 0x28:
                    try:
                        im = Image.open(io.BytesIO(data))
                        if width == 0 or height == 0 or im.size == (width, height):
                            drop_from(full_path, data, im.size[0], im.size[1])
                    except Exception as e:
                        print(repr(e))
                        print('\t[-] Failed for %s, entry: %d' % (full_path, entry.id))
                        raise


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(greeting)
        exit(0)

    hDll = ctypes.cdll.LoadLibrary('bin/icon_extractor.dll')
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    for name in os.listdir(sys.argv[1]):
        try:
            full = os.path.join(sys.argv[1], name)
            print('[+] %s' % name)
            process_file(full, width, height)
        except Exception as e:
            print('\tFailed to extract for %s' % name)
