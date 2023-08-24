class Dependency:

    def __init__(self,name,version,filepath,defType):
        self.name=name
        self.version=version
        self.filepath=filepath
        self.defType=defType
        self.vulnerable=False
        self.detectBloated=False
        self.realBloated=False
        
    def printDependency(self):
        return self.name+self.version+" declared in: "+self.filepath
        
    name=""
    version=""
    filepath=""
    defType=""
    vulnerable=False
    detectBloated=False
    realBloated=False
