#This script takes together three tools (PyCD, fawltydeps, safetyDB) to find unused dependencies and their related vulnerabilities
import sys
import subprocess
from subprocess import DEVNULL
import pandas as pd
import os
import json
import dependency
import versionUtils
        
dependencies=[]

#print on the shell the content of the help file
def printHelpSection():
    file=open("bloatWeak_help.txt","r")
    
    lines=file.readlines()
    
    for line in lines:
        print(line)


#print on the shell the list of all bloated dependencies, the ones affected by vulnerabilities are highlighted with 'VULNERABLE!!!' message on the same line
def getShellOutputJ(savepath):
    print("Bloated dependencies for your project:")

    for d in dependencies:
        print(d.printDependency())


def getSafetyDBOut(savepath):
    file3=open("insecure_full.json","r")
    
    jcontents=json.load(file3)
    
    cols=["bloated dep","version","filepath","cve","affected versions","advisory"]
    
    deps=[]
    
    for d in dependencies:
        lowD=d.name.lower()#normalize the name of dependency as the ones in the db
        dv=d.version
        print(lowD)
        try:
            depVul=jcontents[lowD]#extract from the db, the section related this dependency
            for v in depVul:
                if(versionUtils.checkVersions(dv,v)):
                    d.vulnerable="VULNERABLE!!!"
                    cve=v['cve']
                    vers=v['v']
                    advise=v['advisory']
                    depv=[]
                    depv.append(d.name)
                    depv.append(d.version)
                    depv.append(d.filepath)
                    depv.append(cve)
                    depv.append(vers)
                    depv.append(advise)
                    deps.append(depv)
        except KeyError:
            #when a dependency is not vulnerable, is not in the db and try to use its name as a key, throws an exception
            depv=[]
            depv.append(d.name)
            depv.append(d.version)
            depv.append(d.filepath)
            depv.append("no one")
            depv.append("no one")
            depv.append("no one")
            deps.append(depv)
            continue
    
    #create a pandas dataframe and saves it on a csv table file
    safetyDBFilter=pd.DataFrame(deps,columns=cols)
    safetyDBFilter.to_csv(savepath+"safetyDB_out.csv")
            
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
    #file2=open(savepath+"requirements-unused.txt", "w")
    
    #excluding the first two lines of the file
    file1.readline()
    file1.readline()
    
    #read the first line with a dependency name
    liner=file1.readline()
    
    while True:
        #delete from the line, whitespace characters and newlines
        line=liner.rstrip('\r\n')
        line=line.strip()
        try:
        #when the line starts with a dash, is the one with the dependency name
            if(line[0]=="-"):
                dep=line[3:(len(line)-14)]#take the dependency name substring from the line
                vers = csv1.loc[csv1['dep'] == dep, 'version'].values#take the dependency versions from pycd_out.csv
                files = list(csv1.loc[csv1['dep'] == dep, 'filepath'].values)#take the filepaths where dependency is declared from pycd_out.csv
                linep=file1.readline()
                
                #print(dep)
                #print(files)
            
                #read all the lines after the one with the dependency name, until it finds a new one with another dependency name
                while(linep!="" and linep[0]!="-"):
                    #extract the filepath from the line
                    indS=linep.index('/')
                    filePath=linep[indS:len(linep)-1]
                    try:
                        ind=files.index(filePath)
                    except ValueError as e:
                        msg=str(e)
                        path=msg[1:len(msg)-16]
                        print("Pycd has some problems with config declaration in this file:")
                        print(path)
                        print("The results are affected by this issue, some dependencies are not considered")
                
                    #create a new string that contains the name and the version of the dependency
                    depName=''.join([dep,vers[ind]])
                    depName=depName.replace(' ','')
                    depName+='\n'
                
                    #create a new Dependency object and appends it in dependencies list
                    aDep=dependency.Dependency(dep,vers[ind],filePath)
                    dependencies.append(aDep)
                
                    #read a new line from file1
                    linep=file1.readline()
                
            liner=linep
            if(liner==""):
                break
        except IndexError:
                #if the fawltydep_out.txt has less than three lines, it means that the project has no bloated dependencies
                file1.seek(0)
                file1.readline()
                msg=file1.readline()
                if(msg=="No unused dependencies detected."):
                    print("This project has no bloated dependencies")
                else:
                    print("Fawltydeps gives errors, you need to manually execute the tool to check the issues")
                os.remove(savepath+"fawltydeps_out.txt")
                exit(0)
            
    #closes the file streams            
    file1.close()
    
    os.remove(savepath+"fawltydeps_out.txt")


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
    print("PyCD output obtained in csv format (pycd_out.csv)")
    
    #2. obtain the outupt of falwtydeps and creates a requirements file
    getUnusedRequirements(pycd_savepath,propath,savepath)
    #print("Unused requirements file obtained with FalwtyDeps")
    
    #3. obtain a csv format of bloated&vulnerable dependencies, filtering safetyDB
    getSafetyDBOut(savepath)
    print("SafetyDB filtered output obtained in csv format (report.csv)")
    print()
    
    getShellOutputJ(savepath)
    print()
    print("You can find all the detailed output in the files stored in " + savepath + " directory")


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
