#!/usr/bin/env python3
import csv   #????csv??
import sys
import time
from collections import namedtuple
from multiprocessing import Queue,Process



tax_start_point=5000
income_tax=namedtuple('income_tax',['start_point','rate','quick'])
income_tax_table=[
            income_tax(80000,0.45,15160),
            income_tax(55000, 0.35, 7160),
            income_tax(35000, 0.30, 4410),
            income_tax(25000, 0.20, 2660),
            income_tax(12000, 0.45, 1410),
            income_tax(3000, 0.10, 210),
            income_tax(0, 0.03, 0)
        ]


#????????
class Args:
    def __init__(self):
        self.args=sys.argv[1:]

    def get_file_path(self,option):
        try:  #???????-c?
            option_index=self.args.index(option)
            file_path = self.args[option_index + 1]
            return file_path
        except:
            print('Parameter Error')
            exit()

    @property
    def config_path(self):
        return self.get_file_path('-c')

    @property
    def user_path(self):
        return self.get_file_path('-d')


    @property
    def export_path(self):
        return self.get_file_path('-o')

#?????????????????????
args=Args()

#?????
class Config:
    def __init__(self):
        self.config=self._read_config()

    def _read_config(self):
        config={}
        with open(args.config_path) as f:
            for line in f:
                k,v=line.strip().split('=')
                try:  #?float??????
                    config[k.strip()] = float(v.strip())
                except:
                    print('Parameter Error')
                    exit()
        return config

    def _get_config(self,key):
        try:
            return self.config[key]
        except KeyError:
            print('Config Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        return sum([self._get_config('YangLao'),
                    self._get_config('YiLiao'),
                    self._get_config('ShiYe'),
                    self._get_config('GongShang'),
                    self._get_config('ShengYu'),
                    self._get_config('GongJiJin')])

#???????????????????
config=Config()


#?????
class UserData(Process):
    def __init__(self,userdata_queue):
        super().__init__()
        #self.userdata_list=self._read_users_data()
        self.userdata_queue=userdata_queue

    def _read_users_data(self):
        userdata_list=[]
        with open(args.user_path) as f:
            for i in csv.reader(f):
                employee_id,income_str=i[0],i[1]
                try:
                    income=int(income_str)
                except ValueError:
                    print('Parameter Error')
                    exit()
                userdata_list.append((employee_id,income))

        return userdata_list

    #???property
    # def get_userdata_list(self):
    #     return self.userdata_list

    def run(self):
        for item in self._read_users_data():
            self.userdata_queue.put(item)




#???????
class IncomeTaxCalculator(Process):

    def __init__(self,userdata_queue,export_queue):
        super().__init__()
        self.userdata_queue=userdata_queue
        self.export_queue=export_queue
        #self.userdata_list=userdata_list

    #?????????Income???????????
    @classmethod
    def SheBao(cls,income):
        if income<config.social_insurance_baseline_low:
            shebao_part=config['JiShuL']*shebao_rate
            return shebao_part
        elif income<config.social_insurance_baseline_high:
            shebao_part=income*config.social_insurance_total_rate
            return shebao_part
        else:
            shebao_part=config.social_insurance_baseline_high*config.social_insurance_total_rate
            return shebao_part

    @classmethod
    def tax_part_and_remain(cls,income):
        social_insurance_money=cls.SheBao(income)
        taxable_part=income-social_insurance_money-tax_start_point
        #print(social_insurance_money,taxable_part)

        for item in income_tax_table:
            if taxable_part>item.start_point:
                #print(taxable_part,item.start_point)
                tax=taxable_part*item.rate-item.quick
                #print(tax)
                return '{:.2f}'.format(tax) , '{:.2f}'.format(income-social_insurance_money-tax)
        return '0.00','{:.2f}'.format(income-social_insurance_money)

    #?????????????
    #?????????????????????
    # def calc_for_all_userdata(self):
    #     result=[]
    #     #for emloyee_id,income in self.userdata_list.get_userdata_list():
    #         social_insurance_money='{:.2f}'.format(self.SheBao(income))
    #         tax,remain_money=self.tax_part_and_remain(income)
    #         result.append([emloyee_id,income,social_insurance_money,tax,remain_money])
    #     return result

    #???????????
    def calc(self,emloyee_id,income):
        social_insurance_money = '{:.2f}'.format(self.SheBao(income))
        tax, remain_money = self.tax_part_and_remain(income)
        return [emloyee_id,income,social_insurance_money,tax,remain_money]

    def run(self):
        while True:
            try:
                emloyee_id, income=self.userdata_queue.get(timeout=1)
            except:
                return
            result=self.calc(emloyee_id,income)
            self.export_queue.put(result)

class Export(Process):
    def __init__(self,export_queue):
        super().__init__()
        self.export_queue=export_queue
        self.file=open(args.export_path,'w')
        self.writer=csv.writer(self.file)

        #??csv????
    # def export(self,result,default='csv'):
    #     #result=self.calc_for_all_userdata()
    #     with open(args.export_path,'w') as f:
    #         writer=csv.writer(f)
    #         writer.writerow(result)

    def run(self):
        while True:
            try:
                result=self.export_queue.get(timeout=1)

            except:
                self.file.close()
                return

            self.writer.writerow(result)


if __name__=='__main__':
    start=time.time()
    userdata_queue=Queue()
    export_queue=Queue()
    userdata=UserData(userdata_queue)
    income_calc=IncomeTaxCalculator(userdata_queue,export_queue)
    export=Export(export_queue)
    userdata.start()
    income_calc.start()
    export.start()
    userdata.join()
    income_calc.join()
    export.join()
    end=time.time()
    print('how long:{:.2f}s'.format(end-start))
