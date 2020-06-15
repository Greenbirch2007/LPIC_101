1import urllib
 2from io import BytesIO
 3
 4from pdfminer.pdfparser import PDFParser
 5from pdfminer.pdfdocument import PDFDocument
 6from pdfminer.pdfpage import PDFPage
 7from pdfminer.pdfpage import PDFTextExtractionNotAllowed
 8from pdfminer.pdfinterp import PDFResourceManager
 9from pdfminer.pdfinterp import PDFPageInterpreter
10from pdfminer.pdfdevice import PDFDevice
11from pdfminer.layout import *
12from pdfminer.converter import PDFPageAggregator
13from urllib.request import Request
14from urllib.request import urlopen
15
16# 对线上pdf文件进行读取和写入到txt文件当中
17
18
19# 定义解析函数
20def OnlinePdfToTxt(dataIo,new_path):
21    # 创建一个文档分析器
22    parser = PDFParser(dataIo)
23    # 创建一个PDF文档对象存储文档结构
24    document = PDFDocument(parser)
25    # 判断文件是否允许文本提取
26    if not document.is_extractable:
27        raise PDFTextExtractionNotAllowed
28    else:
29        # 创建一个PDF资源管理器对象来存储资源
30        resmag =PDFResourceManager()
31        # 设定参数进行分析
32        laparams=LAParams()
33        # 创建一个PDF设备对象
34        # device=PDFDevice(resmag )
35        device=PDFPageAggregator(resmag ,laparams=laparams)
36        # 创建一个PDF解释器对象
37        interpreter=PDFPageInterpreter(resmag ,device)
38        # 处理每一页
39        for page in PDFPage.create_pages(document):
40            interpreter.process_page(page)
41            # 接受该页面的LTPage对象
42            layout=device.get_result()
43            for y in layout:
44                try:
45                    if(isinstance(y,LTTextBoxHorizontal)):
46                        with open('%s'%(new_path),'a',encoding="utf-8") as f:
47                            f.write(y.get_text()+'\n')
48                            print("读入成功！")
49                except:
50                    print("读入失败!")
51
52# 获取文件的路径
53url = "file:///I:/Python3.6/patest/PdfTest/pdftestto.pdf"
54html = urllib.request.urlopen(urllib.request.Request(url)).read()
55dataIo = BytesIO(html)
56OnlinePdfToTxt(dataIo,'d.txt')





import pdfplumber
 2import re
 3import json
 4
 5path = 'I:\Python3.6\patest\PdfTest\\numberTest 1.pdf'  # 待读取的PDF文件的路径
 6pdf = pdfplumber.open(path)
 7
 8for page in pdf.pages:
 9    # print(page.extract_text())
10    for pdf_table in page.extract_tables():
11        table = []
12        cells = []
13        for row in pdf_table:
14            if not any(row):
15                # 如果一行全为空，则视为一条记录结束
16                if any(cells):
17                    table.append(cells)
18                    cells = []
19            elif all(row):
20                # 如果一行全不为空，则本条为新行，上一条结束
21                if any(cells):
22                    table.append(cells)
23                    cells = []
24                table.append(row)
25            else:
26                if len(cells) == 0:
27                    cells = row
28                else:
29                    for i in range(len(row)):
30                        if row[i] is not None:
31                            cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
32        for row in table:
33            data =[re.sub('\s+', '', cell) if cell is not None else None for cell in row]
34            data_list =list(enumerate(data))
35            # print(json.dumps(data_list, indent=2, ensure_ascii=False))
36            with open('I:\Python3.6\patest\PdfTest\\numberTest1.json','a',encoding="utf-8") as file:   # json文件的存放位置
37                file.write(json.dumps(data_list, ensure_ascii=False))
38pdf.close()



1import camelot
 2
 3# 从本地的PDF文件中提取表格数据，pages为pdf的页数，默认为第一页
 4tables = camelot.read_pdf('I:\Python3.6\patest\PdfTest\special.pdf', pages='1', flavor='stream')
 5
 6# 表格信息
 7print(tables)
 8print(tables[0])
 9# 表格数据
10print(tables[0].data)


1# 从本地的PDF文件中提取表格数据，pages为pdf的页数，默认为第一页
2tables = camelot.read_pdf('I:\Python3.6\patest\PdfTest\special.pdf', pages='1', flavor='stream')
3
4tables[0].to_csv('special1.csv')


1import camelot
 2
 3
 4# 从PDF文件中提取表格
 5tables = camelot.read_pdf('I:\Python3.6\patest\PdfTest\\numberTest 1.pdf', pages='1', flavor='stream',strip_text=' .\n')
 6
 7# 绘制PDF文档的坐标，定位表格所在的位置
 8plt= camelot.plot(tables[0],kind='text')
 9plt.show()
10
11# 绘制PDF文档的坐标，定位表格所在的位置
12table_df = tables[0].df
13
14print(table_df.head(n=80))