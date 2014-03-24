---
title: Loading Styles Dynamically on Windows 8
author: Evan
layout: blog 
categories:
  - Programming
  - Windows 8
tags:
  - DUI
  - Programming
  - Styles
  - Windows 8
---
 [1]: http://msdn.microsoft.com/en-us/library/windows/apps/hh968442.aspx "Merged Dictionaries"
Windows 8 is very ambitious in its breadth of supported form factors.  Huge screens down through small tablets, it is quite variety of display surfaces supported with different dimensions, aspect ratios, and resolutions

![Common Sizes for Windows 8](http://i1.wp.com/blogs.msdn.com/cfs-file.ashx/__key/communityserver-blogs-components-weblogfiles/00-00-01-29-43-metablogapi/2526.Scaling_2D002D002D00_Common_2D00_Sizes_5F00_thumb_5F00_61A51101.jpg?resize=625%2C352 "Common Sizes for Windows 8")

While designing flexible layouts is a must; there are limits. Add to that the difference in use cases for a person interacting with a large monitor at their desk on the one hand, or viewing a television across the room on the other.  The screens would have similar dimensions and aspect ratios, but the former demands a lot of data be available up close while the latter prefers less data well presented.  DUI or Distance UI is a term for this concept, and dynamic themes may provide some solutions.

On windows 8 I can easily determine the screen size and the resolution and adjust the styles accordingly. The basic templates handle the current window&#8217;s SizeChanged event giving me an opportunity to adjust for a larger screen size.

```
private void WindowSizeChanged(object sender, WindowSizeChangedEventArgs e)
{
    LoadStylesForSize(e.Size);
    this.InvalidateVisualState();
}
```

or I can adjust for a change in resolution in the event handler for the DisplayProperties LogicalDpiChanged event

```
private void DisplayProperties_LogicalDpiChanged(object sender)
{
  LoadStylesForResolution(DisplayProperties.ResolutionScale);
}
```

To load a new template, I create a new MergedDictionary with the styles that I want and apply it to the current application resources.

```
private void LoadStylesForSize(Size size)
{
  ResourceDictionary merged = new ResourceDictionary();
  ResourceDictionary generic = new ResourceDictionary();
  ResourceDictionary theme = new ResourceDictionary();

  generic.Source = new Uri("ms-appx:/Common/StandardStyles.xaml");

  if(size.Width &lt; 1366)
  {
      theme.Source = new Uri("ms-appx:/Common/AppStyles-Custom1.xaml");
  }
  else if(size.Width &lt; 1800)
  {
      theme.Source = new Uri("ms-appx:/Common/AppStyles-Custom2.xaml");
  }
  else{
      theme.Source = new Uri("ms-appx:/Common/AppStyles-Custom3.xaml");
  }

  merged.MergedDictionaries.Add(generic);
  merged.MergedDictionaries.Add(theme);

  App.Current.Resources = merged;

  this.Frame.Navigate(this.GetType(), "AllGroups");
 }
```

When you are creating your themes, remember to pay close attention to dependencies so that a resource doesn&#8217;t try to reference another resource that is not yet defined. See MSDN on [Merged Dictionaries][1] to see what resource is loaded and when. Also, you will have to move all resources from App.xaml into your generic resource dictionary because they will be cleared when you reset your application resources to your new merged dictionary.

The updates only seem to take effect when the elements are recreated, so a navigation is required to apply the changes.

Files: [StyleDemo.zip](https://skydrive.live.com/redir?resid=90A8E1C2B0B6D69B!680&authkey=!AFjh1q_5J3dOSyc "Style Demo .zip")