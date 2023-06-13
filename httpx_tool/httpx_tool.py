import subprocess

class ToolHTTPX:
    def __init__(self, subdomains):
        self.subdomains = subdomains

    def enumerate_subdomains(self):
        listLiveUrl = []
        for subdomain in self.subdomains:
            httpx_command = ['httpx', '-mc', '200,201,206,302,403', '-u', subdomain]
            httpx_output = subprocess.check_output(httpx_command, universal_newlines=True)
            url = httpx_output.strip().splitlines()
            if len(url) != 0:
                listLiveUrl.append(url[0])
        return listLiveUrl

    def get_unique_subdomains(self):
        return self.subdomains

