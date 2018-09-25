# -*- coding: utf-8 -*-
import os
import json
import re
import six, os
from zhconv import convert_for_mw


def get_all_subdir_from_dir(path_dir='.'):
     # 遍历文件夹，输出文件及子文件夹内文件
    subdir = []
    if os.path.exists(path_dir):
        path_dir = os.path.abspath(path_dir)
        for i in os.listdir(path_dir):
            if re.match('^\\.',i):
                continue
            path_i = os.path.join(path_dir, i)
            if os.path.isdir(path_i):
                subdir.append(path_i)
    return subdir


def get_unpress_json_files(dir='.'):
    list_dir = os.listdir(dir)
    print(list_dir)

    res = []
    for item in list_dir:
        if '.json' in item and 'res_' not in item:
            print(item)
            if '.' !=dir:
                item = os.path.join(dir, item)
            res.append(item)
    return res

def get_traditional_press_files(dir='.'):
    list_dir = os.listdir(dir)
    print(list_dir)

    res = []
    for item in list_dir:
        if '.json' in item and 'res_' in item:
            print(item)
            if '.' !=dir:
                item = os.path.join(dir, item)
            res.append(item)
    return res 


def trans(file_path):
    out_path = os.path.join(os.path.dirname(file_path),'final_'+os.path.basename(file_path))
    with open(out_path, 'w', encoding='utf-8') as out_file, open(file_path, 'r', encoding='utf-8') as raw_file:
        for line in raw_file:
            content = convert_for_mw(line, 'zh-cn')
            out_file.write(content)

def main():
    all_subdir = get_all_subdir_from_dir()

    for subdir in all_subdir:
        #json文件压缩处理
        json_list = get_unpress_json_files(subdir)
        for json_file in json_list:
            out_path = os.path.join(os.path.dirname(json_file),'res_'+os.path.basename(json_file))
            with open( json_file , encoding='utf-8') as f, open(out_path , 'w', encoding='utf-8') as out:
                json_array = json.load(f)
                print(json_array)
                json.dump(json_array, out, ensure_ascii=False)
                out.write('\r')
        
        #json文件内容繁体转换成简体
        res_file = get_traditional_press_files(subdir)
        for item in res_file:
            trans(item)

if __name__ == "__main__":
    main()