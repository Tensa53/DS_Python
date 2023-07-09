#This script takes together three tools (PyCD, fawltydeps, safety) to find unused dependencies and their related vulnerabilities
import sys
import subprocess
import pandas as pd
import os
import json
from subprocess import DEVNULL

class Dependency:
    def __init__(self,name,version,filepath,vulnerable):
        self.name=name
        self.version=version
        self.filepath=filepath
        self.vulnerability=""
        
    def printDependency(self):
        return self.name+self.version+" declared in "+self.filepath+" "+self.vulnerability
        
dependencies=[]

#print on the shell the content of the help file
def printHelpSection():
    file=open("bloatWeak_help.txt","r")
    
    lines=file.readlines()
    
    for line in lines:
        print(line)

#print on the shell the list of all bloated dependencies, the ones affected by vulnerabilities are highlighted with 'VULNERABLE!!!' message on the same line
def getShellOutputJ(savepath):
    
    file5=open(savepath+"safety_out.json","r")
    
    jcontents=json.load(file5)
    
    print("Bloated dependencies for your project:")
    for d in dependencies:
        try:
            n=jcontents['affected_packages'][d.name]['name']
            d.vulnerability="VULNERABLE!!!"
            print(d.printDependency())
        except KeyError:
            print(d.printDependency())
    
    #delete the intermediate output, we don't need it anymore
    os.remove(savepath+"fawltydeps_out.txt")

def getSafetyOut(savepath):
    file3=open(savepath+"safety_out.json","w")
    
    #using run(), the main thread always wait for the end of the excecution of the command
    child3=subprocess.run(["safety","check","-r",savepath+"requirements-unused.txt","--output","json"],stdout=file3)
    
    file3.close()

def getUnusedRequirements(pycd_savepath,propath,savepath):
    
    #open the fawlatydeps_out.txt file in read/write mode
    file1=open(savepath+"fawltydeps_out.txt","w+")
    
    #the error output is redirected to devnull, so we don't have anything else that our output on the shell
    child2=subprocess.run(["fawltydeps",propath,"--check-unused","--detailed"], stdout=file1, stderr=DEVNULL)
    
    #move file pointer to the beginnig of the file
    file1.seek(0)

    #open the csv to read it with pandas
    csv1=pd.read_csv(pycd_savepath)
    
    #open the file where the dependencies declaration are going to be written
    file2=open(savepath+"requirements-unused.txt", "w")
    
    #excluding the first two of the file
    file1.readline()
    file1.readline()
    
    liner=file1.readline()
    
    while True:
        #delete from the line, whitespace characters and newlines
        line=liner.rstrip('\r\n')
        line=line.strip()
        #when the line starts with a dash, is the one with the dependency name
        if(line[0]=="-"):
            dep=line[3:(len(line)-14)]#take the dependency name substring from the line
            vers = csv1.loc[csv1['dep'] == dep, 'version'].values#take the dependency versions from pycd_out.csv
            files = list(csv1.loc[csv1['dep'] == dep, 'filepath'].values)#take the filepaths where dependency is declared from pycd_out.csv
            linep=file1.readline()
            
            #read all the lines after the one with the dependency name, until it finds a new one with another dependency name
            while(linep!="" and linep[0]!="-"):
                #extract the filepath from the line
                indS=linep.index('/')
                filePath=linep[indS:len(linep)-1]
                ind=files.index(filePath)
                
                #create a new string that contains the name and the version of the dependency
                depName=''.join([dep,vers[ind]])
                depName=depName.replace(' ','')
                depName+='\n'
                
                #create a new Dependency object and appends it in dependencies list
                dependency=Dependency(dep,vers[ind],filePath,"")
                dependencies.append(dependency)
                
                #write on the output file and read a new line from file1
                file2.write(depName)
                linep=file1.readline()
                
            liner=linep
            if(liner==""):
                break
            
    #closes the files streams            
    file1.close()
    file2.close()

def getPyCDOut(propath,pycd_savepath):
    child=subprocess.run(["python","./GetDep_ast.py",propath,pycd_savepath])

def launch(propath,savepath):
    #creates the save directory if not exist
    try:
        os.mkdir(savepath)
    except FileExistsError:
        print("Directory already exists, output files are written in it")

    pycd_savepath=savepath+"pycd_out.csv"
    
    #1. obtain the csv output from PyCD
    getPyCDOut(propath,pycd_savepath)
    print("PyCD output obtained in csv format")
    
    #2. obtain the outupt of falwtydeps and creates a requirements file
    getUnusedRequirements(pycd_savepath,propath,savepath)
    print("Unused requirements file obtained with FalwtyDeps")
    
    #3. obtain the json output of safety
    getSafetyOut(savepath)
    print("Safety ouptut obtained in json format")
    print()
    
    getShellOutputJ(savepath)
    print()
    print("Finished. You can find all the detailed output in the files stored in " + savepath + " directory")

#the script takes as input the project path to analize and the save path where to store all the outputs
def main():
    num=len(sys.argv)
    
    #check the number of arguments and the correct type of arguments
    if(num==3):
        propath=sys.argv[1]
        savepath=sys.argv[2]
        
        if(propath[len(propath)-1] == '/' and savepath[len(savepath)-1] == '/'):
            if(os.path.exists(propath)):
                launch(propath,savepath)
            else:
                print("THE PROJECT DIRECTORY DOES NOT EXISTS!!!\n")
                printHelpSection()
        else:
            print("THE ARGUMENTS MUST BE PATHS TO SOME DIRECTORIES!!!\n")
            printHelpSection()
    else:
        print("INSERT THE CORRECT NUMBER (2) OF ARGUMENTS!!!\n")
        printHelpSection()

if __name__ == '__main__':
    main()
