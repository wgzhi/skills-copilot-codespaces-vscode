
"""
OPC DA 客户端模块
用于连接和读取OPC DA服务器数据
"""

import time
import threading
from typing import Dict, List, Callable, Optional


class OPCClient:
    def __init__(self):
        self.connected = False
        self.server_name = ""
        self.tags: Dict[str, dict] = {}
        self.values: Dict[str, any] = {}
        self.refresh_thread = None
        self.refresh_rate = 1000  # ms
        self.running = False
        self.on_data_update: Optional[Callable] = None
        self.simulation_mode = True  # 默认使用模拟模式，方便测试
        
    def connect(self, server_name: str) -> bool:
        """
        连接到OPC DA服务器
        
        Args:
            server_name: OPC服务器名称
            
        Returns:
            bool: 连接是否成功
        """
        try:
            self.server_name = server_name
            
            if self.simulation_mode:
                print(f"[模拟模式] 连接到OPC服务器: {server_name}")
                self.connected = True
                return True
            
            # 实际OPC DA连接代码 (Windows环境下使用)
            try:
                import OpenOPC
                self.opc = OpenOPC.client()
                self.opc.connect(server_name)
                self.connected = True
                return True
            except ImportError:
                print("OpenOPC库未安装，使用模拟模式")
                self.simulation_mode = True
                self.connected = True
                return True
                
        except Exception as e:
            print(f"连接OPC服务器失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开与OPC服务器的连接"""
        self.stop_refresh()
        
        if not self.simulation_mode and hasattr(self, 'opc'):
            try:
                self.opc.close()
            except:
                pass
        
        self.connected = False
        print("已断开OPC服务器连接")
    
    def add_tag(self, tag_name: str, register_addr: int, data_type: str, description: str = ""):
        """
        添加OPC标签
        
        Args:
            tag_name: OPC标签名称
            register_addr: Modbus寄存器地址
            data_type: 数据类型
            description: 描述
        """
        self.tags[tag_name] = {
            'tag_name': tag_name,
            'register_addr': register_addr,
            'data_type': data_type,
            'description': description,
            'last_value': None,
            'quality': 'Good'
        }
        
        if self.simulation_mode:
            self.values[tag_name] = 0
    
    def remove_tag(self, tag_name: str):
        """移除OPC标签"""
        if tag_name in self.tags:
            del self.tags[tag_name]
        if tag_name in self.values:
            del self.values[tag_name]
    
    def get_available_servers(self) -> List[str]:
        """
        获取可用的OPC服务器列表
        
        Returns:
            List[str]: 服务器名称列表
        """
        if self.simulation_mode:
            return ['Matrikon.OPC.Simulation.1', 'Kepware.KEPServerEX.V6', 'Simulation.Server']
        
        try:
            import OpenOPC
            opc = OpenOPC.client()
            servers = opc.servers()
            opc.close()
            return servers
        except:
            return ['Matrikon.OPC.Simulation.1']
    
    def read_tag(self, tag_name: str) -> tuple:
        """
        读取单个标签的值
        
        Args:
            tag_name: 标签名称
            
        Returns:
            tuple: (value, quality, timestamp)
        """
        if not self.connected:
            return None, 'Not Connected', None
        
        if self.simulation_mode:
            import random
            if tag_name not in self.values:
                self.values[tag_name] = 0
            
            if 'RANDOM' in tag_name.upper() or 'SIM' in tag_name.upper():
                self.values[tag_name] = random.uniform(0, 100)
            else:
                self.values[tag_name] += random.uniform(-1, 1)
            
            return self.values[tag_name], 'Good', time.time()
        
        try:
            value, quality, timestamp = self.opc.read(tag_name)
            return value, quality, timestamp
        except Exception as e:
            print(f"读取标签 {tag_name} 失败: {e}")
            return None, 'Error', None
    
    def read_all_tags(self) -> Dict[str, dict]:
        """
        读取所有标签的值
        
        Returns:
            Dict[str, dict]: 标签数据字典
        """
        results = {}
        
        for tag_name in self.tags:
            value, quality, timestamp = self.read_tag(tag_name)
            results[tag_name] = {
                'value': value,
                'quality': quality,
                'timestamp': timestamp
            }
            
            if quality == 'Good':
                self.tags[tag_name]['last_value'] = value
                self.tags[tag_name]['quality'] = quality
                self.values[tag_name] = value
        
        return results
    
    def start_refresh(self, refresh_rate: int = None):
        """
        开始定时刷新数据
        
        Args:
            refresh_rate: 刷新间隔(ms)
        """
        if refresh_rate:
            self.refresh_rate = refresh_rate
        
        self.running = True
        self.refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self.refresh_thread.start()
        print(f"开始数据刷新，间隔: {self.refresh_rate}ms")
    
    def stop_refresh(self):
        """停止数据刷新"""
        self.running = False
        if self.refresh_thread and self.refresh_thread.is_alive():
            self.refresh_thread.join(timeout=2.0)
        print("已停止数据刷新")
    
    def _refresh_loop(self):
        """刷新循环"""
        while self.running:
            try:
                results = self.read_all_tags()
                if self.on_data_update:
                    self.on_data_update(results)
            except Exception as e:
                print(f"刷新数据时出错: {e}")
            
            time.sleep(self.refresh_rate / 1000.0)

