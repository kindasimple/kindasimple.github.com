---
permalink: /blog/
layout:    single
title:     Kinda Simple Solutions Blog
classes:   wide
author_profile: true
---

<div>
  {% for post in site.posts %}
	  <span>
    	<p class="post-meta" style="float:right;">{{ post.date | date: "%-d %B %Y" }}</p>
    	<a href="{{ post.url }}"><h1 class="content-subhead">{{ post.title }}</h1></a>
      </span>
      <p>{{ post.excerpt }}</p>
      <p>
      <a href="{{ post.url }}">Continue Reading >></a>
      </p>
  {% endfor %}
</div>