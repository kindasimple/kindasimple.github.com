---
title: Installing R Packages
author: evan
categories: [dev]
tagline: 'The most simple way to install R packages'
---
I see people give a lot of reasons for liking R. Good open source tools are always great. A good library of packages for you to use is a reason often given. I went exploring for some real life applications of R, and found some mapping packages. Then I was faced with installing them.

The easiest way that I found to install a package is through RStudio. You can use it as a package manager to search for a package that you need with autocomplete, install the package, and install the package dependencies.

## Installing a package directly

After you download a tarball, you can install it like so

```
R CMD INSTALL path/to/file/filename.tgz
```

If there are project dependencies, you will have to track down each one individually so I wouldn't recommend this approach unless the package isn't available on CRAN or

## Install with install.packages()

Well known packages can be installed from the CRAN repository from within R. Running R from the terminal, choose a mirror with

```
chooseCRANmirror(81)
```

Choose a nearby mirror to download packages from. Then, installing a package and its dependencies is as simple as

```
install.packages(package_name)
```

## packages

sqldf

http://stackoverflow.com/questions/11488174/how-to-select-a-cran-mirror-in-r
