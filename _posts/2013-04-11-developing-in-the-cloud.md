---
title: Developing in the Cloud
author: Evan
layout: blog 
categories:
  - Programming
  - Technology
tags:
  - Amazon
  - Cloud
  - Programming
---
 [1]: https://c9.io/
 [2]: http://www.cloudshare.com/
 [3]: http://bitnami.com/
 [4]: http://www.teamst.org/
 [5]: redmine.org
 [6]: http://aws.amazon.com/
 [7]: http://programmers.stackexchange.com/questions/33955/using-ec2-instance-as-main-development-platform
 [8]: http://blog.michaelckennedy.net/2011/06/13/building-a-cloud-os-for-net-developers-part-2/
I want to move my development environment to the cloud.  My current setup is poor for a lot of reasons. I have a 120 SSD with half the space dedicated to a Windows 7 instance and the other half being taken up by a Windows 8 VHD.  Both are cluttered, and reaching their storage limits.  What I would like to have is a well curated development environment to do C# development for Windows Mobile apps.  Going to the cloud and taking advantage of accessibility and scalability is exactly what i am looking for.

With Citrix I could create my own local cloud but I find Amazon AWS & Azure much more promising.  There are plenty of ways to get your web development into the cloud through online services.  [Cloud9ide][1] provides a web development environment.  [Cloudshare][2] gives access to a cloud development platform for Beta Microsoft products.

To speed up setup we can use [Bitnami][3] for downloading open source stacks that can be hosted in the AWC cloud or on your local PC.  For a fee, Bitnami will host your environment for you, but for gree you can test out the packages for an hour.  I explored a test instance of [TestLink][4] for creating test plans, which led me to explore some comparable solutions such as [Redmine for Project Management][5] and [RTH &#8211; Requirements and Testing Hub](http://sourceforge.net/projects/rth/).

[Amazon&#8217;s AWS][6] offers a 1 year trial for a micro-instance that has enough computing power, storage, and bandwidth to run a website or web service, making it a great option for testing.  There are options for both Linux and Windows.

What is most encouraging is that people are [already moving their development environment to the cloud][7], and the costs seem to be under control as long [as you aren&#8217;t careless][8].