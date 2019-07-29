#! /usr/bin/env python3
import sys
try:
	salary=int(sys.argv[1])
	taxable_income=salary-5000
	if taxable_income<=3000:
		taxes=taxable_income*0.03-0
		print('{:.2f}'.format(taxes))
	elif 3000<taxable_income<=12000:
		taxes=taxable_income*0.1-210
		print('{:.2f}'.format(taxes))
	elif 12000<taxable_income<=25000:
		taxes=taxable_income*0.2-1410
		print('{:.2f}'.format(taxes))
	elif 25000<taxable_income<=35000:
		taxes=taxable_income*0.25-2660
		print('{:.2f}'.format(taxes))
	elif 35000<taxable_income<=55000:
		taxes=taxable_income*0.3-4410
		print('{:.2f}'.format(taxes))
	elif 55000<taxable_income<=80000:
		taxes=taxable_income*0.35-7160
		print('{:.2f}'.format(taxes))
	elif taxable_income>80000:
		taxes=taxable_income*0.45-15160
		print('{:.2f}'.format(taxes))

except:
	print('Parameter Error')

