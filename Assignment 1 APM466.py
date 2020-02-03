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
        
def spot_rates(bonds):
    spot_rates = []
    for x in range(1,10):
        spots = []
        for i in range(2, 10):
            exponent = (1 / (i * 0.5))
            new_spot = ((100 / bonds[12 * i - x]) ** exponent) - 1
            spots.append(new_spot)
        spot_rates.append(spots)
    return spot_rates

def forward_rates(bonds):
    forward_rates = []
    spots = spot_rates(bonds)
    for i in range(1,10):
        forwards = []
        #index from 0 to 4 since we're using spot rates, which start at year 1
        for x in range(0,4):
            new_forward = ((1 + spots[i-1][2*x])**(x+1)) / ((1+spots[i-1][0])**1) - 1
            forwards.append(new_forward)
        forward_rates.append(forwards)
    return forward_rates
            
def cov_matrix_yield(bonds):
    cov_matrix_yield = []
    yields = compile_days(10)
    for i in range(1,5):
        matrix_yields = []
        for x in range(1,5):
            matrix_yields.append(round(numpy.log(yields[i][x+1]/yields[i][x]),4))
        cov_matrix_yield.append(matrix_yields)
    return cov_matrix_yield

def cov_matrix_forward(bonds):
    cov_matrix_forward = []
    forwards = forward_rates(bonds)
    for i in range(0,2):
        matrix_forwards = []
        #can only index over 1 to 3, since the entire vector of forward rates is 
        #only from 0 to 3, but at 0 for each vector, the value is 0, and we cannot
        #divide by 0, we omit 1yt-1yr
        for x in range(1,3):
            matrix_forwards.append(round(numpy.log(abs(forwards[i][x+1]/forwards[i][x])),4))
        cov_matrix_forward.append(matrix_forwards)
    return cov_matrix_forward
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
            x = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5] 
            fig = pyplot.figure()
            ax = pyplot.subplot(111)  
            pyplot.ylabel('Yields')
            pyplot.xlabel('Time (Years)')              
            for i in range(0,9):
                y = graph_data[i]
                ax.plot(x,y, label = 'day {}'.format(i + 1))
                ax.legend()
            pyplot.show()
            pyplot.savefig('yield_curve.png', dpi = 600)
            
            spot_graph_data = spot_rates(bonds)
            fig = pyplot.figure()
            ax = pyplot.subplot(111)
            pyplot.ylabel('Spot Rates')
            pyplot.xlabel('Time to Maturity (Years)')
            x = [1.5,2,2.5,3,3.5,4,4.5,5]
            for i in range(0,9):
                y = spot_graph_data[i]
                ax.plot(x,y, label = 'day {}'.format(i+1))
                ax.legend()
            pyplot.show()
            pyplot.savefig('spot_curve.png', dpi = 600)
            
            forward_graph_data = forward_rates(bonds)
            fig = pyplot.figure()
            ax = pyplot.subplot(111)
            pyplot.ylabel('Forward Rates')
            pyplot.xlabel('Rate Term (starting at 1 year)')
            x = [1,2,3,4]
            for i in range(0,9):
                y = forward_graph_data[i]
                ax.plot(x,y, label = 'day {}'.format(i+1))
                ax.legend()
            pyplot.show()
            pyplot.savefig('forward_curve.png', dpi = 600)
            
            