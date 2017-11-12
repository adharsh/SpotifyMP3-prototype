import re

url = input('Enter URL: ')

retrieved_data = url[30:].split('/')

user = retrieved_data[0]
id = retrieved_data[2]