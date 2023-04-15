import requests
import xml.etree.ElementTree as ET
import time
i=0
total = 0
place_name = "talca"
while(i!=5000):
	start = time.time()
	if (i>500):
		place_name="conchali"
	if(i>1000):
		place_name="curacavi"
	if(i>1500):
		place_name="holanda"
	if(i>2000):
		place_name ="iquique"
	if (i>2500):
		place_name="peru"
	if(i>3000):
		place_name="buenos aires"
	if(i>3500):
		place_name="roma"
	if(i>4000):
		place_name ="italia"
	response = requests.get(f'https://nominatim.openstreetmap.org/search?q={place_name}&format=xml')
	if response.status_code == 200:
		end = time.time()
		total = end-start
		print(total)
		i+=1
		#if(total>2):
		#	i+=1
		#	print(total)
