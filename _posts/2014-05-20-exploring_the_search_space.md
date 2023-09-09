---
title: Exploring the Search Space
author: evan
categories: [dev]
tags: [search, python, kml, heuristic, AStar]
tagline: 'Implementation of different search algorithms'
header:
  image: /assets/images/header-exploring-the-search-space.png
  teaser: /assets/images/header-exploring-the-search-space.png

---
 [google-map]: https://maps.google.com/maps?q=http%3A//kindasimplesolutions.com/assets/kml/astar_dijkstra.kml "Search results on google maps"
 [sort]: http://kindasimplesolutions.com/blog/upsifting-heapsort/ "df"
 [SO-point-line-distance]: http://stackoverflow.com/questions/849211/shortest-distance-between-Basht-and-a-line-segment "dsf"
 [google-fusion-tables]: https://support.google.com/fusiontables/answer/2571232 "df"
 [dijkstras-algorithm]: http://en.wikipedia.org/wiki/Dijkstra's_algorithm "adf"
 [dijkstras-algorithm-animation]: http://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif
 [a-star]: http://en.wikipedia.org/wiki/A*_search_algorithm "A* search on wikipedia"
 [github-search]: https://github.com/kindasimple/play/tree/master/python/search "Seach code in python on Github"
 [search-result]: http://kindasimplesolutions.com.s3.amazonaws.com/images/search-kml/search-result.png
 [search-dijkstra]: http://kindasimplesolutions.com.s3.amazonaws.com/images/search-kml/dijkstra-search-path.png
 [search-astar]: http://kindasimplesolutions.com.s3.amazonaws.com/images/search-kml/astar-search-path.png
I moved on from [sort][sort] to search and implemented a few search algorithms in python from pseudocode on wikipedia. I coded a simple backtracking algorithm as well as Dijkstra's and an A* search.

![Search Result][search-result]

## Dijkstra's algorithm

[Dijkstra's algorithm][dijkstras-algorithm] searches by traversing the nodes by calculating the cumulative distance to the nearest neighbor and travelling to the node with the minimum cumulative distance. The algorithm keeps track of the minimum cumulative distance calculated for each vertex.

![Dijkstra's Algorithm Animation][dijkstras-algorithm-animation]

Source: [Wikipedia](http://en.wikipedia.org/wiki/File:Dijkstra_Animation.gif)

The brute force backtracking algorithm that I implemented overflowed the stack frame with a graph of a few thousand nodes, while Dijkstra's algorithm had no problems. I moved onto an A* search which was familiar from my college days.

![Dijkstra Search Result][search-dijkstra]

## A* search

[A*][a-star] It is essentially Dijkstra's algorithm that chooses a path based on a heuristic evaluation of neighbors. My heuristic was to score neighbors on how close they are to a line segment that runs from the start to the finish. The math for points and lines in vector space is abstract and not so familiar. I started reading webpages on math for parametric equations and quickly moved onto this [Stack Overflow thread][SO-point-line-distance] where the code was pretty opaque and many answers incorrect. I ended up using this answer which seemed the most strait-forward.

```python
  def dist2line2(x,y,line):
     x1,y1,x2,y2=line
     vx = x1 - x
     vy = y1 - y
     ux = x2-x1
     uy = y2-y1
     length = ux * ux + uy * uy
     det = (-vx * ux) + (-vy * uy) #//if this is < 0 or > length then its outside the line segment
     if det < 0:
       return (x1 - x)**2 + (y1 - y)**2
     if det > length:
       return (x2 - x)**2 + (y2 - y)**2
     det = ux * vy - uy * vx
     return det**2 / length
   def dist2line(x,y,line): return math.sqrt(dist2line2(x,y,line))
```

The resulting A* search performs really well. I chose visual testing with kml and placemarks so I could see my answer on a map. My demo code generates fake cities around the world and generates edges to randomly connect vertices.

![A* Search Result][search-astar]

## Sources

The search output is formatted into KML which you can see on a [google map][google-map] (or import into [google fusion tables][google-fusion-tables] ). The source is [on Github][github-search]
