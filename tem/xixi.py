import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 初始化列表以存储教授信息
faculty_data = []

# 访问 UCI 计算机科学系的页面
url = 'https://cs.ics.uci.edu/faculty/'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 查找所有教授条目
    faculty_list = soup.find_all('article', class_='item--person')
    
    for member in faculty_list:
        # 提取教授姓名
        name = member.find('h3', class_='person__person-title').get_text(strip=True)
        
        # 提取职位信息
        job_title = member.find('span', class_='person__job-title').get_text(strip=True) if member.find('span', class_='person__job-title') else "N/A"
        
        # 提取个人主页链接
        profile_link = member.find('a', class_='item__link')['href'] if member.find('a', class_='item__link') else "N/A"
        
        # 提取电子邮件
        email_link = member.find('a', class_='person__mail')
        email = email_link.get_text(strip=True) if email_link else "N/A"
        
        # 提取研究领域或其他介绍（假设在特定标签中）
        department = member.find('span', class_='person__department').get_text(strip=True) if member.find('span', class_='person__department') else "N/A"
        
        # 保存信息到列表
        faculty_data.append({
            'Name': name,
            'Job Title': job_title,
            'Profile URL': profile_link,
            'Email': email,
            'Department': department
        })
        
        # 避免频繁请求导致封禁
        time.sleep(1)
    
    # 将数据保存为 DataFrame
    df = pd.DataFrame(faculty_data)
    print(df)
    # 可保存为 Excel 或 CSV 文件
    df.to_csv("uci_faculty_info.csv", index=False)
else:
    print(f"Failed to access {url}, status code: {response.status_code}")
