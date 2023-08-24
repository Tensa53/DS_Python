import pandas as pd
import dependency
import subprocess
import os

class ProjectStats:

    def __init__(self,name):
        self.name=name
        depNumber=0
        depBloatNumber=0
        depVulnNumber=0
        depBloatNumber=0
        depBloatVulnNumber=0
        vulnNumber=0

    name=""
    depNumber=0
    depBloatNumber=0 
    depVulnNumber=0
    depBloatVulnNumber=0
    vulnNumber=0

class CSVRow:
    
    def __init__(self,depName,version,filepath,bloated,cve):
        self.depName=depName
        self.version=version
        self.filepath=filepath
        self.bloated=bloated
        self.cve=cve

    depName=""
    version=""
    filepath=""
    bloated=False
    cve=""

measurables=[]
    
notMeasurables=[]

def loadCsv(csvRows,projcsv):
    for rowInd in projcsv.iterrows():
        row=rowInd[1]
        aRow=CSVRow(row[1],row[2],row[3],row[4],row[5])
        csvRows.append(aRow)

def calcStats(projname,csvRows,savepath):
    proj=ProjectStats(projname)

    aDep=dependency.Dependency("","","","")
    countedDep=False
    
    l=len(csvRows)
    
    i=0

    pycd=pd.read_csv(savepath+"pycd_out.csv")
    lll=len(pycd)

    while(i < l):
        if(not countedDep):
            countedDep=True
            proj.depNumber=proj.depNumber+1
            depName=csvRows[i].depName
            version=csvRows[i].version
            filepath=csvRows[i].filepath
            bloated=csvRows[i].bloated
            cve=csvRows[i].cve
            aDep.name=depName
            aDep.version=version
            aDep.filepath=filepath
            aDep.bloated=bloated
            #print(aDep.name)
            if(csvRows[i].bloated):
                proj.depBloatNumber=proj.depBloatNumber+1
            if(csvRows[i].cve!='no one'):
                aDep.vulnerable=True
                proj.depVulnNumber=proj.depVulnNumber+1
                proj.vulnNumber=proj.vulnNumber+1
                if(csvRows[i].bloated):
                    proj.depBloatVulnNumber=proj.depBloatVulnNumber+1
            i=i+1
            continue

        if(csvRows[i].depName==aDep.name and csvRows[i].version==aDep.version and csvRows[i].filepath==aDep.filepath and csvRows[i].bloated==aDep.bloated):
                proj.vulnNumber=proj.vulnNumber+1
                i=i+1
                continue
        else:
                countedDep=False
                continue
    
    stats=[proj.name,proj.depNumber,proj.depBloatNumber,proj.depVulnNumber,proj.depBloatVulnNumber,proj.vulnNumber]
    measurables.append(stats)

    if(not lll==proj.depNumber):
        print(proj.name+" real:"+str(lll)+"---calc:"+str(proj.depNumber)+" AAAAAAAAAAA")
    else:
        pass
        #print(proj.name+" real:"+str(lll)+"---calc:"+str(proj.depNumber))

def main():
    file=open("project_list.txt","w+")
    
    projspath="/home/daniele/git/Validation/BloatWeak_Out/"
    #projspath="/home/daniele/git/NICHE_projects/BloatWeak_Out/Cloneables/"
    
    child=subprocess.run(["ls",projspath,"-1"],stdout=file)
    
    file.seek(0)

    lines=file.readlines()

    ll=len(lines)
    
    #print(ll)

    cols=["project","#dependencies","#bloated","#vulnerable","#bloated&vulnerable","#vulnerabilities"]
    
    for line in lines:
        projname=line.rstrip('\r\n')
        savepath=projspath+projname+"/"
        try:
            #print(savepath+"safetyDB_out.csv")
            try:
                projcsv=pd.read_csv(savepath+"safetyDB_out.csv")
            except NotADirectoryError:
                continue
            print("Project " + projname + " is measurable")
            csvRows=[]
            loadCsv(csvRows,projcsv)
            calcStats(projname,csvRows,savepath)
        except FileNotFoundError:
            print("Project " + projname + " is not measurable")
            #print(projname)
            notMeasurables.append(projname)

    metrics=pd.DataFrame(measurables,columns=cols)
    #metrics.to_csv("measures_proj.csv")
    metrics.to_csv("measures_projv.csv")

    os.remove("project_list.txt")   

    print(str(len(measurables))+"/"+str(ll)+" project are measurables") 

if __name__ == "__main__":
    main()
