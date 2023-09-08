---
title: Upsifting in a Heapsort
author: evan
categories: [dev]
tags: [sorting, python]
tagline: 'upsorting in a heapsort'
header:
  image: assets/images/header-upsifting-heapsort.png
---
While trying to implement a heapsort in python I came across pseudocode that communicated that sifting up and sifting down to build the heap are different approaches to the same things. They both work well for creating a heap. Sifting down will move the element to a sorted position in the tree. Sifting up will move single leaf up to a lower level of the tree.

## Implementation

```
function siftUp(a, start, end) is
     input:  start represents the limit of how far up the heap to sift.
                   end is the node to sift up.
     child := end
     while child > start
         parent := floor((child - 1) / 2)
         if a[parent] < a[child] then (out of max-heap order)
             swap(a[parent], a[child])
             child := parent (repeat to continue sifting up the parent now)
         else
             return
```

The Psuedocode from [Wikipedia](http://en.wikipedia.org/wiki/Heapsort) shows a full implementation with up sifting, and then shows the downsifting code--seeming to indicate that a call to siftdown() and siftup() are interchangeable. After a heapsort swap our heap is damaged and while sifting down will repair the heap, sifting up will not.

After the swap that puts the largest (root) item in the last (sorted) position of the array, sifting down will repair the damaged heap by placing the new root (the swapped leaf) into a correct position. Sifting down runs in O(n) while sifting up doesn't fare as well running O(n log n), so sifting down probably preferred.

![Heapsort Animation](http://upload.wikimedia.org/wikipedia/commons/4/4d/Heapsort-example.gif)

## Heapsort with Downsifting

Source: [Wikipedia](http://en.wikipedia.org/wiki/File:Heapsort-example.gif)

Sifting up will simply look at the last item of the heap and check to see it needs sifting! For our broken heap, this will only cause a swap if the leaf is one level deep and it won't necessarily repair the tree. I discovered this on my own, [as have others](http://stackoverflow.com/questions/16574962/why-doesnt-my-heapsort-work). Its an easy mistake to make, especially from sources that seem confused themselves.

Here's some pseudocode taken from the web

```
heapSort(array) :
    //get max at root
    maxheapify(array)

    end = array.length() -1

    while end > 0 :
        // put max at the end
        swap(0, end)
        end--
        // put heap in max-heap order again
        siftDown(0, end) // or siftUp(0, end)

```
Source: [http://rmandvikar.blogspot.com/2009/02/heapsort.html](http://rmandvikar.blogspot.com/2009/02/heapsort.html)

So, if you are determined to upsift, perhaps as an exercise, you have two options. One is to use it only to create your initial heap, and use downsifting thereafter. Or, you can upsort in a loop and essentially heapify your elements a second time.

```
HeapSort(items) :
    end = len(items) - 1
    heapify_siftup(items, len(items))
    while end > 0 :
      swap(items[end], items[0])
      heapify_siftup(items, end)
      end--
    return items
```

I have both heapsorts implemented in python on [Github](https://github.com/kindasimple/play/blob/master/python/sort/Sorting.py).
