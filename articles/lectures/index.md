# Digest Articles

<ul>
  {% for post in site.categories.lectures %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
