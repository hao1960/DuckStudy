import requests
import json

BASE_URL = 'http://localhost:5000'

def test_register():
    """测试用户注册"""
    url = f'{BASE_URL}/api/user/register'
    data = {
        'username': 'testuser',
        'password': '123456',
        'email': 'test@example.com'
    }
    response = requests.post(url, json=data)
    print('\n=== 测试注册 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {response.json()}')

def test_login():
    """测试用户登录"""
    url = f'{BASE_URL}/api/user/login'
    data = {
        'username': 'testuser',
        'password': '123456'
    }
    response = requests.post(url, json=data)
    print('\n=== 测试登录 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {response.json()}')
    return response.cookies

def test_get_courses():
    """测试获取课程列表"""
    url = f'{BASE_URL}/api/courses'
    response = requests.get(url)
    print('\n=== 测试获取课程列表 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_get_posts():
    """测试获取帖子列表"""
    url = f'{BASE_URL}/api/posts'
    response = requests.get(url)
    print('\n=== 测试获取帖子列表 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_create_post(cookies):
    """测试创建帖子"""
    url = f'{BASE_URL}/api/posts'
    data = {
        'title': '测试帖子',
        'content': '这是一个测试帖子的内容',
        'author': 'testuser'
    }
    response = requests.post(url, json=data, cookies=cookies)
    print('\n=== 测试创建帖子 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

def test_github_trending():
    """测试获取 GitHub 热门仓库（无数据库模式）"""
    url = f'{BASE_URL}/api/github/trending'
    response = requests.get(url)
    print('\n=== 测试获取 GitHub 热门仓库 ===')
    print(f'状态码: {response.status_code}')
    print(f'响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')

if __name__ == '__main__':
    print('开始测试 API...')
    
    # 测试注册
    test_register()
    
    # 测试登录
    cookies = test_login()
    
    # 测试获取课程列表
    test_get_courses()
    
    # 测试获取帖子列表
    test_get_posts()
    
    # 测试创建帖子
    test_create_post(cookies)
    
    # 测试 GitHub 热门仓库（无数据库模式）
    test_github_trending()
    
    print('\n测试完成！') 