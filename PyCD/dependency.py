class Dependency:

    def __init__(self,name,version,filepath):
        self.name=name
        self.version=version
        self.filepath=filepath
        self.vulnerable=""
        
    def printDependency(self):
        return self.name+self.version+" declared in:"+self.filepath+" "+self.vulnerable
        
    name=""
    version=""
    filepath=""
    vulnerable=""
