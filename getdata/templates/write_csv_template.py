{% load getdata_extras %}DNSID,{% for f in fields %}"{{f|addslashes}}",{% endfor %}{% for f in fields_day1 %}"{{f|addslashes}}",{% endfor %}{% for f in fields_bat %}"{{f|addslashes}}",{% endfor %}{% for f in fields_img %}"{{f|addslashes}}",{% endfor %}{% for f in fields_snp %}"{{f|addslashes}}",{% endfor %}
{% for subj,vals_day1,vals_bat,vals_img,genos in subj_data_tuples %}
"{{subj.dns_id|addslashes}}",{% for f in fields %}"{{ subj|getattribute:f|addslashes }}",{% endfor %}{% for v in vals_day1 %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_bat %}"{{ v.value|addslashes }}",{% endfor %}{% for v in vals_img %}"{{ v.value|addslashes }}",{% endfor %}{% for g in genos %}"{{ g.genotype|addslashes }}",{% endfor %}	
{% endfor %}

