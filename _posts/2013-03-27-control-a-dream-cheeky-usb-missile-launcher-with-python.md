---
title: Control a Dream Cheeky USB Missile Launcher with Python
author: Evan
layout: blog 
categories:
  - Programming
  - Technology
tags:
  - Build Server
  - Hardware
  - Programming
  - Python
  - Raspberry Pi
---
 [1]: http://www.raspberrypi.org/
 [2]: https://github.com/codedance/Retaliation
 [3]: http://www.outletpc.com/lf4254-usb-782-generic-usb-foam-missle-launcher.html
 [4]: http://pyusb.sourceforge.net/
 [5]: https://github.com/sudar/MissileLauncher/blob/master/tools/missile-launcher.py
 [6]: http://www.jetbrains.com/teamcity/
 [7]: http://jenkins-ci.org/
I had the idea to set up my [Raspberry Pi][1] as a build server.  Google, perhaps knowing me too well, led me to [an interesting project][2] that uses a USB Missile Launcher to indicate broken builds by launching missiles at the offending programmer.  I just happen to own a [missile launcher][3] of a different model created by the same company, and so how could I not give this project a go?

![Dream Cheeky Missile Launcher](https://kindasimple.s3.amazonaws.com/wp-content/uploads/2013/03/MissileLauncher.jpg "A picture of a usb missile launcher")

There was a bit of setup.  My laptop running Ubuntu was the Hardy Heron release and several cycles behind the current release *Quantal Quetzal*.  I ended up doing a clean install.

The script to control the USB Missile launcher is in Python and depends on [PyUSB][4] for hardware IO.  The vendor and product ID codes were slightly different, but [were documented  elsewhere][5].

```
#New Model
usb.core.find(idVendor=0x2123, idProduct=0x1010)
#My Older Model
usb.core.find(idVendor=0x0a81, idProduct=0x0701)
```

I&#8217;m not big into Python, so debugging this script was foreign to me.  I found some [documentation][5] and with a few imports and commands I learned n = next, c = continue&#8230;enough to be dangerous.  And so I modified the script and submitted my first Github Pull Request.

I checked out both [TeamCity][6] and [Jenkins.][7] I really like them both, finding Jenkins easier to configure and TeamCity more feature rich.  Each one supports Git polling, though I havn&#8217;t yet looked into setting up the Continuous Integration part of the build server&#8211;triggering automated builds on each commit.  Then theres the matter of connecting my Raspberry Pi wirelessly.  So, there is more work to do and more to come!

Update: Pull request merged!
