---
permalink: /blog/
layout:    default
title:     KindaSimple Blog
---

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}"><h3>{{ post.title }}</h3></a>
      <p>{{ post.excerpt }}</p>
      <a href="{{ post.url }}">Continue Reading >></a>
    </li>
    
  {% endfor %}
</ul>
