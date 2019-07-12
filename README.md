# Game
Python Script to free hand on playing Onmyoji
# Description
Use opencv to detect the template pictures in the screen shot of the simulator, and then make some actions according to user's demand.  
Baidu OCR API is an auxiliary approach to help detect the numbers of some perticular loctions of the screen shot.  
In all, the goal is to free your hand on the tedious operations.  
Multithreading is supported, which means you can open as much players as your can and then run them in whatever team mode or solo mode in the same time.  
# Platform
Windows 10 x86_64 (Only tested on this)
# Software
[Thunder Andriod Simulator](https://www.ldmnq.com) Version 3.5+
# Python and python package requirements
Python 3.6+  
opencv  
numpy  
re  
(for more detail please check the source code)
# Code Structure
+ Game
	+ Crack_Onmyoji
		+ logs (Store logs)
		+ instruction ( config.txt is required to store Baidu OCR API Key)
		+ old (Deprecated)
		+ Onmyoji_images (Match template pictures)
		+ test (For test)
		+ crack_onmyoji.py (Code entry, highest level)
		+ log_recorder.py (Write log, util)
		+ onmyoji.py (Onmyoji class to store some global in-game properties and account info)
		+ thunder_controller.py (service, action level)
		+ thunder_player.py (Player class to store player info) 
# Functionality
1. Awakening and Mitama automation in team mode  
2. Original Fire (bad translation xd) automation in solo mode  
3. Personal Breakthrough automaton  
4. Chapter automation in solo mode
# Developing Plan
1. add more functions
2. add gui (maybe xd)
