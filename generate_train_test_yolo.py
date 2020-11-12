import os
import sys
import argparse
import random
classes_list = []
overwrite = True
train_list = []
test_list = []

max_class = 0

temp_list = []

def arg_parser():

     parser = argparse.ArgumentParser(description='''This script allows multiple
                                      YOLO format like dataset merging, train and validate txt generating.
                                           ''')
     
     parser.add_argument('-d', help="Directories ", dest="dir_list", nargs='+', required=True)
     parser.add_argument('-v', help="Specify how much of a set you want for validation. Integer type. Ex: -v 1 -> 10 proc of ds will be splitted for test", dest="split", type=int)
     parser.add_argument('-o', help="Output Directory", dest="out_dir", type=str)
     parser.add_argument('-rn', help="Rename the first part of the path in train txt with another directory", dest="rename_dir", type=str, default='')
    # parser.add_argument('-owr', help="Overwrite the current classes.", action="store_true", dest="overwrite")
     parser.add_argument('-plus',dest='plus', default=0, type=int)
     results = parser.parse_args()
     
     return results
 
def split_procent(procent):
    howManyNumbers = int(round(float(procent/10)*len(temp_list)))
    shuffled = temp_list[:]

    random.shuffle(shuffled)
    test_list.extend(shuffled[:howManyNumbers])
    train_list.extend(shuffled[howManyNumbers:])
    print("train_list : ", len(train_list))
    print("test_list :", len(test_list))
    

def write_to_file(ren_dir):
    
    prefix = ''
    if ren_dir != '':
        prefix = ren_dir
    out_f_train = open("train.txt","w")
    out_f_test = open("test.txt","w")
       
    for i in train_list:
        mix = str(prefix) + str(i) + "\n"
        out_f_train.write(mix)    
        
    for j in test_list:
        mix = str(prefix) + str(j) + "\n"
        out_f_test.write(mix)
    out_f_train.close()
    out_f_test.close()
        
def read_dir(dir_name, plus, out_dir):
    global max_class
    
    cwd = os.getcwd()
    dir_path = os.path.join(cwd, dir_name)
    out_dir = os.path.join(cwd, out_dir)
    
    try:
        os.mkdir(out_dir)
    except:
        print("directory already exist")
            
    for txt in os.listdir(dir_path):
        if txt.endswith(".txt"):
            img_name = txt[:-3]
            temp_list.append(img_name+"jpg")
            
            if plus != 0:
               
                txt_path = os.path.join(dir_path, txt)
                f_handler = open(txt_path, "r")
                out_f_path = os.path.join(out_dir, txt)
                out_f = open(out_f_path, "w")
                
                
                line = f_handler.readline()
                line_spliited = line.split()
                
                cl_id = int(line.split()[0])
                fin_val = cl_id + plus
                
                if cl_id > max_class:
                            max_class = cl_id

                out_f.write(str(fin_val)+ " " + line_spliited[1][0:6] + " " + line_spliited[2][0:6] + " "+ line_spliited[3][0:6] + " " + line_spliited[4][0:6]+ "\n")
                
                while line:
                    line = f_handler.readline()
                 
                    if line != '':
                        cl_id = int(line.split()[0])
                        fin_val = cl_id + plus
                        line_spliited = line.split()
                        
                        if cl_id > max_class:
                            max_class = cl_id
                        out_f.write(str(fin_val)+ " " + line_spliited[1][0:6] + " " + line_spliited[2][0:6] + " "+ line_spliited[3][0:6] + " " + line_spliited[4][0:6]+ "\n")
                       
                out_f.close()
                f_handler.close()
    
def main():
    arg_parser()
    res = arg_parser()
    procent = res.split
    out_dir = res.out_dir

    dir_list = res.dir_list
    for dir in dir_list:
        read_dir(dir, plus, out_dir)
        split_procent(procent)
  
    write_to_file(res.rename_dir)

if __name__ == "__main__":
    main()