---
title: Exiting a Windows Phone Application
author: Evan
categories:
  - Programming
  - Windows Phone 7
tags:
  - Programming
  - Windows Phone
---
On a Windows Phone it&#8217;s bad form to quit an application to close itself. Apps are supposed to be left running, since the application lifecycle suspends apps when they are not in use. Pressing the &#8220;Back&#8221; key on the first page will close your app.

So, for times when that app should no longer be used disabling the UI is the next best thing to exiting the application. Here&#8217;s an easy way to do it.

```c#
private void Exit()
{
    while (NavigationService.BackStack.Any())
    {
            NavigationService.RemoveBackEntry();
    }
    this.IsHitTestVisible = this.IsEnabled = false;
    if (this.ApplicationBar != null)
    {
	    foreach (var item in this.ApplicationBar.Buttons.OfType<ApplicationBarIconButton>())
	    {
		     item.IsEnabled = false;
        }
    }
}
```