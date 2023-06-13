import re
import subprocess
class Utils:
    def getListDomain(data): 
        pattern = r"(?<!\S)[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?(?!\S)"
        domains = [item for item in data if re.match(pattern, item)]
        return domains
    

    def is_command_installed(command):
        try:
            # Use the subprocess module to run the command with the "--version" option
            output = subprocess.check_output([command, "--version"], stderr=subprocess.STDOUT, universal_newlines=True)
            return True
        except subprocess.CalledProcessError:
            # The command returned a non-zero exit status, indicating it's not installed or not found
            return False