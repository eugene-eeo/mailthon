from sys import version_info

if version_info[0] == 3:
    unicode = str
    bytes_type = bytes
else:
    unicode = lambda k: k.decode('utf8')
    bytes_type = str
