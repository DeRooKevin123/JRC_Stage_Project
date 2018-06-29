# Importing libraries needed
import sys
import csv
import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from datetime import datetime


def arguments():
    # Creating parameters to insert and plot a specified graph
    parser = argparse.ArgumentParser(usage='-f [] -d [] -m [] -s [] -e [] -a [] -o []')
    
    parser.add_argument("-f", "--filename", help="Filename. Path to and with your file name without dataformat", required=True)
    parser.add_argument("-d", "--dataformat", choices=['nc', 'tss'], help="Dataformat. Choose 'nc' for NetCDF or 'tss' for Timestep files", required=True)
    parser.add_argument("-m", "--mask", type=int, nargs="+", help="Mask. Either 1 (single point) or 2 points (topleft, bottomright)", required=False)
    parser.add_argument("-s", "--start_date", help="Start date. Usage: day/month/year", required=True)
    parser.add_argument("-e", "--end_date", help="End date. Usage: day/month/year", required=True)
    parser.add_argument("-a", "--aggregation", choices=['yes', 'no'], help="Yearly Aggregation. Choose 'yes' or 'no' to see every year's graph in a single one", required=True)
    parser.add_argument("-o", "--outfile", help="Outfile. Choose a name for the output file", required=True)
    parser.add_argument("-i", "--stationid", help="Station ID. Choose a station by giving its number", required=False)
    
    
    args = parser.parse_args()
    if args.dataformat=='nc' and args.stationid:
        sys.exit("Dataformat ['nc'] and Station ID can't go together!")
    elif args.dataformat=='tss' and not args.stationid:
        sys.exit("Dataformat ['tss'] requires a Station ID!")
        
    return args

    
def print_arguments(args):
    # Printing the values entered by the user
    print "X--------------------------------------------X"
    print ("(Filename)             You entered:  " + str(args.filename))
    print ("(Dataformat)           You entered:  " + str(args.dataformat))
    print ("(Mask)                 You entered:  " + str(args.mask))
    print ("(Start Date)           You entered:  " + str(args.start_date))
    print ("(End Date)             You entered:  " + str(args.end_date))
    print ("(Yearly Aggregation)   You entered:  " + str(args.aggregation))
    print ("(Outfile)              You entered:  " + str(args.outfile))
    print "X--------------------------------------------X"


def define_mask(mask, x, y):
    # Calculating all variables needed for the mask
    res = {'x1': None, 'y1': None, 'x2': None, 'y2': None}
    delta_x = x[1] - x[0]
    delta_y = y[0] - y[1]
    if mask:
        if len(mask) == 4:
            print "You selected a bounding box mask"
            res['x1'] = mask[0]
            res['y1'] = mask[1]
            res['x2'] = mask[2]
            res['y2'] = mask[3]
            res['min_x1'] = int(round((res['x1'] - x[0]) / delta_x))
            res['min_y1'] = int(round((y[0] - res['y1']) / delta_y))
            res['min_x2'] = int(round((res['x2'] - x[0]) / delta_x))
            res['min_y2'] = int(round((y[0] - res['y2']) / delta_y))
        elif len(mask) == 2:
            print "You selected a single point filter"
            res['x1'] = mask[0]
            res['y1'] = mask[1]
            res['min_x'] = int(round((res['x1'] - x[0]) / delta_x))
            res['min_y'] = int(round((y[0] - res['y1']) / delta_y))
        else:
            sys.exit("ERROR: Mask usage: 'x1' 'y1' 'x2' 'y2'")
    print res
    return res


