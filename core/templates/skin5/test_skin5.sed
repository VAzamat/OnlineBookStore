s|https://demo\.templatesjungle\.com/[^/]\+/\([[:alnum:]_-]\+\)\.html|{% url 'core:\1' %}|g
s|core:about|core:about_us|g
s|core:single-product|core:single_product|g
s|single-post|single_post|g
s|\./\([[:alnum:]_-]\+\)_files/|images/|g
s|src=\"images/\([^\"]*\)\"|src=\"{% static 'skin5/images/\1' %}\"|g
s|'core:contact'|'core:contacts'|g
s|core:login|core:my_account|g

