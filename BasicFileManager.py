import shutil as st # This will be needed once we start working on actual file operations
import pathlib as pl
import tabulate as tbl
import subprocess as sbp

path = pl.Path.home()

while True:
    action = input(str(path) + " ")
    if action == "help" or action == "h":
        print(tbl.tabulate([["\"help\" or \"h\"", "Brings up this"], ["\"list\" and \"ls\"", "List files in the current directory"], ["\"exists\" and \"ex\"", "Check if a directory or file exists. Please be sure to enter the command followed by the directory seperated by a space. If entering a new directory connected to the current directory, put a \"~\" character right before the path. Ex. \"~/path/to/directory\""], ["\"changedir\" and \"cd\"", "Change the directory. Please be sure to enter the command followed by the directory seperated by a space. If entering a new directory connected to the current directory, put a \"~\" character right before the path. Ex. \"~/path/to/directory/\""], ["\"run\"", "Runs a new process in the current directory. Arguments come after the \"run\" command. Ex. run [example]"]], headers=["Command", "Purpose"]))
    elif action == "list" or action == "ls":
        FileTable = []
        for x in path.iterdir():
            FileToAdd = [str(x).split("/")[len(str(x).split("/")) - 1]]
            if pl.Path.is_dir(x) == True:
                FileToAdd.append("Folder/Directory")
            elif pl.Path.is_file(x):
                FileToAdd.append("File")
            ParentDirectory = str(x.absolute()).split("/") #[len(str(x.absolute()).split("/")) - 1]
            FileToAdd.append("/".join(ParentDirectory))
            FileTable.append(FileToAdd)
        FileTable.sort()
        print(tbl.tabulate(FileTable, headers=["Name", "File Type", "Complete Path"]))
    elif action[:action.find(" ")] == "exists" or action[0:action.find(" ")] == "ex":
        if action[action.find(" ") + 1] == "~" and pl.Path(str(path) + "/" + action[action.find(" ") + 2:]).is_dir():
            directory = pl.Path(str(path) + "/" + action[action.find(" ") + 2:])
        else:
            directory = pl.Path(action[action.find(" ") + 1:])
        if pl.Path(directory).exists():
            if (pl.Path(directory).is_dir()):
                print("The folder/directory " + str(directory) + " exists")
            elif (pl.Path(directory).is_file()):
                print("The file " + str(directory) + " exists")
        else:
            print(str(directory) + " does not exist or the command is incomplete")
    elif action[:action.find(" ")] == "cd" or action[0:action.find(" ")] == "changedir":
        if action[action.find(" ") + 1] == "~" and pl.Path(str(path) + "/" + action[action.find(" ") + 2:]).is_dir():
            path = pl.Path(str(path) + "/" + action[action.find(" ") + 2:])
        elif pl.Path(action[action.find(" ") + 1:]).is_dir():
            path = pl.Path(action[action.find(" ") + 1:])
        else:
            print("Please enter a a valid path")
    elif action[:action.find(" ")] == "run": # Note that from my testing, this part isn't actually working due to file permission issues. I am currently looking into a solution for this.
        if action.find("sudo") != -1:
            confirm_operation = True
            print("You are going to execute a command in sudo mode. This is a potentially dangerous operation that can cause damage to your files or computer. Are you sure you want to continue? ", end="")
            while True:
                user_input = input("\"Y/y\" for yes or \"N/n\" for no: ")
                if user_input.lower() == "y":
                    confirm_operation = True
                    break
                elif user_input.lower() == "n":
                    confirm_operation = False
                    break
                else:
                    print("Please enter a valid option")
                    continue
        if confirm_operation:
            try:
                sbp.run([str(path), action[action.find(" ") + 1:]])
            except Exception as e:
                print("An error occurred in the subprocess. " + "Error: " + str(e))
        else:
            print("Operation aborted")
    else:
        print("The entered input is invalid or incomplete. Type \"help\" or \"h\" for more information")