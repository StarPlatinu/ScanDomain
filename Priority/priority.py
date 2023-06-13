import subprocess                     # install subprocess
from bs4 import BeautifulSoup         # install beautifulsoup4
import os
class AmassTool:
    def __init__(self, listDomains, rootDomain): 
        self.root_domain = rootDomain
        self.list_subdomains = listDomains
        self.current_directory = os.getcwd()
        self.dir_output = self.current_directory
        self.name_output="amass2"    
        self.command = 'amass viz -d3 -o {0} -oA {1} -d {2} '.format(
                        self.current_directory, 
                        self.name_output,
                        self.root_domain)
        self.script = self.initial_code()
        
    def initial_code(self):
        # Opening the html file
        HTMLFile = open("{0}/{1}.html".format(self.dir_output, self.name_output), "r")
        # Reading the file
        index = HTMLFile.read()

        # Creating a BeautifulSoup object and specifying the parser
        S = BeautifulSoup(index, 'html.parser' )
        print(type(S.select('script:nth-of-type(1)')))

        script = S.select('script:nth-of-type(1)').__str__()
        start = script.find("nodes: [")+8
        end = script.find("],")

        script = script[start:end:1].replace(" ", "").replace("\n\n", " ")
        return script
    
    # create bien dictionary ( KEY - VALUE)  (subdomain - num )
    def createDict(self, list_subdomains,script):
        dict ={}
        a_list = list_subdomains.copy()
        total =0
        ave = 0
        for x in list_subdomains:
            index=script.find(x)
            if index != -1 :
                end= script.rfind(",label:",0,index)
                start= script.rfind(",num:",0,index)+5
                num = int(script[start:end:1])
                # print(num)
                dict[x]=num
                a_list.remove(x)
                total += num
                # print(dict)

        # print(len(dict))
        # print(total)
        if total !=0:
            ave = total//len(dict)
        # print(ave)
        for x in a_list:
            dict[x] = ave
        return dict
    
    def get_num(self, subdomain, dict):
        return dict[subdomain]

    def checkWAF(self, subdomain):
        output = subprocess.check_output(["wafw00f",subdomain],universal_newlines=True)
        if output.find(" is behind ") != -1:
            return 1
        else:
            return 0
        
    def run(self):
        dic = self.createDict(self.list_subdomains,self.script)
        new_list = sorted(self.list_subdomains, key=lambda x: (self.get_num(x,dic), self.checkWAF(x)))
        print(new_list)
        return new_list


if __name__ == '__main__':
    listDomains = ['wiki.owasp.org','dsomm.owasp.org','ahihi.org']
    rootDomain = "owasp.org"
    tool = AmassTool(listDomains, rootDomain)
    tool.run()
