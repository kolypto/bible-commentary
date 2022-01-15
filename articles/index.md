# Article categories

* [Digest Articles](digest/)
* [Заметки](note/)
* [Лекции](lectures/)

# All Articles

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
