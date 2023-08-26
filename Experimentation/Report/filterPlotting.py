import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def antiJoin():
    csv1=pd.read_csv("bl1.csv")
    csv2=pd.read_csv("bl2.csv")
    
    print(len(csv1))
    print(len(csv2))
    
    #perform outer join
    outer = csv1.merge(csv2, how='outer', indicator=True)

    #perform anti-join
    anti_join = outer[(outer._merge=='left_only')].drop('_merge', axis=1)

    #view results
    print(anti_join)

def noBloatedFilter():
    csv2=pd.read_csv("report.csv")
    
    bloated2=csv2[(csv2["Comment"]=="This project is correctly measurable by measure_proj.py script") | (csv2["Comment"]=="This project has more than 1000 dependencies")]
    
    bloated2.to_csv("bl2.csv")
    
    print(bloated2)

def bloatedFilter():
    csv1=pd.read_csv("measures_proj.csv")
    
    bloated=csv1[csv1["#bloated"]>0]
    
    bloatedd=bloated.drop(columns=['Unnamed: 0'])
    
    bloatedd.to_csv("bloated.csv")
    
def bloatedNFilter():
    data=[]
    
    cols=["#bloated","#project"]
    
    csv1=pd.read_csv("bloated.csv")
    
    bloatednum=csv1["#bloated"]
    
    maxx=bloatednum.max()
    
    print(maxx)
    
    i=1
    
    while i <= maxx:
        bloatedn=csv1[csv1["#bloated"]==i]
        bloatednn=bloatedn.drop(columns=['Unnamed: 0'])
        lbl=len(bloatedn)
        if(lbl==0):
            pass
        else:
            row=[i,lbl]
            print(str(lbl) + " progetti hanno " + str(i) + " bloated dependency")
            blname="bloated"+str(i)+".csv"
            bloatednn.to_csv(blname)
            data.append(row)
        i=i+1
        
    reportBl=pd.DataFrame(data,columns=cols)
    reportBl.to_csv("reportBl.csv")
    
def bldReportPlot():
    csv1=pd.read_csv("reportBl.csv")
    
    bln=csv1["#bloated"]
    prn=csv1["#project"]
    
    df = pd.DataFrame({'#bloated':bln, '#project':prn})
    ax = df.plot.bar(x='#bloated', y='#project', rot=0)
    ax.bar_label(ax.containers[0])
    plt.show()
    
def vulnFilter():
    csv1=pd.read_csv("measures_proj.csv")
    
    vulnerables=csv1[csv1["#vulnerabilities"]>0]
    
    vulnerabless=vulnerables.drop(columns=['Unnamed: 0'])
    
    vulnerabless.to_csv("vulnerables.csv")
    
def vulnNFilter():
    data=[]
    
    cols=["#vulnerable","#project"]
    
    csv1=pd.read_csv("vulnerables.csv")
    
    vulnnum=csv1["#vulnerable"]
    
    maxx=vulnnum.max()
    
    print(maxx)
    
    i=1
    
    while i < maxx:
        vulnerablesn=csv1[csv1["#vulnerable"]==i]
        vulnerablesnn=vulnerablesn.drop(columns=['Unnamed: 0'])
        lbl=len(vulnerablesn)
        if(lbl==0):
            pass
        else:
            row=[i,lbl]
            print(str(lbl) + " progetti hanno " + str(i) + " dipendenze vulnerabili")
            vlname="vulnerables"+str(i)+".csv"
            vulnerablesnn.to_csv(vlname)
            data.append(row)
        i=i+1
        
    reportVuln=pd.DataFrame(data,columns=cols)
    reportVuln.to_csv("reportVuln.csv")
    
def vulnReportPlot():
    csv1=pd.read_csv("reportVuln.csv")
    
    vln=csv1["#vulnerable"]
    prn=csv1["#project"]
    
    media=csv1[['#vulnerable']].mean(axis=0)
    
    print(media)
    
    df = pd.DataFrame({'#vulnerable':vln, '#project':prn})
    ax = df.plot.barh(x='#vulnerable', y='#project', rot=0)
    
    ax.bar_label(ax.containers[0])
    plt.show()
    
def bldVulnFilter():
    csv1=pd.read_csv("measures_proj.csv")
    
    bldVuln=csv1[(csv1["#bloated&vulnerable"]>0)]
    
    bldVulnn=bldVuln.drop(columns=['Unnamed: 0'])
    
    bldVulnn.to_csv("bloated&vulnerable.csv")
    
def bldVulnNFilter():
    data=[]
    
    cols=["#bloated&vulnerable","#project"]
    
    csv1=pd.read_csv("bloated&vulnerable.csv")
    
    vulnnum=csv1["#bloated&vulnerable"]
    
    maxx=vulnnum.max()
    
    print(maxx)
    
    i=1
    
    while i <= maxx:
        bloatedn=csv1[csv1["#bloated&vulnerable"]==i]
        bloatednn=bloatedn.drop(columns=['Unnamed: 0'])
        lbl=len(bloatedn)
        if(lbl==0):
            pass
        else:
            row=[i,lbl]
            print(str(lbl) + " progetti hanno " + str(i) + " dipendenze vulnerabili")
            blname="bloatedvulnerables"+str(i)+".csv"
            bloatednn.to_csv(blname)
            data.append(row)
        i=i+1
        
    reportBl=pd.DataFrame(data,columns=cols)
    reportBl.to_csv("reportBldVuln.csv")
    
def bldVulnReportPlot():
    csv1=pd.read_csv("reportBldVuln.csv")
    
    bldVln=csv1["#bloated&vulnerable"]
    prn=csv1["#project"]
    
    df = pd.DataFrame({'#bloated&vulnerable':bldVln, '#project':prn})
    ax = df.plot.bar(x='#bloated&vulnerable', y='#project', rot=0)
    
    ax.bar_label(ax.containers[0])
    plt.show()
    
def bldNotVulnFilter():
    csv1=pd.read_csv("bloated.csv")
    
    bldNotVuln=csv1[csv1['#bloated&vulnerable']==0]
    
    bldNotVulnn=bldNotVuln.drop(columns=['Unnamed: 0'])
    
    bldNotVulnn.to_csv('bloated&NotVulnerable.csv')

def main():
    bldVulnNFilter()
    #print("Select a function to call specifying it in the main() code")

if __name__ == "__main__":
    main()
