# YAFastbootAdbGUI
Yet another adb/fastboot GUI

![ui](img/ui2.png)


# Why this

Uhhhhh
1. made in python
2. made with pydeargui
3. more or less like a side project lmao

# Install / compile
Just run the exe file, OR if you are on linux / want to compile

```
git clone --depth=1 --recursive https://github.com/Ricca665/YAFastbootAdbGUI
make libraries #To update libraries, only required if compiling or running on linux
pip install -r requirements.txt # If you don't want to redo this file
```
On linux after those commands you MUST use this:

```
python src\main.py
```

But if you want to compile an executable:
```
make program #To compile only for windows
```
# Windows defender flagged this as malware... is this a virus???
No, i don't even know myself why it flags it as malware (probably because of subprocess), but it isn't
If you don't belive me, look throught the code, it's not malware

# FAQ
Q: It doesn't work (throws Access is denied)
A: Run it as administrator
# I DON'T TAKE RESPONSIBILITY FOR ANY BRICKED DEVICES, DEAD RAMS, EXPLOSIONS, ETC...
