{% load getdata_extras %}DNSID,{% for f in fields %}"{{f|addslashes}}",{% endfor %}{% for f in fields_day1 %}"{{f|addslashes}}",{% endfor %}{% for f in fields_bat %}"{{f|addslashes}}",{% endfor %}{% for f in fields_comp %}"{{f|addslashes}}",{% endfor %}{% for f in fields_freesurfer %}"{{f|addslashes}}",{% endfor %}
{% for subj,vals_day1,vals_bat,vals_comp,vals_img in subj_data_tuples %}"{{subj.dns_id|addslashes}}",{% for f in fields %}"{{ subj|getattribute:f|addslashes }}",{% endfor %}{% for v in vals_day1 %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_bat %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_comp %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_freesurfer %}"{{ v.value|addslashes }}",{% endfor %}
{% endfor %}

