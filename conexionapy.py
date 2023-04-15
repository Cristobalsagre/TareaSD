import redis
import requests
import xml.etree.ElementTree as ET
import time

total = 0

#Esto es para poder conectar las instancias de redis a python, y poder modificar el cache
r1 = redis.Redis(host='localhost', port=6379, decode_responses=True)
r2 = redis.Redis(host='localhost', port=6380, decode_responses=True)
r3 = redis.Redis(host='localhost', port=6381, decode_responses=True)

while(True):
	# Definir el lugar a buscar
	place_name = input("Ingrese ubicacion a buscar: ")
	char_place = list(place_name)
	#se empieza a medir el tiempo
	start = time.time()
	
	#Estos condicionales ven si ya esta el lugar buscado en cache
	if (r1.exists(place_name) == 1):
		print(r1.hgetall(place_name))
		end = time.time()
		total = end-start
		print(total)
		continue

	elif (r2.exists(place_name) == 1):
		print(r2.hgetall(place_name))
		end = time.time()
		total = end-start
		print(total)
		continue

	elif (r3.exists(place_name) == 1):
		print(r3.hgetall(place_name))
		end = time.time()
		total = end-start
		print(total)
		continue
	# Hacer una solicitud GET a la API

	response = requests.get(f'https://nominatim.openstreetmap.org/search?q={place_name}&format=xml')

	# Verificar que la solicitud fue exitosa (código de estado 200)
	if response.status_code == 200:
	    end = time.time()
	    total = end-start
	    # La respuesta de la API está disponible en response.text
	    # Analizar la respuesta XML
	    root = ET.fromstring(response.text)
	    # Obtener los datos del primer resultado
	    first_result = root.find('place')
	    
	    #Aqui se distribuye la carga entre los cache, se ve la primera letra del input y segun eso va a un redis o a otro
	    letter_to_redis = {
		'a': r1,
		'b': r1,
		'c': r1,
		'd': r1,
		'e': r1,
		'f': r1,
		'g': r1,
		'j': r1,
		'k': r2,
		'l': r2,
		'm': r2,
		'n': r2,
		'o': r2,
		'p': r2,
		'q': r2,
		'r': r2,
		's': r2,
		'v': r3,
		'x': r3,
		'y': r3,
		'z': r3,
		'u': r3,
		't': r3,
		'h': r3,
		'i': r3,
		}

	    #Si se cumplio alguna de las condicionales anteriores, se escriben los datos en el cache
	    redis_instance = letter_to_redis.get(char_place[0], None)
	    if redis_instance is not None:
	    	redis_instance.hset(place_name, mapping={
			'Nombre': f'{first_result.attrib["display_name"]}',
			'Latitud': f'{first_result.attrib["lat"]}',
			'Longitud': f'{first_result.attrib["lon"]}'
		})

		
		
	    # Imprimir algunos datos
	    print(f'Nombre: {first_result.attrib["display_name"]}')
	    print(f'Latitud: {first_result.attrib["lat"]}')
	    print(f'Longitud: {first_result.attrib["lon"]}')
	    print(total)
	else:
	    # Si la solicitud no fue exitosa, se puede imprimir un mensaje de error
	    print('Error al hacer la solicitud:', response.status_code)
