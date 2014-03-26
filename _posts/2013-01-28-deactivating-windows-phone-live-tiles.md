---
title: Deactivating Windows Phone Live Tiles
author: Evan
layout: blog 
categories:
  - Programming
  - Technology
  - Windows Phone 7
  - Windows Phone 8
tags:
  - Live Tiles
  - Programming
  - Windows Phone
---
 [1]: http://msdn.microsoft.com/en-us/library/windowsphone/develop/jj206971(v=vs.105).aspx "Flip Tile Template Overview on MSDN"
When alive with activity, the Windows Phone 8 Live Tiles look great. I like the [Flip Tile Template][1], in particular. It&#8217;s useful to be able to return them to a dormant state, and its not immediately obvious how to do this. Update your tile template Text and TileUri and your tile will clear its content but remain &#8220;alive&#8221; and flipping.

This problem [carries over from Windows Phone 7](http://social.msdn.microsoft.com/Forums/en-US/wpnotifications/thread/9f5c85e0-7bb3-4f2d-9700-9359642f5a72/ "Windows Phone QA: How do I reset a flipping Mango Tile after push notification?") where, to prevent my dormant tiles from spinning, I would force an error.

<pre class="prettyprint"><code>
ShellTile pinnedTile = GetPinnedTile();
StandardTileData dormantTile = GetDormantTile();

StandardTileData invalidTile = dormantTile.BackBackgroundImage = new Uri("/", UriKind.Relative); //this is an invalid uri
pinnedTile.Update(invalidTile); //prevent flipping by causing error

pinnedTile.Update(dormantTile);
</code></pre>

This hack doesn&#8217;t work in Windows Phone 8. I came across the suggestion to clear all text fields by setting them to empty strings and clear all Uri by setting them equal to null. I find it easier to use an empty template to be sure all properties are nulled.

<pre class="prettyprint"><code>
private string FLIP_TEMPLATE_XML = @"&lt;?xml version=""1.0"" encoding=""utf-8""?>
&lt;wp:Notification xmlns:wp=""WPNotification"" Version=""2.0"">
  &lt;wp:Tile Id=""[Tile ID]"" Template=""FlipTile"">
    &lt;wp:SmallBackgroundImage Action=""Clear"">&lt;/wp:SmallBackgroundImage>
    &lt;wp:WideBackgroundImage Action=""Clear"">&lt;/wp:WideBackgroundImage>
    &lt;wp:WideBackBackgroundImage Action=""Clear"">&lt;/wp:WideBackBackgroundImage>
    &lt;wp:WideBackContent Action=""Clear"">&lt;/wp:WideBackContent>
    &lt;wp:BackgroundImage Action=""Clear"">&lt;/wp:BackgroundImage>
    &lt;wp:Count Action=""Clear"">&lt;/wp:Count>
    &lt;wp:Title Action=""Clear"">&lt;/wp:Title>
    &lt;wp:BackBackgroundImage Action=""Clear"">&lt;/wp:BackBackgroundImage>
    &lt;wp:BackTitle Action=""Clear"">&lt;/wp:BackTitle>
    &lt;wp:BackContent Action=""Clear"">&lt;/wp:BackContent>
  &lt;/wp:Tile>
&lt;/wp:Notification>"
</code></pre>

And then update the tile to force it to go dormant.

<pre class="prettyprint"><code>
FlipTileData pinnedTile = GetPinnedTile();
FlipTileData dormantTile = GetDormantTile();

FlipTileData clearTile = new FlipTileData(FLIP_TEMPLATE_XML.Replace("[Tile ID]", "MyTile"));
pinnedTile.Update(clearTile);

pinnedTile.Update(tileData);
</code></pre>

This works, but not 100% reliably. A dormant tile will at times, come to life unexpectedly.  I realized that the platform was defeating me after some trial and error.

The problem is that when a live tile is updated, the tile queues up an update to all tile sizes but to be efficient it defers execution of the update until a size needs to be displayed. So, a wide image won&#8217;t be downloaded until changing to a wide live tile.  After updating a live tile to a dormant template, changing its size will trigger both the dormant update AND ANY UPDATE ALREADY IN THE QUEUE.

These updates occur asynchronously rather than sequentially. As a result, my update to a dormant tile would happen quickly. The queued update to a flipping tile retrieved images from a remote uri, and so it completed second and the tile remained &#8220;live&#8221;.

My workaround is to set the tile as dormant every time the application is run, and so the outdated tile eventually works itself out. I don&#8217;t yet know of a foolproof way to remove the activity from my live tiles. Do you know of one?