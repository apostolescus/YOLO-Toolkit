import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from datetime import datetime


cwd = os.getcwd()
class_dict = {}

def parse_arguments():
      parser = argparse.ArgumentParser()
      
      parser.add_argument('-d',help="Directory", dest="dir", nargs="+", required=True)
      parser.add_argument("--missing", help="Check fir missing pairs image - txt",action="store_true", dest="missing")
      parser.add_argument("--infos",help="Generates infos about files and classes",action="store_true", dest="infos")
      parser.add_argument("--empty",help="Check for empty files",action="store_true", dest="empty")
      parser.add_argument("-clfile", help="File containing names of the classes",dest="cl_file", default='', required=False, type=str)
      
      results = parser.parse_args()
      
      return results

def check_missing_pairs(dir_name):
    
    check_dict = []
    
    dir_path = os.path.join(cwd, dir_name)
    # train_path = os.path.join(dir_path,"train.txt")
    # test_path = os.path.join(dir_path,"test.txt")

    for pair in os.listdir(dir_path):
        
        if pair.endswith(".txt") or pair.endswith(".jpg"):
            pair_name = pair[:-4]
        elif pair.endswith(".jpeg"):
            pair_name = pair[:-5]
            
        if pair_name != "train" and pair_name != "test":
            if pair_name in check_dict:
                check_dict.remove(pair_name)
            else:
                check_dict.append(pair_name)
        
    if check_dict == []:
            return True
    else:
        return check_dict 
    
def add_to_dict(item):
    global class_dict
    
    if item in class_dict.keys():
        class_dict[item] += 1
    else:
        class_dict[item] = 0
        
def generate_ds_infos(dir_name):
    dir_path = os.path.join(cwd, dir_name)
    
    for item in os.listdir(dir_path):
        if item.endswith("txt") and item != "train.txt" and item != "test.txt":
            file_path = os.path.join(dir_path, item)
            f = open(file_path,"r")
            
            line = f.readline()
        
            cl_id = int(line.split()[0])
            add_to_dict(cl_id)
            
            while line:
                line = f.readline()
                if line != '':
                    cl_id = int(line.split()[0])
                    add_to_dict(cl_id)
            
            
    return True

def plot_diagram(min_step, max_step, cl_file):

    colors = []
    fig = plt.figure(figsize= (20,5))
    
    #legend
    
    red_patch = mpatches.Patch(color='red', label="<" +str(min_step) + " sau >"+ str(max_step))
    blue_patch = mpatches.Patch(color='blue', label=str(min_step) + " - " + str(max_step))
    

    names = ['class_id','numbers']
    formats = ['int','int']
    dtype = dict(names = names, formats = formats)
    array = np.array(list(class_dict.items()), dtype=dtype)
    sortedArr = np.sort(array)
    
    x = []
    y = []
    labels = []
    if cl_file != '':
        f = open(cl_file,"r")
        
        line = f.readline()
        labels.append(line)
        
        while line:
            line = f.readline()
            labels.append(line)
        labels.pop()

    for arr in sortedArr:
        x.append(str(arr[0]))
        
        y.append(arr[1])
        
    for ar in sortedArr:
        if ar[1] < min_step:
            colors.append('red')
        elif ar[1] > max_step:
            colors.append('red')
        else:
            colors.append('blue') 
    
    plt.bar(x, y, color = colors)
    plt.xticks(x, labels) #, rotation=90)
    plt.legend(handles=[red_patch, blue_patch])
    
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    year = datetime.now().year
    
    fig_path = os.path.join(cwd, "dataset_infos-"+str(currentDay)+"."+ str(currentMonth) +"."+ str(year) +".png")
    for i in range(len(y)):
        plt.text(x = float(x[i])-0.2 , y = float(y[i])+0.4, s = y[i], size = 6)
    #plt.show()
    plt.savefig(fig_path)
    plt.close()


def check_empty(dir_name):
    empty_list = []
    dir_path = os.path.join(cwd, dir_name)
  
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
    
        if os.stat(file_path).st_size == 0:
            empty_list.append(file_path)
            
    return empty_list

def main():
    results = parse_arguments()
    dirs = results.dir
    cl_file =  results.cl_file
    
    for d in dirs:
        if results.missing:
            out = check_missing_pairs(d)
            if out is True:
                print("No missing pairs")
            else:
                print("Missing pairs in:",d)
                
                for miss_elem in out:
                    print(miss_elem)
                     
        if results.infos:
            generate_ds_infos(d)
        if results.empty:
            out_empty = check_empty(d)
            if out_empty == []:
                print("No empty item")
            else:
                print("Empty items in :",d)
                for empty in out_empty:
                    print(empty)
    
    if class_dict:
        plot_diagram(1600,2200, cl_file)
    
if __name__ == "__main__":
    main()