---------------------------READ ME---------------------------
Program: wholeTile
Version: 3.2
Created by B.Wu
Date: 2019-04-26

--------------------------INSTRUCTION------------------------

For identifying whole tiles in Takeoffs: 
1. Save a screenshot of your DWG model over white background (including the boundaries and tiles hatch)
	- PNG has better resolution then JPEG and is recommended
2. Running from Commend Line Prompt: Navigate to the correct file address, copy the file address after "cd "
    (e.g. cd C:\Users\Interns PC\Desktop\workspace\Python) and press Enter
3. Type in "wholeTile-v3.1.exe -f <filename.filetype>" (e.g. wholeTile-v3.1.exe -f test.png), and press Enter
	- Pressing "TAB" autofills filenames with extension
4. A PNG called "<filename>-##.png" will be saved under the file address, with ## being the number of whole tiles detected.
5. Click into the output picture to verify/edit tile numbers.

Note: Verify the number of tiles from "square.png" every time. Some perimeter tiles that are very close to a square 
      may pass the threshold (Line 54) and get counted towards whole tiles. 

List of Commends:
	-h --help: help
	-f --file <filename.filetype>: enter input file name

--------------------------KNOWN ISSUES-----------------------

- JPEG might not have enough resolution to return correct answers

-------------------------------------------------------------