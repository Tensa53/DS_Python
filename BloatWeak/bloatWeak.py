#This script takes together three tools (PyCD, fawltydeps, safety) to find unused dependencies and their related vulnerabilities

import sys
import subprocess
import pandas as pd
import os
from subprocess import DEVNULL

def getSafetyOut(savepath):
    file3=open(savepath+"/safety_out.json","w")
    
    #using call instead of Popen, the main thread always wait for the end of the excecution of the command
    child3=subprocess.call(["safety","check","-r",savepath+"/requirements-unused.txt","--output","json"],stdout=file3)
    
    file3.close()

def getUnusedRequirements(pycd_savepath,propath,savepath):
    
    #open the fawlatydeps_out file in read/write mode
    file1=open(savepath+"/fawltydeps_out.txt","w+")
    
    #the error output is redirected to devnull, so we don't have anything else that our output on the shell
    child2=subprocess.call(["fawltydeps",propath,"--check-unused"], stdout=file1, stderr=DEVNULL)
    
    #move file pointer to the beginnig of the file
    file1.seek(0)
    
    #read all the lines of the file
    lines=file1.readlines()

    #open the csv to read it with pandas
    csv1=pd.read_csv(pycd_savepath)
    
    #remove duplicate lines from csv
    csv1.drop_duplicates(subset=None, inplace=True)

    file2=open(savepath+"/requirements-unused.txt", "w")
    
    for line in lines:
        #when the line starts with a dash, is the one with the dependency name
        if(line[0]=="-"):
            dep=line[3:(len(line)-2)]#take the dependency name substring from the line
            ver = csv1.loc[csv1['dep'] == dep, 'version'].values[0]#extract the version of the dependency from the csv
            depName=''.join([dep,ver])#merge the dep string and the ver string, to take full specification of the dependency
            depName+="\n"#adds the new line to write on file
            file2.write(depName)#write on the requirements-unused.txt file
        else:
            continue
            #print("it's a blank line or something else line")
            
    #closes the files streams            
    file1.close()
    file2.close()
    
    #delete the intermediate output, we don't need it anymore
    os.remove(savepath+"/fawltydeps_out.txt")

def getPyCDOut(propath,pycd_savepath):
    child=subprocess.call(["python","../PyCD/GetDep_ast.py",propath,pycd_savepath])


def main():
    #the script takes as input the project path to analize and the save path where to store all the outputs
    propath=sys.argv[1]
    savepath=sys.argv[2]
    
    #creates the save directory if not exist
    try:
        os.mkdir(savepath)
    except FileExistsError:
        print("Directory already exists, output files are overwritten")
    
    pycd_savepath=savepath+"/pycd_out.csv"
    
    #1. obtain the csv output from PyCD
    getPyCDOut(propath,pycd_savepath)
    print("PyCD output obtained in csv format")
    
    #2. obtain the outupt of falwtydeps and creates a requirements file
    getUnusedRequirements(pycd_savepath,propath,savepath)
    print("Unused requirements file obtained with FalwtyDeps")
    
    #3. obtain the json output of safety
    getSafetyOut(savepath)
    print("Safety ouptut obtained in json format")
    
    print("Finished! You can find all the output in your directory")
    

if __name__ == '__main__':
    main()
