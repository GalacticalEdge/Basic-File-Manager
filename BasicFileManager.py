import shutil as st # This will be needed once we start working on actual file operations
import pathlib as pl
import tabulate as tbl

path = pl.Path("/")

while True:
    action = input(">>>")
    if action == "help" or action == "h":
        print("\"help\" and \"h\": Brings up this\n\"list\" and \"ls\": List files in the current directory\n\"exists\" and \"ex\": Check if a directory or file exists\n\"changedir\" and \"cd\": Change the directory. Please be sure to enter the command followed by the directory seperated by a space\n\"copy\": Copy a file to another file or directory")
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
        if pl.Path(str(path) + "/" + action[action.find(" ") + 1:]).is_dir():
            directory = pl.Path(str(path) + "/" + action[action.find(" ") + 1:])
        else:
            directory = pl.Path(action[action.find(" ") + 1:])
        if pl.Path(directory).exists():
            if (pl.Path(directory).is_dir()):
                print("The folder/directory " + str(directory) + " exists")
            elif (pl.Path(directory).is_file()):
                print("The file " + str(directory) + " exists")
        else:
            print(directory + " does not exist or the command is incomplete")
    elif action[:action.find(" ")] == "cd" or action[0:action.find(" ")] == "changedir":
        if pl.Path(str(path) + "/" + action[action.find(" ") + 1:]).is_dir():
            path = pl.Path(str(path) + "/" + action[action.find(" ") + 1:])
        elif pl.Path(action[action.find(" ") + 1:]).is_dir():
            path = pl.Path(action[action.find(" ") + 1:])
        else:
            print("Please enter a a valid path")
    else:
        print("The entered input is invalid or incomplete. Type \"help\" or \"h\" for more information")