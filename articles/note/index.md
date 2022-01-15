# Notes

<ul>
  {% for post in site.categories.note %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
