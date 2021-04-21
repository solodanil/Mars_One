from requests import get, post, delete

print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/10').json())
print(get('http://localhost:5000/api/v2/jobs/str').json())

print(post('http://localhost:5000/api/v2/jobs', json={
            'team_leader': '1',
            'description': 'test_job',
            'work_size': 36,
            'collaborators': '1, 2',
            'is_finished': 0
}).json())
print(post('http://localhost:5000/api/v2/jobs').json())

print(get('http://localhost:5000/api/v2/jobs').json())

print(delete('http://localhost:5000/api/v2/jobs/2').json())
print(delete('http://localhost:5000/api/v2/jobs/15').json())

print(get('http://localhost:5000/api/v2/jobs').json())
