'''
439/440 engineered projects: 1 of this ones is private (https://github.com/arita37/mlmodels)
To correctly clone the projects, launch this script inside the desired clone folder and also copy in it the csv
'''

import pandas as pd
import subprocess
import requests

def main():
    niche=pd.read_csv("NICHE_Engineered_(Filtered ver. of NICHE).csv")
    
    repos=niche["GitHub Repo"]
    
    for r in repos:
        link="https://github.com/"+r
        l=requests.get(link)
        status_code=l.status_code
        if(status_code==200):
            print("Status Code: " + str(status_code) + " The repo " + link + " is public, proceeds with cloning it")
            child=subprocess.run(["git","clone",link])
        else:
            print("Status Code: " + str(status_code) + " The repo " + link + " is private")


if __name__ == "__main__":
    main()
