import requests
import string

for i in string.printable:
	try:
		r = requests.get('http://%s.com' % i)
	except:
		print ("estas semao, http://%s.com no existeix" % i)
