import numpy as np
import pandas as pd
import time
import requests
import re

p1 = r'<tr.+?ter">.+?(\d{4}-\d{2}-\d{2}).+?</div.+?ter">.+?([\d.]+)</div.+?ter">.+?([\d.]+)</div.+?ter">.+?([\d.]+)</div.+?ter">.+?([\d.]+)</div.+?ter">.+?([\d.]+)</div.+?ter">.+?([\d.]+)</div></td>.+?</tr>'
fw = open('6.3/600618第二题结果.csv', 'w')
data_path = 'Data_600618/'
for nian in range(1999, 2019):
    for jidu in range(1, 5):
        with open(data_path + 'DataHTML_600618_Year_' + str(nian) + '_Jidu_' + str(jidu) + '.txt', 'r', encoding='utf-8') as file:
            html = file.read()
            match = re.findall(p1, html, re.S)
            if match:
                for line in match:
                    fw.write('{:s}, {:s}, {:s}, {:s}, {:s}, {:s}, {:s}\n'.format(line[0], line[1], line[2], line[3],
                                                                                 line[4], line[5], line[6]))
fw.close()

