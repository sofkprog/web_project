from requests import post, get, delete

print(get('http://localhost:8080/api/goods').json())

"""print(post('http://localhost:8080/api/goods',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'price': 200,
                 'is_private': False}).json())"""
'''print(delete('http://localhost:8080/api/goods/9').json())'''
