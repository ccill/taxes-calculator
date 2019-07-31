#!/usr/bin/env python3
import sys
list1=sys.argv[1:]
insurance_tax=0.165

def get_salary(list1):
	dict1={}
	for i in list1:
		x,y=i.split(':')
		if y.isdigit():
			dict1[x]=int(y)
		else:
			print('Parameter Error')
			exit()
	return dict1

def tax(salary):
	taxable_income=salary-salary*insurance_tax-5000
	if taxable_income<=0:
		return 0
	elif taxable_income<=3000:
		return taxable_income*0.03-0
	elif taxable_income<=12000:
		return taxable_income*0.1-210
	elif taxable_income<=25000:
		return taxable_income*0.2-1410
	elif taxable_income<=35000:
		return taxable_income*0.25-2660
	elif taxable_income<=55000:
		return taxable_income*0.3-4410
	elif taxable_income<=80000:
		return taxable_income*0.35-7160
	elif taxable_income>80000:
		return taxable_income*0.45-15160
		
if __name__=='__main__':
	try:
		dict1=get_salary(list1)
		for k in dict1:
			last_salary=dict1[k]-dict1[k]*insurance_tax-tax(dict1[k])
			print('{}:{:.2f}'.format(k,last_salary))
	except:
		print('Parameter Error')
		
	

