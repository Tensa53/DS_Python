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
def getShellOutput(savepath):
    print("Bloated dependencies for your project:")

    bloat=False

    for d in dependencies:
        if(d.detectBloated and d.realBloated):
            bloat=True
            if(d.vulnerable):
                print(d.printDependency()+" VULNERABLE!!!")
            else:
                print(d.printDependency())
                
    if(not bloat):
        print("This project has no bloated dependencies")


def getSafetyDBOut(savepath):
    file3=open("insecure_full.json","r")
    
    jcontents=json.load(file3)
    
    cols=["dep","version","filepath","bloated","cve","affected versions","advisory"]
    
    deps=[]
    
    for d in dependencies:
        lowD=d.name.lower()#normalize the name of dependency as the ones in the db
        dv=d.version
        dvs=dv.split(',')
        try:
            depVul=jcontents[lowD]#extract from the db, the section related this dependency
            for v in depVul:
                if(versionUtils.checkVersions(dvs,v)):
                    d.vulnerable=True
                    cve=v['cve']
                    vers=v['v']
                    advise=v['advisory']
                    depv=[]
                    depv.append(d.name)
                    depv.append(d.version)
                    depv.append(d.filepath)
                    depv.append(d.realBloated)
                    depv.append(cve)
                    depv.append(vers)
                    depv.append(advise)
                    deps.append(depv)
            if(not d.vulnerable):
                #when the vulnerable flag is still False after the checkVersions loop, it means that the dependency is in the db but that our analyzed version is not vulnerable
                depv=[]
                depv.append(d.name)
                depv.append(d.version)
                depv.append(d.filepath)
                depv.append(d.realBloated)
                depv.append("no one")
                depv.append("no one")
                depv.append("no one")
                deps.append(depv)
        except KeyError:
            #when a dependency is not vulnerable, is not in the db and try to use its name as a key, throws an exception
            depv=[]
            depv.append(d.name)
            depv.append(d.version)
            depv.append(d.filepath)
            depv.append(d.realBloated)
            depv.append("no one")
            depv.append("no one")
            depv.append("no one")
            deps.append(depv)
    
    #create a pandas dataframe and saves it on a csv table file
    safetyDBFilter=pd.DataFrame(deps,columns=cols)
    safetyDBFilter.to_csv(savepath+"safetyDB_out.csv")
            
    file3.close()
    

def setBloated(depName,filePath,step):
    for d in dependencies:
        if(d.name==depName and d.filepath==filePath):
            if(d.defType=="install_requires"):
                d.detectBloated=True
                if(step==2):
                    d.realBloated=True
                return 2
            else:
                return 1

    return 0

def getUnusedRequirements(propath,savepath,step):
    incomplete=False

    #open the fawltydeps_out.txt file in read/write mode
    file1=open(savepath+"fawltydeps_out.txt","w+")
    
    #the error output is redirected to devnull, so we don't have anything else that our output on the shell
    child2=subprocess.run(["fawltydeps",propath,"--check-unused","--detailed"], stdout=file1, stderr=DEVNULL)
    
    #move file pointer to the beginnig of the file
    file1.seek(0)
    
    #excluding the first two lines of the file
    file1.readline()
    file1.readline()
    
    #read the first line with a dependency name
    liner=file1.readline()

    while True:
        #delete from the line, whitespace characters and newlines
        line=liner.rstrip('\r\n')
        line=line.strip()

        #when the line starts with a dash, is the one with the dependency name
        try:
            if(line[0]=="-"):
                dep=line[3:(len(line)-14)]#take the dependency name substring from the line
                linep=file1.readline()
        
                while(linep!="" and linep[0]!="-"):
                    #extract the filepath from the line
                    indS=linep.index('/')
                    filePath=linep[indS:len(linep)-1]
                    indSe=filePath.rindex('/')
                    reqName=filePath[indSe+1:]
                    indSd=reqName.rfind("-")
                    indSu=reqName.rfind("_")
                    if(indSd==-1 and indSu==-1):
                        #check if the dependency is bloated
                        res=setBloated(dep,filePath,step)
                        if(res==0):     
                            incomplete=True
                            #comment the next three lines if you also want to analyze the output of incomplete projects
                            print("PyCD is missing some configuration files, the output is incomplete.")
                            os.remove(savepath+"fawltydeps_out.txt")
                            exit(0)
                            
                    #read a new line from file1
                    linep=file1.readline()
        except IndexError:
            #if the fawltydep_out.txt has less than three lines, it means that the project has no bloated dependencies
            file1.seek(0)
            file1.readline()
            msg=file1.readline()
            msg=msg.rstrip('\r\n')
            if(msg=="No unused dependencies detected."):
                os.remove(savepath+"fawltydeps_out.txt")
                return
            else:
                print("Fawltydeps returns errors and you need to manually execute the tool to check the issues, the output is incomplete")
                os.remove(savepath+"fawltydeps_out.txt")
                #comment the next line if you also want to analyze the output of incomplete projects
                exit(0)
                return

        liner=linep
        if(liner==""):
            break

    if(incomplete):
        print("PyCD is missing some configuration files, the output is incomplete")

    #closes the file streams            
    file1.close()

    os.remove(savepath+"fawltydeps_out.txt")
    
def installUnused(savepath):
    print("Installing unused dependencies")
    
    for d in dependencies:
        if(d.detectBloated):
            child1=subprocess.run(["pip","install",d.name],stdout=DEVNULL,stderr=DEVNULL)

def getPyCDOut(propath,pycd_savepath):
    child=subprocess.run(["python","./GetDep_ast.py",propath,pycd_savepath])

    try:
        csv=pd.read_csv(pycd_savepath)
        csvd=csv.drop_duplicates(subset=["dep","version","filepath"], keep="first")
        csvdd=csvd.drop(columns=['Unnamed: 0'])
    except FileNotFoundError:
        print("PyCD has some issues scanning this project, pycd_out.csv file does not exists. Execution interruepted")
        exit(0)

    if(len(csvd)==0):
        print("PyCD has some issues scanning this project, pycd_out.csv is an empty file. Execution interruepted")
        exit(0)

    #also save the pycd output in a list of Dependency objects
    for rowInd in csvdd.iterrows():
        row=rowInd[1]
        aDep=dependency.Dependency(row['dep'],row['version'],row['filepath'],row['type'])
        dependencies.append(aDep)

    os.remove(pycd_savepath)
    csvdd.to_csv(pycd_savepath)


def launch(propath,savepath):
    #creates the save directory if not exist
    try:
        os.mkdir(savepath)
    except FileExistsError:
        print("Directory already exists, output files are written in it")

    pycd_savepath=savepath+"pycd_out.csv"
    
    #Obtain the csv output from PyCD
    getPyCDOut(propath,pycd_savepath)
    print("PyCD output obtained in csv format (pycd_out.csv)")
    
    #Obtain the outupt of falwtydeps and check which dependencies are bloated
    print("Checking unused dependencies with FawltyDeps")
    step=1
    #execute the first check without unused deps installed (simple mapping)
    getUnusedRequirements(propath,savepath,step)
    
    installUnused(savepath)
    
    step=2
    #execute the second check with unused deps installed (improved mapping)
    getUnusedRequirements(propath,savepath,step)
    #uninstallUnused(savepath)
    
    #Obtain a csv format of bloated&vulnerable dependencies, filtering safetyDB
    getSafetyDBOut(savepath)
    print("SafetyDB filtered output obtained in csv format (safetyDB_out.csv)")
    print()
    
    getShellOutput(savepath)
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
