# ProxyBeuker
## Batch Convert RED Digital Cinema .R3D to ProRes video files using ProxyBeuker

<img src="https://repository-images.githubusercontent.com/113862704/d2fb0700-8586-11ea-8bd1-a6900d5898d2" width="50%" height="50%">
<img src="https://proxybeuker.com/images/5f6ca3a50cf73174242b66e8_proxy-beuker-mockup-2-1.jpg" width="50%" height="50%">

ProxyBeuker helps with a quick proxy workflow for video editing. Creating proxies in Adobe Media Encoder or Resolve takes time. You have to import files, configure presets etc... 

Proxybeuker scans your import folder for all RED .R3D files and  starts converting them right away to FullHD ProRes LT files. It takes 3000 files as easily as 30. 

You need to have RedCine-X installed for it to work. The build is for OSX only at the moment. 
Build the tool on OSX with PyInstaller or grab it from the dist directory. 

    PyInstaller --onefile -y --icon=ico.icns --windowed proxybeuker.py
      
More info:
https://www.proxybeuker.com
