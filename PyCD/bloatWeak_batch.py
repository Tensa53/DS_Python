'''
439 progetti ingegnerizzati: 1 è privato (https://github.com/arita37/mlmodels)
'''
import subprocess
import os

def main():
    file=open("project_list.txt","w+")
    
    child=subprocess.run(["ls","/home/daniele/git/NICHE_projects/repo/","-1"],stdout=file)
    
    file.seek(0)
    
    lines=file.readlines()
    
    i=0
    
    for line in lines:
        projname=line.rstrip('\r\n')
        if(projname != "dataset_script"):
            i=i+1
            print("Executing BloatWeak for project n. " + str(i) + "/439: " + projname)
            savepath="/home/daniele/git/NICHE_projects/BloatWeak_Out/"+projname+"/"
            try: 
                os.mkdir(savepath)
            except FileExistsError:
                pass
            propath="/home/daniele/git/NICHE_projects/repo/"+projname+"/"
            file0=open(savepath+"bloatweak_out.txt","w")
            file1=open(savepath+"bloatweak_err.txt","w")
            child2=subprocess.run(["python3","bloatWeak.py",propath,savepath],stdout=file0,stderr=file1)
            file0.close()
            file1.close()
    
    file.close()
    os.remove("project_list.txt")
    
    print("Completed!!!")


if __name__ == "__main__":
    main()
