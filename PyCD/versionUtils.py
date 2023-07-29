from packaging import version

#takes a pinned/constrained dependency declaration as a string and extract the dependency name
def filterVersion(d):
    if(d[0]=='<' or d[0]=='>'):
        if(d[1]=='='):
            return d[2:]
        else:
            return d[1:]
    else:
        return d[2:]

#takes a pinned/constrained dependency decleration as a strng and check if is in the versions range
def compareVersions(d,versions):
    val=False

    for ver in versions:
        v=filterVersion(ver)
        if(ver[0]=='<'):
            if(ver[1]=='='):
                if(version.parse(d) == version.parse(v) or version.parse(d) < version.parse(v)):
                    return True
            else:
                if(version.parse(d) < version.parse(v)):
                    return True
        elif(ver[0]=='>'):
            if(ver[1]=='='):
                if(version.parse(d) == version.parse(v) or version.parse(d) > version.parse(v)):
                    return True
            else:
                if(version.parse(d) > version.parse(v)):
                    return True
        elif(ver[0]=='='):
                if(version.parse(d) == version.parse(v)):
                    return True
                    
    return False
    
def checkVersions(d,v):
    df=filterVersion(d)

    versions=v['v'].split(',')
    if(compareVersions(df,versions)==True):
        return True
