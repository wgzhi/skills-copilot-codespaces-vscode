
"""
工程管理模块
支持工程保存、加载以及CSV导入导出
"""

import json
import csv
from typing import List, Dict
from config import DATA_TYPES


class ProjectManager:
    def __init__(self):
        self.project_data = {
            'version': '1.0',
            'opc_server': '',
            'modbus_port': 502,
            'refresh_rate': 1000,
            'tags': []
        }
    
    def save_project(self, file_path: str) -> bool:
        """
        保存工程到文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否保存成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.project_data, f, indent=4, ensure_ascii=False)
            print(f"工程已保存到: {file_path}")
            return True
        except Exception as e:
            print(f"保存工程失败: {e}")
            return False
    
    def load_project(self, file_path: str) -> bool:
        """
        从文件加载工程
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.project_data = json.load(f)
            print(f"工程已从 {file_path} 加载")
            return True
        except Exception as e:
            print(f"加载工程失败: {e}")
            return False
    
    def set_opc_server(self, server_name: str):
        """设置OPC服务器名称"""
        self.project_data['opc_server'] = server_name
    
    def get_opc_server(self) -> str:
        """获取OPC服务器名称"""
        return self.project_data.get('opc_server', '')
    
    def set_modbus_port(self, port: int):
        """设置Modbus端口"""
        self.project_data['modbus_port'] = port
    
    def get_modbus_port(self) -> int:
        """获取Modbus端口"""
        return self.project_data.get('modbus_port', 502)
    
    def set_refresh_rate(self, rate: int):
        """设置刷新速率"""
        self.project_data['refresh_rate'] = rate
    
    def get_refresh_rate(self) -> int:
        """获取刷新速率"""
        return self.project_data.get('refresh_rate', 1000)
    
    def add_tag(self, tag_name: str, register_addr: int, data_type: str, description: str = "", register_type: str = "holding"):
        """
        添加标签配置
        
        Args:
            tag_name: OPC标签名称
            register_addr: Modbus寄存器地址
            data_type: 数据类型
            description: 描述
            register_type: 寄存器类型
        """
        tag = {
            'tag_name': tag_name,
            'register_addr': register_addr,
            'data_type': data_type,
            'description': description,
            'register_type': register_type
        }
        self.project_data['tags'].append(tag)
    
    def remove_tag(self, index: int):
        """移除标签"""
        if 0 <= index < len(self.project_data['tags']):
            del self.project_data['tags'][index]
    
    def get_tags(self) -> List[Dict]:
        """获取所有标签"""
        return self.project_data['tags']
    
    def clear_tags(self):
        """清空所有标签"""
        self.project_data['tags'] = []
    
    def export_csv(self, file_path: str) -> bool:
        """
        导出标签配置到CSV文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否导出成功
        """
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['tag_name', 'register_addr', 'data_type', 'description', 'register_type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for tag in self.project_data['tags']:
                    writer.writerow(tag)
            
            print(f"CSV已导出到: {file_path}")
            return True
        except Exception as e:
            print(f"导出CSV失败: {e}")
            return False
    
    def import_csv(self, file_path: str) -> bool:
        """
        从CSV文件导入标签配置
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否导入成功
        """
        try:
            imported_tags = []
            
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    tag = {
                        'tag_name': row.get('tag_name', ''),
                        'register_addr': int(row.get('register_addr', 0)),
                        'data_type': row.get('data_type', 'INT16'),
                        'description': row.get('description', ''),
                        'register_type': row.get('register_type', 'holding')
                    }
                    
                    if tag['data_type'] not in DATA_TYPES:
                        tag['data_type'] = 'INT16'
                    
                    imported_tags.append(tag)
            
            self.project_data['tags'] = imported_tags
            print(f"已从 {file_path} 导入 {len(imported_tags)} 个标签")
            return True
        except Exception as e:
            print(f"导入CSV失败: {e}")
            return False

