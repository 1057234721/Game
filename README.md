# Game
Python Script to free hand on playing Onmyoji
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
		+ crack_onmyoji.py (Code entry)
		+ log_recorder.py (Write log)
		+ onmyoji.py (Onmyoji class, stores some in-game properties)
		+ thunder_controller.py (Action level)
		+ thunder_player.py (Player class) 
