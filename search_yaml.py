#!/usr/bin/env python3

import os
import argparse
import time
import yaml
from pprint import pprint
import json
import re

class FileTreeMaker(object):
    def _recurse(self, parent_path, file_list,output_buf, level):
        if len(file_list) == 0 \
            or (self.max_level != -1 and self.max_level <= level):
            return
        else:
            file_list.sort(key=lambda f: os.path.isfile(os.path.join(parent_path, f)))
            for idx, sub_path in enumerate(file_list):
                if any(exclude_name in sub_path for exclude_name in self.exn):
                    continue

                full_path = os.path.join(parent_path, sub_path)
                idc = "┣━"
                if idx == len(file_list) - 1:
                    idc = "┗━"

                if os.path.isdir(full_path) and sub_path not in self.exf:
                    self._recurse(full_path, os.listdir(full_path),output_buf, level + 1)
                elif os.path.isfile(full_path):
                    if full_path.endswith('.yml'):
                        disk = os.getcwd()
                        full_path = full_path.replace('.\\','\\')
                        full_path = disk + full_path
                        output_buf.append(full_path)
                        
    def make(self, args):
        self.root = args.root
        self.exf = args.exclude_folder
        self.exn = args.exclude_name
        self.max_level = args.max_level

        print("CurrentDir :%s" % os.getcwd())

        buf = []
        path_parts = self.root.rsplit(os.path.sep, 1)
        buf.append("[%s]" % (path_parts[-1],))
        self._recurse(self.root, os.listdir(self.root),buf, 0)
        buf.pop(0)
        return buf
def parse_json(yaml_list):
    Full_Path_T1127_List = []
    for yaml_path in yaml_list:
        try:
            with open(yaml_path,encoding="utf-8") as filename:
                f_content = filename.read()
                f_content = f_content.replace('---\n','')
                data = yaml.load(f_content, Loader=yaml.CLoader)
                for propertys in data:
                    if 'Full_Path' in data:
                        Commands = data['Commands']
                        for property_sub in Commands:
                            regex = re.compile(r'T1127')
                            T1127 = property_sub['MitreID']
                            if regex.search(T1127) and property_sub['Privileges'] == 'User' :
                                Full_Path_T1127_List.append(data['Full_Path'][0]['Path'])
                    

                #pprint(data)
        except Exception as e:
            print(e)
            continue
    return list(set(Full_Path_T1127_List))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", help="root of file tree", default=".")
    parser.add_argument("-o", "--output", help="output file name", default="")
    parser.add_argument("-xf", "--exclude_folder", nargs='*', help="exclude folder", default=[])
    parser.add_argument("-xn", "--exclude_name", nargs='*', help="exclude name", default=[])
    parser.add_argument("-m", "--max_level", help="max level",
                        type=int, default=-1)
    args = parser.parse_args()
    
    yaml_lists = FileTreeMaker().make(args)
    T1127_list = parse_json(yaml_lists)
    for i in T1127_list:
        print(i)
