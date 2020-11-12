# YOLO Dataset Toolkit

Small toolkit to analyze, check and generate train/test files from YOLO formatted dataset.

#   Check Data Healty 
 Use *check_data_healty.py*  to search for:
 * missing pairs of text - jpg/jpeg 
 * empty files (both txt and jpg/jpeg)
 
How to run:

        $python ./check_data_healty.py --missing --empty -d PATH_TO_DIR
# Generate Dataset Infos
Use *check_data_healty.py*.
Specify after "-clfile" the path to the class name file (eg. "obj.names")
Use "--infos" flag.

 ![Image of Dataset](https://cdn1.bbcode0.com/uploads/2020/11/12/f19199aba344472d35935c4e871214d7-full.png)
    
    $python ./check_data_healty.py --infos -clfile PATH_TO_CLASS_NAME_FILE

# Generate Train/ Test Files
 Use *generate_train_test_yolo.py*.
  ### Arguments:
  
  - d : Path to your dataset directory
  - v : v*10 procent of the dataset will be splitted for training
    Ex: -v 1 : 10% of your ds will be split for training

        $ python ./generate_train_test_yolo.py -d PATH_TO_DATASET -v 2
    this will split the dataset by 20% for testing and 80% for training 
 # Merge multiple datasets
 Problem: Suppose you have three datasets each with N1,N2,N3 classes.
 Each ds has it's own YOLO formatted txts where the classes are notated with numbers in range 0 - N.
 When you want to merge all these datasets some of the labeled classes will overlap.
 EX: Suppose in each dataset you have at least one object labeled as "0".
    If you merge the datasets without updating the classes number you will have 3 different objects labeled as "0" in your final ds.
    Instead, you should have the objects label different, for example: "0","1","2".
  ![Problem Scheme](https://cdn1.bbcode0.com/uploads/2020/11/12/5a4bc3f4f23d8cf89a9a0cf1f343a8bf-full.png)
  
  
 ### Arguments:
  - d : specify the directory containing all images and txts.
  - o : output directory
  - plus : specify how much to add to the current class
  
        $ python ./generate_train_test.py -d PATH_TO_DATASET -o PATH_TO_DEST_DIR -plus 2
    Suppose you have the following label:
    *0 0.5712 0.6451 0.0029 0.0117*
    After running:
    *2 0.5712 0.6451 0.0029 0.0117*

 TODO next: Merge all the train/test files

