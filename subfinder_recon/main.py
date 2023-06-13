from .subfinder_tool import SubfinderTool
from .findomain_tool import FindomainTool
from .asetfinder_tool import AssetFinderTool
from .amass_tool import AmassTool
import time
class SubDomainReconTool:
    def __init__(self, domain): 
        self.domain = domain
        self.listDomain = []


    def run(self):
        startTime = time.time() 

        findomainList = FindomainTool(self.domain).enumerate_subdomains()
        # amassList = AmassTool(self.domain).enumerate_subdomains()
        assetfinderList = AssetFinderTool(self.domain).enumerate_subdomains()
        subfinderList = SubfinderTool(self.domain).enumerate_subdomains()
        # listDomain = amassList + assetfinderList + findomainList + subfinderList
        listDomain = assetfinderList + findomainList + subfinderList
        uniqueList = list(set(listDomain))
        
        print(f"[+] The final script finish in: {time.time() - startTime}")
        
        self.listDomain = uniqueList
        return uniqueList
    
    
    def writeToFile(self): 
        if len(self.listDomain) == 0: 
            print('There is no file to write. use run() in SubDomainReconTool to generate output.txt')
            return
        
        with open("output.txt", "w") as file:
            # Iterate over each element in the list
            for item in self.listDomain:
                # Write the element to the file
                file.write(str(item) + "\n")

if __name__ == '__main__':
    tool = SubDomainReconTool('bugcrowd.com')
    tool.run()
    tool.writeToFile()
