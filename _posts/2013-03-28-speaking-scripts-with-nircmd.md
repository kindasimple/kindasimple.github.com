---
title: Speaking Scripts With NirCmd
author: Evan
layout: blog 
categories:
  - Command Line
tags:
  - Build Script
  - Command Line
  - Scripting
  - TTS
---
 [1]: The windows http://www.nirsoft.net/utils/nircmd.html
Nir Sofer has written a fun utility that I have been using to make my scripts talk.  Its called [nircmd.exe][1]

> NirCmd is a small command-line utility that allows you to do some useful tasks without displaying any user interface. By running NirCmd with simple command-line option, you can write and delete values and keys in the Registry, write values into INI file, dial to your internet account or connect to a VPN network, restart windows or shut down the computer, create shortcut to a file, change the created/modified date of a file, change your display settings, turn off your monitor, open the door of your CD-ROM drive, and more&#8230;
> 
> http://www.nirsoft.net/utils/nircmd.html

Text-To-Speach is available at least as far back as Windows XP. I&#8217;m not sure how to call it directly, but using nircmd it is as simple as

```
nircmd speak text "Hello" 2 60
```

The parameters are the speed and the volume of the narrator. To add narration to my scripts I call :SPEAK instead of echo to write to the console.

```
REM =====================================================================
REM = SPEAK - vocalize command
REM =====================================================================
:SPEAK
where nircmd.exe /Q
if %errorlevel% neq 0 ( 
echo %~1 
) else (
nircmd speak text "%~1" 2 60
)
EXIT /B
```

When handling exceptions during my build scripts, I use this :NOTIFICATION routine to call my speech routine to alert me if I am within earshot.

```
REM =====================================================================
REM = NOTIFY - indicate failure
REM =====================================================================
:NOTIFY
echo Error occurred with code %~1
CALL :SPEAK "Error occurred with code %~1"
SET Error=%~1
EXIT /B
```

After executing MSBuild, I check for errors and notify myself audiably if there is a problem.

```
if %errorlevel% neq 0 CALL :NOTIFY %errorlevel%
```