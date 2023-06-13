import subprocess
import time
from .utils import Utils
class FindomainTool: 
    def __init__(self, domain):
        self.domain = domain

    def enumerate_subdomains(self): 
        try: 
            startTime = time.time()
            command = ['findomain', '-t', self.domain]

            print("[+] Start extracting using Find...")
            output = subprocess.check_output(command, universal_newlines=True)
            print("==> Extracted data:", output)
            
            print(f"[+] Script finish in: {time.time() - startTime}")
            
            result = list(set(output.strip().split('\n')))
            finalList = Utils.getListDomain(result)
            
            return finalList
        except subprocess.CalledProcessError:
            print('Findomain tool might not be installed.')
            return []