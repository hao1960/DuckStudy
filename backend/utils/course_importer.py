# backend/utils/course_importer.py
import json
import os
from typing import Dict, List, Optional
from backend.models.course import Course
from backend.config.database import db

def import_course_data(json_file: str) -> bool:
    """从JSON文件导入课程数据"""
    try:
        if not os.path.exists(json_file):
            print(f"文件不存在: {json_file}")
            return False
            
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"读取到的数据: {data}")  # 调试信息
            
        for course_data in data.get('courses', []):
            print(f"处理课程数据: {course_data}")  # 调试信息
            
            # 验证必要字段
            if 'name' not in course_data:
                print(f"课程数据缺少name字段: {course_data}")
                continue
                
            # 检查课程是否已存在
            existing_course = Course.query.filter_by(
                name=course_data['name']
            ).first()
            
            if existing_course:
                print(f"课程已存在: {course_data['name']}")
                continue
                
            try:
                # 创建新课程
                course = Course(
                    name=course_data['name'],
                    description=course_data.get('description', '')
                )
                
                print(f"准备添加课程: {course.name}")  # 调试信息
                db.session.add(course)
                print(f"课程已添加到session: {course.name}")  # 调试信息
                
                # 立即提交每个课程
                try:
                    db.session.commit()
                    print(f"成功提交课程: {course.name}")
                except Exception as e:
                    print(f"提交课程 {course.name} 失败: {str(e)}")
                    db.session.rollback()
                    continue
                
            except Exception as e:
                print(f"创建课程对象失败: {str(e)}")
                continue
            
        print("所有课程处理完成")
        return True
        
    except Exception as e:
        print(f"导入课程数据失败: {str(e)}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        db.session.rollback()
        return False

def export_course_data(json_file: str) -> bool:
    """导出课程数据到JSON文件"""
    try:
        courses = Course.query.all()
        data = {
            'courses': [
                {
                    'id': course.id,
                    'name': course.name,
                    'description': course.description
                }
                for course in courses
            ]
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("课程数据导出成功！")
        return True
        
    except Exception as e:
        print(f"导出课程数据失败: {str(e)}")
        return False