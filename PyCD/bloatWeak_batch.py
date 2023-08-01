import subprocess
import os

def main():
    file=open("projects_list.txt","w+")
    
    projspath="/home/daniele/git/NICHE_projects/Repo/Cloneables/"
    savepath="/home/daniele/git/NICHE_projects/BloatWeak_Out/Cloneables/"
    
    child=subprocess.run(["ls",projspath,"-1"],stdout=file)
    
    file.seek(0)
    
    lines=file.readlines()
    
    ll=len(lines)
    
    for i in range(ll):
        repo=lines[i].rstrip('\r\n')
        print("Executing BloatWeak for project "+str(i+1)+"/"+str(ll)+": "+repo)
        propath=projspath+repo+"/"
        pycd_savepath=savepath+repo+"/"
        try:
            os.mkdir(pycd_savepath)
        except FileExistsError:
            pass
        file1=open(pycd_savepath+"bloatweak_out.txt","w")
        file2=open(pycd_savepath+"bloatweak_err.txt","w")
        child1=subprocess.run(["python3","bloatWeak.py",propath,pycd_savepath],stdout=file1,stderr=file2)
        file1.close()
        file2.close()
        
    os.remove("projects_list.txt")
        
    print("Completed!")

if __name__ == "__main__":
	main()
