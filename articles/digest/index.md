# Digest Articles

<ul>
  {% for post in site.categories.digest %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
