
# coding: utf-8

# In[ ]:


import os
import numpy as np
import pandas as pd
import jieba as jb
import csv
#######################################get the argument

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()
    
    # Please implement your algorithm below
    
    # TODO load source data, build search engine

    # TODO compute query result
  
    # TODO output result

############################################get resource data
#userhome =os.path.expanduser('~')
#source_data_path = userhome + "/Desktop/source .csv"
source_data_path = args.source
source = pd.read_csv(source_data_path,header=None)
source.columns=["Index","News_Title"]
############################################build inverted index
dic = {}
for i in range(len(source)):
    temp_str = source.iat[i,1]
    temp_list = jb.lcut(temp_str,cut_all=False) 
   
    for j in range(len(temp_list)):   
        if temp_list[j] in dic:
           dic[temp_list[j]].append(i+1)
        else:
            dic[temp_list[j]]=[i+1]
        
del i
del j

####################################################get query data
#query_data_path = userhome+"/Desktop/query .txt"
query_data_path = args.query
query = pd.read_csv(query_data_path,header=None)
query.columns=["query_keyword"]
#############################################list query string
query_list=[]#new a list

for i in range(len(query)):
  query_string = query.iat[i,0]#get string

  seg_list = jb.lcut(query_string,cut_all=False)
  temp_list = []#empty list
  for j in range(len(seg_list)):
     
     if seg_list[j] != " ":   
         temp_list.append(seg_list[j])
  
  query_list.append(temp_list)#query list


del temp_list

##############################################get the look up result         
output_list = [] 
temp_list = []
temp_set = set()

for i in range(len(query_list)):
    for j in query_list[i]:
          
          if(j in dic and "and" in query_list[i]):
                
           
                if (temp_set == set()):
                    temp_set = set(dic[j])
                    
                   
              
                elif(j != "and"):
                    temp_set = temp_set.intersection(set(dic[j]))
                   
                  
          elif(j in dic and "or" in query_list[i]):
                
                if(temp_set == set()):
                    temp_set = set(dic[j])
                    
                elif(j != "or"):               
                    temp_set=temp_set.union(set(dic[j]))   
                    
          elif(j in dic and "not" in query_list[i]):
                 
              
                 if (temp_set == set()):
                     temp_set = set(dic[j])
                     
              
                 elif(j != "not"):
                     temp_set = temp_set.difference(set(dic[j]))
                     
          
          
    
    temp_list = list(temp_set.copy())  
    temp_list.sort(reverse=False)
    
    if (temp_list == []):
        temp_list.append(0)
    
    output_list.append(temp_list[:])
          
    temp_set = set()  
          
#######################################################export output list
output_data_path = args.output
#output = open('/Users/johnodin99/Desktop/output.txt','w') 
output = open(output_data_path,'w') 
outputCSV = csv.writer(output)
outputCSV.writerows(output_list)
output.close()
  

