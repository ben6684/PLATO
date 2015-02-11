from django import template 

register = template.Library()

def def_mm(s):
	m="Not mentioned"
	if s==1:
		m="January"
	if s==2:
		m="February"
	if s==3:
		m="March"
	if s==4:
		m="April"
	if s==5:
		m="May"
	if s==6:
		m="June"
	if s==7:
		m="July"
	if s==8:
		m="Auguste"
	if s==9:
		m="September"
	if s==10:
		m="October"
	if s==11:
		m="November"
	if s==12:
		m="December"
	
	return m

@register.filter
def month_name(month_number):
	return def_mm(month_number)
