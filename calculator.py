#!/usr/bin/env python3
import sys
import csv
from collections import namedtuple
import json
from decimal import Decimal

income_tax_quick_lookup_item=namedtuple('income_tax_quick_lookup_item',['start_point','tax_rate','quick_subtractor'])

class calculator:
    def __init__(self):
        self.dict_cfg={}
        self.salary=[]
        self.start_point=5000
        self.income_tax_quick_lookup_table=[
            income_tax_quick_lookup_item(80000,0.45,15160),
            income_tax_quick_lookup_item(55000, 0.35, 7160),
            income_tax_quick_lookup_item(35000, 0.30, 4410),
            income_tax_quick_lookup_item(25000, 0.25, 2660),
            income_tax_quick_lookup_item(12000, 0.20, 1410),
            income_tax_quick_lookup_item(3000, 0.10, 210),
            income_tax_quick_lookup_item(0, 0.03, 0)]

    def get_normail_data(self,file):
        with open(file) as f:
            for line in f:
                x,y=line.split('=')
                self.dict_cfg[x.strip()]=float(y.strip())
        SheBao=sum(self.dict_cfg.values())-self.dict_cfg['JiShuL']-self.dict_cfg['JiShuH']
        return SheBao

    def get_csv_data(self,file):
        with open(file) as f:
            data=csv.reader(f)
            for i in data:
                i[1]=int(i[1])
                self.salary.append(i)
        #return self.salary

    def get_shebao(self,SheBao):
        for i in self.salary:
            if i[1]<self.dict_cfg['JiShuL']:
                shebao=self.dict_cfg['JiShuL']*SheBao
            elif i[1]<self.dict_cfg['JiShuH']:
                shebao = i[1] * SheBao
            else:
                shebao = self.dict_cfg['JiShuH'] * SheBao
            i.append(shebao)

    def get_tax(self):
        for i in self.salary:
            should_tax=i[1]-i[2]-self.start_point

            if should_tax<0:
                tax=0
                i.append(tax)
            else:
                for item in self.income_tax_quick_lookup_table:
                    if should_tax>item.start_point:
                        tax=should_tax*item.tax_rate-item.quick_subtractor
                        i.append(tax)
                        break

    def get_final_salary(self):
        for i in self.salary:
            final_salary=i[1]-i[2]-i[3]
            i.append(final_salary)

    def decimal_(self):
        for i in self.salary:
            for j in range(len(i)-1):
                i[j+1]=str(Decimal(i[j+1]).quantize(Decimal('0.00')))

    def output_json_csv(self,file):

        with open(file,'w') as f:
            for data in self.salary:
                csv.writer(f).writerow(data)

if __name__=='__main__':
	try:
		test_cfg,user_csv,gongzi_csv=sys.argv[2],sys.argv[4],sys.argv[6]
		cal=calculator()
		SheBao=cal.get_normail_data(test_cfg)
		cal.get_csv_data(user_csv)
		cal.get_shebao(SheBao)
		cal.get_tax()
		cal.get_final_salary()
		cal.decimal_()
		cal.output_json_csv(gongzi_csv)
	except:
		print('ERROR')

