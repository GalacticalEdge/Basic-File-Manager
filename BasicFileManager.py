import shutil as st # Used for specific file operations, such as copying, moving, and deleting files/directories (in particular, removing whole directories)
import pathlib as pl # Used for identifying file paths
import tabulate as tbl # Used to print information
import subprocess as sbp # Used for the "run" command
from send2trash import send2trash # Used for sending files to the trash
import os # Used for file operations that shutil does not have

path = pl.Path.home()

def ReturnPath(action, path, exist=True, filereturntype="both"):
    if filereturntype != "both" and filereturntype != "directory" and filereturntype != "file":
        print("A problem has occurred determining the file return type. Please report this bug.")
        return path
    
    if action[action.find(" ") + 1] == "~":
        TargetPath = pl.Path(str(path) + "/" + action[action.find("~") + 2:])
    else:
        TargetPath = pl.Path(str(action[action.find(" ") + 1:]))
    
    if exist == True:   
        if ((TargetPath.is_dir() or TargetPath.is_file()) and filereturntype == "both") or (TargetPath.is_dir() and filereturntype == "directory") or (TargetPath.is_file() and filereturntype == "file"):
            return TargetPath
        else:
            if filereturntype == "both":
                print("Please enter a valid directory or file path")
                return path
            else:
                print("Please enter a valid " + filereturntype + " path")
                return path
    else:
        if not TargetPath.is_dir() or not TargetPath.is_file():
            return TargetPath
        else:
            return path
        
# This is where the program's main execution occurs

while True:
    action = input(str(path) + " ")
    if action == "help" or action == "h":
        print(tbl.tabulate([["\"help\" or \"h\"", "Brings up this"], ["\"list\" and \"ls\"", "List files in the current directory"], ["\"exists\" and \"ex\"", "Check if a directory or file exists. Please be sure to enter the command followed by the directory seperated by a space. If entering a new directory connected to the current directory, put a \"~\" character right before the path. Ex. \"~/path/to/directory\""], ["\"changedir\" and \"cd\"", "Change the directory. Please be sure to enter the command followed by the directory seperated by a space. If entering a new directory connected to the current directory, put a \"~\" character right before the path. Ex. \"~/path/to/directory/\""], ["\"run\"", "Runs a new process in the current directory. Arguments come after the \"run\" command. Ex. run [example]"], ["\"trash\"", "Send a directory or file to the trash. Enter the directory after the command seperated by a space"], ["\"rm\" or \"remove\"", "Deletes a file permanently from the system. please use with caution"], ["\"mkdir\" or \"makedir\"", "Create a directory"], ["\"exit\"", "Quits the program"]], headers=["Command", "Purpose"]))
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
        path = ReturnPath(action, path, True, "directory")
    elif action[:action.find(" ")] == "run": # Note that from my testing, this part isn't actually working due to file permission issues. I am currently looking into a solution for this.
        try:
            # print(action[action.find(" ") + 1:].split(" ") + [str(path)])
            sbp.run(action[action.find(" ") + 1:].split(" "), cwd=path)
        except Exception as e:
            print("An error occurred in the subprocess. Error: " + str(e))
    elif action[:action.find(" ")] == "trash":
        try:
            PathToTrash = ReturnPath(action, path, True, "both")
            if str(PathToTrash) == str(path):
                pass
            else:
                send2trash(PathToTrash)
        except Exception as e:
            print("An error has occurred trying to move a directory/file to the trash. Error: " + e)
    elif action[:action.find(" ")] == "remove" or action[:action.find(" ")] == "rm":
        try:
            PathToDelete = ReturnPath(action, path, True, "both")
            if str(PathToDelete) == str(path):
                pass
            else:
                while True:
                    Warning = input("Are you sure you want to delete this path/directory permanently?: ")
                    if Warning.lower() == "y":
                        if PathToDelete.is_dir():
                            st.rmtree(PathToDelete)
                            break
                        elif PathToDelete.is_file():
                            os.remove(PathToDelete)
                            break
                    elif Warning.lower() == "n":
                        print("Operation Aborted")
                        break
                    else:
                        print("Please enter a valid option")
                        continue
        except Exception as e:
            print("An error has occurred trying to delete a directory/file. Error: " + e)
    elif action[:action.find(" ")] == "makedir" or action[:action.find(" ")] == "mkdir":
        NewDirectory = ReturnPath(action, path, False, "directory")
        if str(NewDirectory) == str(path):
            pass
        else:
            os.mkdir(NewDirectory)
    elif action == "exit":
        exit()
    else:
        print("The entered input is invalid or incomplete. Type \"help\" or \"h\" for more information")