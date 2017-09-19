import urllib3, json
http = urllib3.PoolManager()

#TODO
#Rajouter couleur / icones
R  = '\033[31m' # red
G  = '\033[32m' # green
color = ''
def color_result(result):
	#Si le resultat est bon , vert
	if result :
		return print(G + str(result) + '\033[0m')
	#Si le resultat est mauvais, le mettre en rouge
	else: return print(R + str(result) + '\033[0m')
####### TEST POST api/v1/users

print ("Test POST api/v1/users/signup")
#tester autre méthode que POST
data = {
	"email" : "foo@mail.com",
	"username" : "foo",
	"password" : "password"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('PUT',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print("méthode autre que POST")
color_result(r.status == 405)


######### TEST POST api/v1/users/signup Username déja pris
data = {
	"email" : "foo@mail.com",
	"username" : "foo",
	"password" : "password"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée de Username déja pris")
color_result(r.status == 400)



######## TEST POST api/v1/users New USER bon email bon username
data = {
	"email" : "foo2@mail.com",
	"username" : "foo2",
	"password" : "password"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec email et username pas utilisé")
color_result(r.status == 200)

#username vide
data = {
	"email" : "foo3@mail.com",
	"username" : "",
	"password" : "password"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec email bon et username vide")
color_result(r.status == 400)

#password vide
data = {
	"email" : "foo4@mail.com",
	"username" : "foo4",
	"password" : ""
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec email/ username bon mais password vide")
color_result(r.status == 400)

#email vide

data = {
	"email" : "",
	"username" : "foo5",
	"password" : "jmlabite"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec email/ password bon mais email vide")
color_result(r.status == 400)

#email déja pris

data = {
	"email" : "foo2@mail.com",
	"username" : "foo5",
	"password" : "jmlabite"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec username/ password bon mais email déja pris")
color_result(r.status == 400)

#route valide


####### TEST ENTREE POST

data = {
	"description" : "Lol that post is shit",
	"url": "localhost:5000/lololodalakdaz"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/posts',
	body=encoded_data,
	headers={'Content-Type': 'application/json',
	'Authorization' : 'eyJleHAiOjE1MDU3NTgwMzQsImlhdCI6MTUwNTU4NTIzNCwiYWxnIjoiSFMyNTYifQ.eyJpZCI6MX0.GEyiGHqFvosB3EKCYjmN29x9_qpS6n8eJikmTtm_aF0'
	}
)
print ("test POST de api/v1/posts")
color_result(r.status == 200)

####### TEST ENTREE COMMENT
####### TEST DELETE USER
####### TEST DELETE POST
####### TEST DELETE COMMENT


#r = http.request('GET', 'localhost:5000/api/v1/users/foo')
