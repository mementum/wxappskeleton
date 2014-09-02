wxappskeleton
=============

Skeleton wxPython application including executable generation
with pyinstaller and setup generation with innosetup

Console applications can also be generated

Modify appconstants.py with the application information and
place a your start code in a main.py[w] or appname.py[w] file.
(appname stands for the name you configure in appconstants.py)

To add items to the executable/setup installation you can
modify build_utils and change the copy_items dictionary

Additional variables can be fine tuned in build_utils to
modifiy directory names, files to be cleaned before generation
and others

