# coding=utf-8


import xlrd
import pandas as pd
import os

# 创建的目录

def mkdir():
    loc_getcwd = os.getcwd()
    path = "{0}/Outputs".format(loc_getcwd)
    #如果存在目录先删除，如果不存在就创建
    if os.path.exists(path):
        os.removedirs(path)
    else:
        os.mkdir(path)
    return path

def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        dataFile.append(table.row_values(rowNum))
       # # if 去掉表头
       # if rowNum > 0:


    return dataFile


if __name__ == '__main__':
    loc_getcwd = os.getcwd()
    # excelFile = '{0}\a.xlsx'.format(loc_getcwd) # windows and linux！
    excelFile = '{0}/s.xlsx'.format(loc_getcwd) # 处理了文件属于当前目录下！
    ln = mkdir()
    f_list=[]

    # 先把单表的名字容器给弄出来
    names_list = set()
    for item in read_xlrd(excelFile=excelFile):
        names_list.add(item[0])
        item_l = []
        for  one_item in item:
            if one_item != '':
                item_l.append(one_item)
            else:
                pass
        item_l.append(one_item)
        first_item = item_l[:-1]
        last_item = item_l[-1:]
        f_list.append((first_item[:-1], first_item[-1:]))

    columns = ["表名", "字段名"]

    allC_dt = pd.DataFrame(f_list, columns=columns)
    allC_dt.to_excel("{0}/de.xlsx".format(ln), index=0)




    #     strNums = [str(x) for x in last_item]
    #     l_last = ",".join(strNums)
    #
    #



    # full_items = read_xlrd(excelFile=excelFile)
    # for single_name  in names_list:
    #     one_list = []
    #     one_list.append(single_name)
    #     for item in full_items:
    #         if single_name == item[0]:
    #             one_list.append(item[1])
    #         else:
    #             pass

