import subprocess
import time
from .utils import Utils
class AmassTool: 
    def __init__(self, domain):
        self.domain = domain
    
    def enumerate_subdomains(self):
        try:
            startTime = time.time()
            command = ['amass', 'enum', '-d', self.domain]
            
            print("[+] Start extracting using Amass...")
            output = subprocess.check_output(command, universal_newlines=True)
            print("==> Extracted data:", output)
            
            print(f"[+] Script finish in: {time.time() - startTime}")

            result = list(set(output.strip().split('\n')))
            finalList = Utils.getListDomain(result)

            return finalList
        except subprocess.CalledProcessError:
            print('Amass tool might not be installed.')
            return []