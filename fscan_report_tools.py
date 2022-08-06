'''
针对 fscan 的 report 根据 ip 做数据分类的处理，并提供如下功能：
1.输出：输出分类结果，如果指定 ip，就仅输出对应 ip 的结果
2.保存：保存分类结果，如果指定 ip，就仅保存对应 ip 的结果
3.nmap扫描：扫描开放端口，如果指定 ip，就仅扫描对应 ip 的开放端口（需要安装 nmap）
'''
import os
import argparse
import re

example = "examples: python fscan_report_tools.py result.txt -p -ip 123.123.123.123"

parser = argparse.ArgumentParser(description="fscan 报告处理脚本", epilog=example)
parser.add_argument("report_filename", help="fscan 报告的文件路径")
parser.add_argument("-ip", help="根据指定的 ip 从报告中提取相关的信息")
parser.add_argument("-p", "--print", action="store_true", help="输出对报告结果进行 ip 分类的信息")
parser.add_argument("-o", action="store_true", help="保存根据ip分类的结果（可用 -ip 指定 ip）")
parser.add_argument("-n", "--nmap", action="store_true", help="调用 nmap 对 fscan 扫描到的开放端口进行服务识别（可用 -ip 指定 ip）")
args = parser.parse_args()

# 键名是 ip，每个 ip 存储一个链表，存储报告中相关的信息
ip_data = {}

def sort():
    """根据 ip 对报告的数据进行分类"""
    handler = open(args.report_filename, 'r')
    pattern = re.compile(r"(\d{1,3}\.){3}\d{1,3}")

    line = handler.readline().rstrip()
    while line:
        
        ip = pattern.search(line).group(0)
        if line[-4:] == "open":

            if ip not in ip_data.keys():
                ip_data[ip] = []

            ip_data[ip].append(line)
            line = handler.readline().rstrip()

        elif line[:3] == "[*]":
            
            ip_data[ip].append(line)
            line = handler.readline().rstrip()

            while line[:3] != "[*]" and line != "":
                ip_data[ip].append(line)
                line = handler.readline().rstrip()
    

def s_print(ip=None):
    """输出分类结果"""
    if ip:
        keys = [ip]
    else:
        keys = ip_data.keys()

    for k in keys:
        print("========== " + k + " ==========")
        for v in ip_data[k]:
            print(v)
        print()


def save(ip=None):
    """保存分类结果"""
    out_dir = "ip_report"
    if os.path.exists(out_dir) is False:
        os.mkdir(out_dir)

    if ip:
        keys = [ip]
    else:
        keys = ip_data.keys()

    for ip in keys:
        with open(out_dir + '/' + ip + ".txt", 'w') as f:
            data = ""
            for d in ip_data[ip]:
                data += d + "\n"
            f.write(data)
    

def nmap_(ip=None):
    """调用 nmap 扫描"""
    nmap_report_dir = "nmap_report"
    if os.path.exists(nmap_report_dir) is False:
        os.mkdir(nmap_report_dir)

    if ip:
        targets = [ip]
    else:
        targets = ip_data.keys()

    for t in targets:
        ports = ""
        for v in ip_data[t]:
            if v[-4:] == "open":
                colon_i = v.index(':')
                space_i = v.index(' ')
                port = v[colon_i+1:space_i]
                ports += port + ','

        ports.rstrip(',')
        os.system("nmap -sS -sV -p " + ports + " -o " + nmap_report_dir + "/" + t + ".txt " + t)
        

if __name__ == "__main__":
    sort()

    p_flag = args.print
    o_flag = args.o
    nmap_flag = args.nmap
    ip = args.ip

    if p_flag is True:
        if ip:
            # 指定 ip 输出结果
            s_print(ip)
        else:
            # 输出全部 ip 的分类结果
            s_print()
    
    if o_flag is True:
        if ip:
            # 指定 ip 就只保存那个 ip 的结果
            save(ip)
        else:
            # 没指定 ip 就保存全部 ip 的结果
            save()
    
    if nmap_flag is True:
        if ip:
            # 指定 ip 就扫描那个 ip 开放的端口
            nmap_(ip)
        else:
            # 没指定 ip 就扫描全部 ip 开放的端口
            nmap_()
        
    


        
