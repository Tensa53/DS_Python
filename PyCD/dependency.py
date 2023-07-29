class Dependency:

    def __init__(self,name,version,filepath):
        self.name=name
        self.version=version
        self.filepath=filepath
        self.vulnerable=False
        self.bloated=False
        
    def printDependency(self):
        return self.name+self.version+" declared in: "+self.filepath
        
    name=""
    version=""
    filepath=""
    vulnerable=False
    bloated=False
