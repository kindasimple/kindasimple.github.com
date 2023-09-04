---
title: Doing Data Science
author: evan
categories: [dev]
tagline: 'finding data to visualize'
---

I took a short four week course on the R programming language. R is open source and there is a community that contributes packages which can be found on CRAN.org. There is great support for visualizationsn with easy to create graphs, maps, and some custom graphics such as word clouds or node maps.

I have also been dabbling with some unix programs and set myself to create some shell scripts to do something cool with R. My first attempt to consume some public API is the ____ for earthquake data.

There are feeds available in both XML and json. I am making use of cUrl to request a feed regularly.  I set up a daily script to request earthquake data and store it in a database. Then, on request I can query the data, parse it with jq, and throw a data set to a file that can be loaded into R to create a map of seismic activity.