def process_nc(args):
    # Creating a dataset for the file
    file_path = (args.filename + "." + args.dataformat)
    dataframe = Dataset(file_path)
    
    if args.aggregation=='yes' and not args.mask:
        sys.exit("ERROR: Aggregation ['yes'] needs Mask")
        
    # Setting up the dataframe
    x = dataframe["x"]
    y = dataframe["y"]
    dis = dataframe["dis"]
    mask = define_mask(args.mask, x, y)
    delta_x = x[1] - x[0]
    delta_y = y[0] - y[1]

    # Defining the start and end date
    date_format = "%d/%m/%Y"
    date0 = datetime.strptime('1/1/1990', date_format)
    date1 = datetime.strptime(args.start_date, date_format)
    date2 = datetime.strptime(args.end_date, date_format)

    # Checking if 'aggregation' is 'yes'
    if args.aggregation=='yes' and args.mask:
        
        # Getting the timeline from the start date to the end date
        first_year = date1.year
        last_year = date2.year
        date_begin_difference = date1 - date0
        date_end_difference = date2 - date0
        date_begin = date_begin_difference.days
        date_end = date_end_difference.days
        
        counter = 1
        ra = 0
        ylist = list()
        df_list = list()
        df_year = list()
        
        # Appending the years/days to a list, keeping leap years in mind
        for year in xrange(first_year, last_year + 1):
            counter += 366 if year % 4 == 0 else 365
            ra = 366 if year % 4 == 0 else 365
            ylist += [year for b in xrange(ra)]
                
            # Plotting the graphs according to the mask
            if len(args.mask) == 2:
                df_y = dis[counter - ra:counter, mask['min_y'], mask['min_x']]
                plt.plot(df_y)
            elif len(args.mask) == 4:  
                dfm = dis[counter - ra:counter, int(round(mask['y2'] / delta_y)):int(round(mask['y1'] / delta_y)), int(round(mask['x1'] / delta_x)):int(round(mask['x2'] / delta_x))].mean(axis=0)
                df_list.append(dfm)
                df_year.append(year)
       
        # If mask length = 2, plot violin graph according to data. If mask length = 4, create an outfile with a piece of a map according to the two points
        if len(args.mask) == 2:
            plt.show()
            df_y = dis[date_begin:date_end, mask['min_y'], mask['min_x']]
            df_x = pd.DataFrame(ylist, columns=["year"])
            df_x = df_x["year"][date_begin:date_end]
            sns.violinplot(x=df_x, y=df_y)
            plt.show()
        
        elif len(args.mask) == 4:
            dsout = Dataset(args.outfile+".nc", "w", format="NETCDF4_CLASSIC")
            lat = dsout.createDimension('y', ((mask['y1'] - mask['y2']) / delta_y))
            lon = dsout.createDimension('x', ((mask['x2'] - mask['x1']) / delta_x))
            time = dsout.createDimension('time', None)
        
            times = dsout.createVariable('time', np.float64, ('time',))
            latitudes = dsout.createVariable('y', np.float32,('y',))
            longitudes = dsout.createVariable('x', np.float32,('x',))
            
            diss = dsout.createVariable('dis', np.float32, ('time', 'y', 'x',))
            latitudes[:]=list(range(int(mask['y1']), int(mask['y2']), int(-delta_y)))
            longitudes[:]=list(range(int(mask['x1']), int(mask['x2']), int(delta_x)))
            
            for year in range(len(df_year)):
                diss[year,:,:] = df_list[year]
                
            # Closing the output file
            dsout.close()
        

def process_tss(args):
    
    # Counting lines and columns in the file
    file_path = (args.filename + "." + args.dataformat)
    with open(file_path) as f:
        count = sum(1 for line in f)
        f.seek(0)
        reader = csv.reader(f, delimiter='\t', skipinitialspace=True)
        first_row = next(reader)

        len_columns = len(first_row)
    
        
    # Reading the file and appending the columns to a dataframe
    df = pd.read_csv(file_path, header=None, delim_whitespace=True, skiprows=820)
    col = list()
    
    for i in range(len_columns):
        col.append(i)
    df.columns=col
    df = df[1:]
    df["timestamp"]=pd.date_range(start='1/1/1990', periods=count)
    lyear = list()
    for date in pd.date_range(start='1/1/1990', periods=count):
        lyear.append( )
    df["year"]=lyear
    
    
def main():
    
    # Calling all functions to operate and do the magic
    args = arguments()
    dataformat = args.dataformat    
    print_arguments(args)    
    
    # Plotting a graph for the file in two ways; one for a NetCDF file, the other for a '.tss' file.
    if dataformat == 'nc':
        process_nc(args)
    else:
        process_tss(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
    
