import numpy
import math
from typing import List, TextIO
from matplotlib import pyplot

def csv_to_list(csv):
    data = []
    for line in csv:
        data.append(float(line.strip().split(',')[0]))
    return data

def no_coupon_step(price, time):
    r = -numpy.log(price/100)/time
    return r 

def repeat_step(bonds, day):
    yields = []
    #since the order of bond prices is from newest to oldest, need to use 
    #12-day instead of 1+day to index over each days price for each bond
    yields.append(no_coupon_step(bonds[12 - day],1/12))
    for i in range(1,10):
        sum_cash_flows = 0
        for x in range(i):
            sum_cash_flows += 100 * bonds[1 + 12 * i] * math.exp(-yields[x]*(x * (0.5)))
        new_yield = (-numpy.log(bonds[i * 12 + 12 - day] - sum_cash_flows) + numpy.log(100))/(float(i) * 0.5)
        yields.append(new_yield)
        sum_cash_flows = 0
    return yields

def compile_days(days):
    all_yields = []
    for i in range(1,days+1):
        all_yields.append(repeat_step(bonds, i))
    return all_yields
        
    
if __name__ == '__main__':
    running = True
    while running:
        test = input("Press any key to read and compile data, or type quit")
        if test == "quit":
            running = False
        else:
            bond_file = open('bond_data1.csv')
            bonds = csv_to_list(bond_file)
            graph_data = compile_days(10)
            print(graph_data)
            x = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5] 
            fig = pyplot.figure()
            ax = pyplot.subplot(111)  
            pyplot.ylabel('Yields')
            pyplot.xlabel('Time (Years)')              
            for i in range(1,9):
                y = graph_data[i]
                ax.plot(x,y, label = 'day {}'.format(i))
                ax.legend()
            pyplot.show()
            pyplot.savefig('yield_curve.png', dpi = 600)
            