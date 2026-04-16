
"""
Modbus TCP 服务器模块
提供Modbus TCP服务器功能
"""

import threading
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from typing import Dict, Optional
from config import MAX_REGISTERS
from data_converter import DataConverter


class ModbusTCPServer:
    def __init__(self):
        self.port = 502
        self.running = False
        self.server_thread = None
        self.context = None
        self.holding_registers = [0] * MAX_REGISTERS
        self.input_registers = [0] * MAX_REGISTERS
        self.coils = [False] * MAX_REGISTERS
        self.discrete_inputs = [False] * MAX_REGISTERS
        self.data_converter = DataConverter()
        
    def start(self, host: str = '0.0.0.0', port: int = 502) -> bool:
        """
        启动Modbus TCP服务器
        
        Args:
            host: 监听地址
            port: 监听端口
            
        Returns:
            bool: 是否启动成功
        """
        if self.running:
            print("Modbus服务器已在运行中")
            return True
        
        try:
            self.port = port
            
            # 创建数据块
            store = {
                'di': ModbusSequentialDataBlock(0, self.discrete_inputs),
                'co': ModbusSequentialDataBlock(0, self.coils),
                'hr': ModbusSequentialDataBlock(0, self.holding_registers),
                'ir': ModbusSequentialDataBlock(0, self.input_registers),
            }
            
            # 创建上下文
            self.context = ModbusServerContext(slaves=store, single=True)
            
            # 在新线程中启动服务器
            self.running = True
            self.server_thread = threading.Thread(
                target=self._server_loop,
                args=(host, port),
                daemon=True
            )
            self.server_thread.start()
            
            print(f"Modbus TCP服务器已启动，监听地址: {host}:{port}")
            return True
            
        except Exception as e:
            print(f"启动Modbus服务器失败: {e}")
            self.running = False
            return False
    
    def stop(self):
        """停止Modbus TCP服务器"""
        if not self.running:
            return
        
        self.running = False
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2.0)
        
        print("Modbus TCP服务器已停止")
    
    def _server_loop(self, host: str, port: int):
        """服务器循环"""
        try:
            StartTcpServer(
                context=self.context,
                address=(host, port)
            )
        except Exception as e:
            if self.running:
                print(f"Modbus服务器运行错误: {e}")
    
    def write_holding_register(self, address: int, value: int):
        """
        写入单个保持寄存器
        
        Args:
            address: 寄存器地址
            value: 寄存器值
        """
        if 0 <= address < MAX_REGISTERS:
            self.holding_registers[address] = value & 0xFFFF
            if self.context:
                self.context[0].setValues(3, address, [self.holding_registers[address]])
    
    def write_holding_registers(self, address: int, values: list):
        """
        写入多个保持寄存器
        
        Args:
            address: 起始地址
            values: 值列表
        """
        for i, value in enumerate(values):
            if 0 <= address + i < MAX_REGISTERS:
                self.holding_registers[address + i] = value & 0xFFFF
        
        if self.context:
            self.context[0].setValues(3, address, [v & 0xFFFF for v in values])
    
    def write_input_register(self, address: int, value: int):
        """
        写入单个输入寄存器
        
        Args:
            address: 寄存器地址
            value: 寄存器值
        """
        if 0 <= address < MAX_REGISTERS:
            self.input_registers[address] = value & 0xFFFF
            if self.context:
                self.context[0].setValues(4, address, [self.input_registers[address]])
    
    def write_input_registers(self, address: int, values: list):
        """
        写入多个输入寄存器
        
        Args:
            address: 起始地址
            values: 值列表
        """
        for i, value in enumerate(values):
            if 0 <= address + i < MAX_REGISTERS:
                self.input_registers[address + i] = value & 0xFFFF
        
        if self.context:
            self.context[0].setValues(4, address, [v & 0xFFFF for v in values])
    
    def write_value_to_registers(self, address: int, value, data_type: str, register_type: str = 'holding'):
        """
        将数值写入寄存器
        
        Args:
            address: 起始地址
            value: 数值
            data_type: 数据类型
            register_type: 寄存器类型 ('holding' 或 'input')
        """
        registers = self.data_converter.value_to_registers(value, data_type)
        
        if register_type == 'holding':
            self.write_holding_registers(address, registers)
        else:
            self.write_input_registers(address, registers)
    
    def read_holding_register(self, address: int) -> int:
        """
        读取单个保持寄存器
        
        Args:
            address: 寄存器地址
            
        Returns:
            int: 寄存器值
        """
        if 0 <= address < MAX_REGISTERS:
            return self.holding_registers[address]
        return 0
    
    def read_holding_registers(self, address: int, count: int) -> list:
        """
        读取多个保持寄存器
        
        Args:
            address: 起始地址
            count: 数量
            
        Returns:
            list: 值列表
        """
        values = []
        for i in range(count):
            if 0 <= address + i < MAX_REGISTERS:
                values.append(self.holding_registers[address + i])
            else:
                values.append(0)
        return values
    
    def read_input_register(self, address: int) -> int:
        """
        读取单个输入寄存器
        
        Args:
            address: 寄存器地址
            
        Returns:
            int: 寄存器值
        """
        if 0 <= address < MAX_REGISTERS:
            return self.input_registers[address]
        return 0
    
    def read_input_registers(self, address: int, count: int) -> list:
        """
        读取多个输入寄存器
        
        Args:
            address: 起始地址
            count: 数量
            
        Returns:
            list: 值列表
        """
        values = []
        for i in range(count):
            if 0 <= address + i < MAX_REGISTERS:
                values.append(self.input_registers[address + i])
            else:
                values.append(0)
        return values

