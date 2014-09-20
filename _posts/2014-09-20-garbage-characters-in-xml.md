---
title: Garbage Characters in XML
author: Evan
layout: blog
categories:
  - Running
  - Data
tags:
  - command line
---
Polar's GPS often takes time to establish a satellite connection and retrieve a position. After export a "strange character" sits in the time node, causing jquery's xml parser to choke and die.

![gpx](https://www.dropbox.com/s/vft9ev36r1ifvim/Screenshot%202014-09-20%2015.18.49.png?raw=1)

there are options to filter unwanted characters in preprocessing using `sed` and `awk`.

    sed -i '.orig' 's/[^[:print:]]//'  13011601.gpx
    perl -i.bak -pe 's/[^[:print:]]//g' 13011601.gpx

I don't want a general filter that could have other side effects. I want to target the character thats causing me problems. A helpful stack overflow post suggested that I revisit Joel Spolsky's article,  [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets](http://www.joelonsoftware.com/articles/Unicode.html). I don't often mess with character encodings, so I'm not positive where to begin.

I get the hex values for each character, and do a search for the hex value "30", a zero, to find the 0.0000000 coordinate readings for the "trkpt" node

    hexdump 13011601.gpx

![less](https://www.dropbox.com/s/poikcom4lrj5qwf/Screenshot%202014-09-20%2015.31.03.png?raw=1)

Just below is the hex value `1e`, which is a special ASCII character for a record separator. Its probably no cooincidence that the decimal vaule for a record separater of the same as the hex value for a zero.


[![Table](https://www.dropbox.com/s/dn3qdt5ow9fy0py/Screenshot%202014-09-20%2015.14.01.png?raw=1)](http://www.asciitable.com/)

Now I can target and remove the record separater by using tr to remove the bothersome character.

    $ tr -d '\036' < 13011601.gpx | head -n15
    <?xml version="1.0" encoding="UTF-8"?>
    <gpx
    version="1.0"
    creator="Polar ProTrainer 5 - www.polar.fi"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.topografix.com/GPX/1/0"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
    <time>2013-01-16T07:25:50Z</time>
    <trk>
    <trkseg>
    <trkpt lat="0.000000000" lon="0.000000000">
    <time></time>
     <fix>none</fix>
     <sat>0</sat>
    </trkpt>

