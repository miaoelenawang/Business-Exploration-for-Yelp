import json

def save_dic(file_name, output):
	with open(file_name, 'w') as f:
		json.dump(output, f)

def reload_dic(file_name):
	with open(file_name,'r') as f:
		b = f.readlines()
	return json.loads(b[0])
