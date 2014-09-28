{%- extends 'slides_reveal.tpl' -%}


{% block body %}

{{ super() }}

<script>

Reveal.initialize({
    controls: false,
    slideNumber: true,
    transitionSpeed: 'fast', // default/fast/slow
    theme: 'sky',
    center: false,

    minScale: 0.1,
    maxScale: 2.0
});

</script>

{% endblock body %}
