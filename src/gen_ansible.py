import logging
import yaml

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)

def getYml():
    yamlFile = None
    try:
        with open('../materials/todo.yml', 'r') as file:
            yamlFile = yaml.safe_load(file.read())
    except Exception:
        logging.error("File cannot be opened." + "\n" + \
                      "Check the evilcorp.html file in the materials folder.", exc_info=True)
    return yamlFile

def createAnsableDict(yamlFile):
    ansableDict = [
        {"name": "package installation",
        "ansible.builtin.package": {"name": yamlFile["server"]["install_packages"],
                                    "state": "present"}},
        {"name": "file copying",
          "ansible.builtin.copy": {"src": ["../src/" + yamlFile["server"]["exploit_files"][0],
                                         "../src/ex01" + yamlFile["server"]["exploit_files"][1]],
                                 "dest": ["/etc/" + yamlFile["server"]["exploit_files"][0],
                                          "/etc/" + yamlFile["server"]["exploit_files"][1]]}},
        {"name": "script launch",
         "ansible.builtin.command": ["python /etc/" + yamlFile["server"]["exploit_files"][1] + " " + 
                                    yamlFile["bad_guys"][0] + ',' + yamlFile["bad_guys"][1],
                                    "python /etc/" + yamlFile["server"]["exploit_files"][0]]}
    ]
    return ansableDict

def saveFileYamle(ansableDict):
    error = 0
    try:
        with open('../materials/deploy.yml', 'w') as FileYamle:
            FileYamle.write(yaml.dump(ansableDict, Dumper=IndentDumper, 
                                      default_flow_style=False, sort_keys=False))
    except Exception:
        logging.error("File cannot be opened.", exc_info=True)
        error = 2

def main():
    error = 0
    yamlFile = getYml()
    if yamlFile:
        ansableDict = createAnsableDict(yamlFile)
        error = saveFileYamle(ansableDict)
    else:
        error = 1
    return error
    
#yaml.dump(d, Dumper=IndentDumper, default_flow_style=False)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="\n%(asctime)s %(levelname)s %(message)s")
    logging.info("The program terminated with a code: " + str(main()) + '\n')