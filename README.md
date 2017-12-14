What is this?
=============

2 Cars is an arcade game for the Sugar desktop.

How to use?
===========

2 Cars is part of the Sugar desktop.  Please refer to;

* [How to Get Sugar on sugarlabs.org](https://sugarlabs.org/),
* [How to use Sugar](https://help.sugarlabs.org/),
* [Download 2 Cars using Browse](https://activities.sugarlabs.org/), search for `Cars`, then download, and;
* Refer the 'How to play' section inside the activity

How to upgrade?
===============

On Sugar desktop systems;
* use [My Settings](https://help.sugarlabs.org/en/my_settings.html), [Software Update](https://help.sugarlabs.org/en/my_settings.html#software-update), or;
* use Browse to open [activities.sugarlabs.org](https://activities.sugarlabs.org/), search for `Cars`, then download.

How to run?
=================

2 Cars depends on Python, PyGTK and PyGame.

2 Cars is started by [Sugar](https://github.com/sugarlabs/sugar).

2 Cars is not packaged by Debian and Ubuntu distributions.  
On Ubuntu systems these required dependencies (`python-gtk2-dev` and
`python-pygame`) need to be manually installed.


**Running on Ubuntu**
- Install the dependencies - 
```
sudo apt install python-gtk2-dev python-pygame
```

- Clone the repo and run-
```
git clone https://github.com/sugarlabs/2-cars-activity.git
cd 2-cars-activity
python main.py
```

**Running inside Sugar**

- Open Terminal activity and change to the 2 Cars activity directory
```
cd activities\2Cars.activity
```
- To run
```
sugar-activity .
```
