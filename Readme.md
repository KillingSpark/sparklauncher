SparkLauncher
=============
The bestestes launcher in the whole universe WoopDee$$$$ingDoo

# Search all yours Apps! #
Just type parts of the name and your faithful launcher will find your hearths desire
![](https://i.imgur.com/Mkq6WyE.png)

# Search your Files! #
Preface with a ~ + _space_ to search through your home directory or with a / + _space_ for your whole file system.
you only need to type parts of the name of your directory/file and it will be found
![](https://i.imgur.com/4S7lBKy.png)
![](https://i.imgur.com/5tf3zih.png)

# Search your Bookmarks (chrome and chromium) #
Preface with # + _space_ to search through your bookmarks

# Use as a calculator #
Type ! + _space_ and then insert your calculation you are too lazy to do in your head!

# It is learning! #
The launcher remembers which apps/files/directories you start/open and gives the one you like the most first

# Favorites without typing! #
The most started apps will be in the list without having to type anything
![](https://i.imgur.com/wylD6Zl.png)

# Customization is a thing!
settings.py holds all the available settings. Get Wild!
![](https://i.imgur.com/qwe4Lhh.png)

# Installing #
Sorry no install script yet, just put it anywhere, make main.py executable and have fun
Maybe set a keyboard shortcut or whatever. 

Depends on:  
1. PyGObject, refer to their installing manual: [python-gtk3-installing](https://python-gtk-3-tutorial.readthedocs.io/en/latest/install.html)  
2. pyxdg (in pip) or python-xdg (in ubuntu repos) or get it from their website: [pyxdg](https://freedesktop.org/wiki/Software/pyxdg/)  
3. xdg-open but that should be installed anyways by your distro

# Usage #
The first time you open main.py it may take a second to load everything
but after that the daemon is running and it will open immediatly.  
After the daemon is running you can send some signals to the Launcher:  
1. call the main.py again without args: show the window
2. main.py hide: hides the window
2. main.py reload: reloads the desktop entries + bookmarks (needed if something changed)
2. main.py kill: kills the daemon if needed/wanted. Needed to reload the styles if you are trying out some themeing

# Notes #
In your ~/.config/sparklauncher directory will be a file .sparklauncher which holds the info what you started how often. Delete it to reset or edit
the numbers to set the apps you want to have on the "front page".
If the launcher crashes maybe the lockfile that prevents multiple instances might be still there preventing it from opening,
delete /tmp/.sparklauncherlock to make it available again. this shouldnt happen tho.


