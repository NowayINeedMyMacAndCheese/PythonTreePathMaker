Tree Path Generator

WARNING THE SCRIPTS HAVE ERRORS THEY CAN ONLY BE RUN LOCALLY IM SORRY FOR THIS inconvenience

This tool helps you create a visual tree path from your directory structure. It works by listing all files and folders, 
then converting that list into a readable tree format using a Python script.

Step 1: Generate the File List
Use one of the following methods to create filelist.txt:

Option 1: Use Provided Scripts
Run the included generate_filelist.bat (for CMD) or generate_filelist.ps1 (for PowerShell) to automatically generate filelist.txt.

Option 2:  Use a Command Manually

PowerShell:

Get-ChildItem -Recurse -Force | Select-Object -ExpandProperty FullName > filelist.txt

CMD:

dir /a /s /b > filelist.txt

Step 2: Generate the Tree Path

After filelist.txt is created, run the Python script

Example Output
markdown
C:\/
└── Users
    └── koosh
        └── Desktop
            └── pythonpathmaker
                ├── FileListMaker.ps1
                ├── FilelistMaker.bat
                ├── Pythonpathmaker.py
                ├── ReadMe.txt
                ├── filelist.txt
                └── pythonpathmaker
                    └── filelist_pathtree.txt

