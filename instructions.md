# Instructions

## GBShell.py

Usage： ./GBShell.py  [OPTION]...  [FILE]...  [LABEL/KEY:value]

Description：a command line ，users can operate on this to controll the whole GBFS.

​	   -a, --add

​			Add a label [LABEL] in the given file [FILE]

​	   -d, --delete

​			Delete the label [LABEL] in the given file [FILE].If the given file doesn't have that label,deleting

​		is invaild,and return a warning signal.

​	   -f, --find

​			User gives shell the labels [LABEL] or the proporties [KEY:value],and all the nodes that

​		have the given labels or proporties are printed in the screen.If none node meets 

​		the requirements,Not Found will be returned.

​	    -h, --help

​			Show the help info.

​	    -l, --showlink

​			Print all the files(nodes) that are adjacent to the given file[FILE].

​	    -r, --rec

​			Recommend.

​	    -s, --show

​			Print all the labels and proporties of the given file [FILE]. 