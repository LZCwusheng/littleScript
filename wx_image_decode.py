import os
import sys


def decode(dat_dir, out_dir, filename):
    """
    对图片的 dat 加密文件进行解密
    params:
        dat_dir  dat 文件的目录路径
        out_dir  解密文件的存储路径
        filename 文件名
    """
    
    ext_value = {"png": [137, 80], "jpg": [255, 216], "gif": [71, 73]}

    dat_path = dat_dir + "/" + filename
    dat_handler = open(dat_path, "rb")
    dat_data = dat_handler.read()
    
    # 获取密钥
    ext = ''
    key = 0
    for k in ext_value:
        b1 = dat_data[0]
        b2 = dat_data[1]

        if b1 ^ ext_value[k][0] == b2 ^ ext_value[k][1]:
            ext = k                            # ext 图片后缀名
            key = b1 ^ ext_value[k][0]         # key 是密钥
            break
    
    basename = os.path.basename(filename)
    image_path = out_dir + "/" + basename + "." + ext
    image_handler = open(image_path, 'wb')
    image_data = []
    # 解密文件
    for b in dat_data:
        d = b ^ key
        image_data.append(d)
    # 保存原始数据，输出到文件中
    image_handler.write(bytes(image_data))

    image_handler.close()
    dat_handler.close()

usage = '''
usage: python wx_image_decoe.py [-d <dat_dir>] [-o <output_dir>]
相关链接：https://wenku.baidu.com/view/7702386ce75c3b3567ec102de2bd960590c6d9c5.html
params:
    -d  dat 的目录路径，默认是当前所在路径
    -o  解密文件的存储路径，默认是当前所在路径
'''

print(usage)

dat_dir = "."
out_dir = "."

if len(sys.argv) == 3:
    if sys.argv[1] == "-d":
        dat_dir = sys.argv[2]
    elif sys.argv[1] == "-o":
        out_dir = sys.argv[2] 
elif len(sys.argv) == 5:
    if sys.argv[1] == "-d":
        dat_dir = sys.argv[2]
        out_dir = sys.argv[4]
    elif sys.argv[1] == "-o":
        dat_dir = sys.argv[4]
        out_dir = sys.argv[2] 

dat_dir.replace('\\', '/')
out_dir.replace('\\', '/')
if os.path.exists(out_dir) is False:
    os.mkdir(out_dir)

files = os.listdir(dat_dir)
for filename in files:
    decode(dat_dir, out_dir, filename)



