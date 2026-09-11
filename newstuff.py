# import os
# import time
# from pathlib import Path
# import shelve
# import pprint
# import shutil
# import os
# import send2trash
# import zipfile
# import openpyxl
# os.chdir("C:\\Windows")
# print(os.getcwd())
# print(Path.home())
##Why we need to know all of this is because everyone programs well but they dont understand how to
#perform file management and how to find root and stuff
# p1 =  Path("spam/eggs")
# p2 = Path("C:/Windows")
# print(p1.is_absolute())
# print(p2.is_absolute())
# rel =  Path("spam/eggs")
# abs_Path = Path.cwd() / rel
# print(abs_Path)
# p = Path("C:/Users/Admin/Documents/report.pdf")
# print("Anchor :",p.anchor)
# print("Parent :",p.parent)
# print("Name : ",p.name)
# print("Stem : ",p.stem)
# print("suffix : ",p.suffix)
# print("----------------------------------------------------------------------")
# print(p.parts)
# print(p.parents[0])
# print(p.parents[1])
# print()
#Doubt:can you find the number of sub directories like you can find the length of a string?
# #there is no way to do it in path but maybe in another function
# p = Path("sample123.txt")
# if p.exists():
#     stats = p.stat()
#     print(stats.st_size)
#     print(stats.st_mtime)
#     print(stats.st_ctime)

# realtime = time.ctime(stats.st_ctime)
# print(realtime)
# for file in Path(".").glob("sample???.txt"):
#      print(file)
# from pathlib import Path
# p = Path("spam.txt")
# chars = p.write_text("Hello,World!",encoding = "utf - 8")
# # print(chars)
# # content = p.read_text(encoding = "UTF-8")
# # print(content)
# file = open("spam.txt","r",encoding = "utf-8")
# data = file.read()
# file.close()           
# print(data)
# file = open("spam.txt","w+",encoding="UTF-8")
# file.write("Helllo,world!\n")
# file.close()
#shelve module brings a concept of shelves which is basically dictionaries 
#but dictionaries only are active when the program is open and is disabled when the program is turned off
#so we create a dictionary object using shelve module to create a permanent dictionary. and the object is called shelf.
# shelf = shelve.open("mydata")
# shelf["Cats"]=["Zophie","Milo","Asteroiddestroyer"]
# print(list(shelf.keys()))
# print(list(shelf.values()))
# shelf.close
# cats = ["Zophie","Pooka","Simon"]
# data = pprint.pformat(cats)

# with open("cats.123","w") as f:
#     f.write("cats ="+data)
# shutil.copy("spam.txt","notes.txt")
# shutil.copytree("bms1","bmsbkup1")
# shutil.move("spam.txt","spam321.txt")
# print(os.listdir("."))
# for folder,subfolder,files in os.walk("."):
#     print(folder)
#     print(subfolder)
#     print(files)
# with zipfile.ZipFile("bmist.zip","w",compression = zipfile.ZIP_DEFLATED) as Z:
#     Z.write("cats123.txt")

# with zipfile.ZipFile("bmist.zip") as Z:
#     print(Z.namelist())

# with zipfile.ZipFile("bmist.zip") as Z:
#     Z.extractall("extracted_files")

# NOTE: Backslashes in Windows paths are treated as escape sequences in normal
# Python strings. Use one of these approaches to avoid that:
#  - Raw string: r"C:\Users\..." (used below)
#  - Escape backslashes: "C:\\Users\\..."
#  - Forward slashes: "C:/Users/..."
#  - Use pathlib.Path, which avoids manual escaping and is cross-platform.

# from pathlib import Path as _Path

# excel_path = _Path(r"C:\Users\Sai Suhas Maddali\Downloads\file_example_XLS_10.xls")

# openpyxl reads .xlsx files. If you have a legacy .xls file you can:
#  - convert it to .xlsx, or
#  - use pandas with an appropriate engine (e.g. 'xlrd' for older pandas/engines),
#    or use the 'xlrd' package directly for .xls files.
# if excel_path.suffix.lower() == ".xls":
# 	print("Warning: file has .xls extension — openpyxl supports .xlsx only.")

# try:
# 	# pass a string path (Path objects are accepted by many libraries too)
# 	wb = openpyxl.load_workbook(str(excel_path))
# except Exception as e:
# 	print(f"Failed to open workbook '{excel_path}': {e}")
# 	wb = None
# wb =openpyxl.load_workbook("file_example_XLS_10.xlsx")
# print(wb.sheetnames)

# sheet = wb.active
# print(sheet["A1".value])

# for row in sheet.rows:
#     for cell in row:
#         print(cell.value)
        