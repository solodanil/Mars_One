from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/10').json())
print(get('http://localhost:5000/api/v2/users/str').json())

print(post('http://localhost:5000/api/v2/users', json={
            'surname': 'Ivanov',
            'name': 'Joe',
            'age': 36,
            'position': 'middle',
            'speciality': 'engeneer',
            'address': 'module_05',
            'email': 'ex@ex.ru',
            'password': 'qwerty'
}).json())
print(post('http://localhost:5000/api/v2/users').json())

print(get('http://localhost:5000/api/v2/users').json())

print(delete('http://localhost:5000/api/v2/users/2').json())
print(delete('http://localhost:5000/api/v2/users/15').json())

print(get('http://localhost:5000/api/v2/users').json())
