#440/572 ML projects are Engineered

import pandas as pd

def main():

    niche=pd.read_csv("NICHE.csv")
    
    engineered=niche[niche["Engineered ML Project"] == 'Y']
        
    print(engineered)
    
    #engineered.to_csv("NICHE_Engineered.csv",columns=col)
    engineered.to_csv("NICHE_Engineered_(Filtered ver. of NICHE).csv")
    
if __name__ == '__main__':
    main()
