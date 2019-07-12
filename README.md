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
# Configuration
1.modify every Thunder Android Simulator's resolution to 1280 x 720.  
2.modify every Thunder Android Simulator's share path to the project's Onmyoji_images.  
3.modify ld.exe, ldconsole.exe path and share path in the thunder_controllor.py.  
4.create your own Baidu OCR API access_token and put it in the config section, under instruction/config.txt.  
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
		+ thunder_controller.py (Service, action level)
		+ thunder_player.py (Player class to store player info) 
# Functionality
1. Awakening and Mitama automation in team mode  
2. Original Fire (bad translation xd) automation in solo mode  
3. Personal Breakthrough automaton  
4. Chapter automation in solo mode
# Developing Plan
1. add more functions
2. add gui (maybe xd)
# Disclaimer
阴阳师™ (Onmyoji) is a brand which belongs to NetEase™ corporation (网易(杭州)网络有限公司).  
雷电模拟器™ (Thunder Android Simulator) is a brand which belongs to Shanghai Changzhi Internet Technology corporation (上海畅指网络科技有限公司).  
