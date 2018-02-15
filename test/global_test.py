import urllib3, json
from pprint import pprint
http = urllib3.PoolManager()

wrongAuthorization = 'jeSuIsUnMauVaisUseRloL'
authorization= ''
def color_result(result):
	#Si le resultat est bon , vert
	if result :
		return print('\033[32m' + str(result) + '\033[0m')
	#Si le resultat est mauvais, le mettre en rouge
	else: return print('\033[31m' + str(result) + '\033[0m')

####### TEST PUT api/v1/users



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
print ("Test PUT api/v1/users/signup")
color_result(r.status == 405)

######## TEST POST api/v1/users New USER bon email bon username
data = {
    "email" : "foo2@mail.com",
    "username" : "foo",
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
s= json.loads(r.data.decode('utf-8'))
#### On récupère le token de ce user afin de l'utiliser pour les prochains tests
authorization= s['token']

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
r = http.request('POST',
    'localhost:5000/api/v1/users/signup',
    body=encoded_data,
    headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un user avec Username déja pris")
color_result(r.status == 400)

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
	"password" : "pass"
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
	"password" : "pass"
}

encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/users/signup',
	body=encoded_data,
	headers={'Content-Type': 'application/json'}
)
print ("test d'entrée d'un nouveau user avec username/ password bon mais email déja pris")
color_result(r.status == 401)

############################################# FIN TEST USERS ##############################################
#
############################################# DEBUT TEST POSTS ############################################

####### TEST ENTREE POST

data = {
	"description" : "Petit chat nul lol",
    "title" : "Chat",
    "image": "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"
}
encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
	'localhost:5000/api/v1/posts',
	body=encoded_data,
	headers={'Content-Type': 'application/json',
	'Authorization' : authorization
})
print ("test POST de api/v1/posts")
color_result(r.status == 200)


####### TEST ENTREE POST USER INEXISTANT

data = {
       "description" : "Petit chat nul lol",
    "title" : "Chat",
    "image" : "lololllolol"
}
encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
    'localhost:5000/api/v1/posts',
    body=encoded_data,
    headers={'Content-Type': 'application/json',
    'Authorization' : wrongAuthorization
})
print ("test POST de api/v1/posts avec User inexistant")
color_result(r.status == 401)

####### TEST DELETE POST MAUVAIS USER
#
r = http.request('DELETE',
    'localhost:5000/api/v1/posts/1',
    headers={
    'Authorization' : wrongAuthorization
    }
)
print ("test DELETE de api/v1/posts/1 avec mauvais user")
color_result(r.status == 401)

####### TEST DELETE POST INEXISTANT
#
r = http.request('DELETE',
    'localhost:5000/api/v1/posts/1548',
    headers={
    'Authorization' : authorization
    }
)
print ("test DELETE de api/v1/posts/1548 qui est un post inexistant")
color_result(r.status == 404)

################################# UPVOTES TESTS ###################

####### TEST D'UPVOTE DE POST
r = http.request('POST',
    'localhost:5000/api/v1/posts/1/upvotes',
    headers={
    'Authorization' : authorization
    }
)
print ("test POST upvotes de api/v1/posts/1/upvotes")
color_result(r.status == 200)

####### TEST D'UPVOTE DE POST INEXISTANT
r = http.request('POST',
    'localhost:5000/api/v1/posts/50/upvotes',
    headers={
    'Authorization' : authorization
    }
)
print ("test POST upvotes de api/v1/posts/50/upvotes avec Post inexistant")
color_result(r.status == 404)

####### TEST D'UPVOTE DE POST AVEC USER INEXISTANT
r = http.request('POST',
    'localhost:5000/api/v1/posts/1/upvotes',
    headers={
    'Authorization' : wrongAuthorization
    }
)
print ("test POST upvotes de api/v1/posts/50/upvotes avec user inexistant")
color_result(r.status == 401)


############################################# FIN TEST POSTS ##############################################
#
############################################# DEBUT TEST COMMENTS ############################################

####### TEST ENTREE COMMENT USER INEXISTANT

data = {
    "content" : "Lol that post is so bad",
    "post_id": 1
}
encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
    'localhost:5000/api/v1/comments',
    body=encoded_data,
    headers={'Content-Type': 'application/json',
    'Authorization' : wrongAuthorization
})
print ("test POST de api/v1/comments avec User inexistant")
color_result(r.status == 401)

####### TEST ENTREE COMMENT
data = {
    "content" : "Lol that post is so bad",
    "post_id": 1
}
encoded_data = json.dumps(data).encode('utf-8')
r = http.request('POST',
    'localhost:5000/api/v1/comments',
    body=encoded_data,
    headers={'Content-Type': 'application/json',
    'Authorization' : authorization
    }
)
print ("test POST de api/v1/comments")
color_result(r.status == 200)


####### TEST DELETE COMMENT MAUVAIS USER
#
r = http.request('DELETE',
    'localhost:5000/api/v1/comments/1',
    headers={
    'Authorization' : wrongAuthorization
    }
)
print ("test DELETE de api/v1/comments/1 avec mauvais user")
color_result(r.status == 401)



####### TEST DELETE COMMENT INEXISTANT
#
r = http.request('DELETE',
    'localhost:5000/api/v1/comments/1548',
    headers={
    'Authorization' : authorization
    }
)
print ("test DELETE de api/v1/comments/1548 qui est un comment inexistant")
color_result(r.status == 404)



####### TEST DELETE COMMENT BON USER
#
r = http.request('DELETE',
    'localhost:5000/api/v1/comments/1',
    headers={
    'Authorization' : authorization
}
)
print ("test DELETE de api/v1/comments/1")
color_result(r.status == 200)

####### TEST DELETE POST BON USER
#
r = http.request('DELETE',
    'localhost:5000/api/v1/posts/1',
    headers={
    'Authorization' : authorization
    }
)
print ("test DELETE de api/v1/posts/1")
color_result(r.status == 200)



####### TEST DELETE USER BON USER

r = http.request('DELETE',
    'localhost:5000/api/v1/users',
    headers={
    'Authorization' : authorization
    }
)
print ("test DELETE de api/v1/users")
color_result(r.status == 200)



#r = http.request('GET', 'localhost:5000/api/v1/users/foo')
