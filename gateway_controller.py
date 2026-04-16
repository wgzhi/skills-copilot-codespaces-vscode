
"""
网关主控制器
整合OPC客户端、Modbus服务器和工程管理功能
"""

import time
from typing import Dict
from opc_client import OPCClient
from modbus_server import ModbusTCPServer
from project_manager import ProjectManager


class GatewayController:
    def __init__(self):
        self.opc_client = OPCClient()
        self.modbus_server = ModbusTCPServer()
        self.project_manager = ProjectManager()
        
        self.opc_client.on_data_update = self._on_opc_data_update
        self.running = False
    
    def load_project(self, file_path: str) -> bool:
        """加载工程配置"""
        if self.project_manager.load_project(file_path):
            self._apply_project_config()
            return True
        return False
    
    def save_project(self, file_path: str) -> bool:
        """保存工程配置"""
        self._update_project_from_current()
        return self.project_manager.save_project(file_path)
    
    def _apply_project_config(self):
        """应用工程配置"""
        self.opc_client.tags.clear()
        
        for tag_config in self.project_manager.get_tags():
            self.opc_client.add_tag(
                tag_config['tag_name'],
                tag_config['register_addr'],
                tag_config['data_type'],
                tag_config['description']
            )
    
    def _update_project_from_current(self):
        """更新工程配置为当前状态"""
        self.project_manager.clear_tags()
        
        for tag_name, tag_info in self.opc_client.tags.items():
            self.project_manager.add_tag(
                tag_name,
                tag_info['register_addr'],
                tag_info['data_type'],
                tag_info['description'],
                'holding'
            )
        
        self.project_manager.set_opc_server(self.opc_client.server_name)
        self.project_manager.set_modbus_port(self.modbus_server.port)
        self.project_manager.set_refresh_rate(self.opc_client.refresh_rate)
    
    def start_gateway(self):
        """启动网关"""
        if self.running:
            print("网关已在运行中")
            return
        
        if not self.opc_client.connected and self.project_manager.get_opc_server():
            self.opc_client.connect(self.project_manager.get_opc_server())
        
        if self.opc_client.connected:
            modbus_port = self.project_manager.get_modbus_port()
            refresh_rate = self.project_manager.get_refresh_rate()
            
            self.modbus_server.start(port=modbus_port)
            self.opc_client.start_refresh(refresh_rate)
            self.running = True
            print("网关已启动")
    
    def stop_gateway(self):
        """停止网关"""
        if not self.running:
            return
        
        self.opc_client.stop_refresh()
        self.modbus_server.stop()
        self.running = False
        print("网关已停止")
    
    def _on_opc_data_update(self, data: Dict[str, dict]):
        """OPC数据更新回调"""
        for tag_name, tag_data in data.items():
            if tag_name in self.opc_client.tags:
                tag_info = self.opc_client.tags[tag_name]
                value = tag_data.get('value')
                quality = tag_data.get('quality')
                
                if quality == 'Good' and value is not None:
                    try:
                        self.modbus_server.write_value_to_registers(
                            tag_info['register_addr'],
                            value,
                            tag_info['data_type'],
                            'holding'
                        )
                    except Exception as e:
                        print(f"写入Modbus寄存器失败: {e}")
    
    def add_tag(self, tag_name: str, register_addr: int, data_type: str, description: str = ""):
        """添加标签"""
        self.opc_client.add_tag(tag_name, register_addr, data_type, description)
    
    def remove_tag(self, tag_name: str):
        """移除标签"""
        self.opc_client.remove_tag(tag_name)
    
    def connect_opc(self, server_name: str) -> bool:
        """连接OPC服务器"""
        return self.opc_client.connect(server_name)
    
    def disconnect_opc(self):
        """断开OPC连接"""
        if self.running:
            self.stop_gateway()
        self.opc_client.disconnect()
    
    def get_available_opc_servers(self):
        """获取可用的OPC服务器"""
        return self.opc_client.get_available_servers()
    
    def is_running(self) -> bool:
        """检查网关是否运行中"""
        return self.running

