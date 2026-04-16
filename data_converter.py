
"""
数据类型转换模块
支持多种数据类型与Modbus寄存器之间的转换
"""

import struct
import numpy as np
from config import DATA_TYPES


class DataConverter:
    @staticmethod
    def value_to_registers(value, data_type):
        """
        将数值转换为Modbus寄存器列表
        
        Args:
            value: 输入数值
            data_type: 数据类型
            
        Returns:
            list: 寄存器列表 (16位整数)
        """
        type_info = DATA_TYPES[data_type]
        registers = []
        
        if data_type == 'INT16':
            val = int(value)
            if val < -32768 or val > 32767:
                raise ValueError("INT16 value out of range")
            registers.append(val & 0xFFFF)
        elif data_type == 'UINT16':
            val = int(value)
            if val < 0 or val > 65535:
                raise ValueError("UINT16 value out of range")
            registers.append(val & 0xFFFF)
        elif data_type in ['INT32', 'UINT32', 'FLOAT32']:
            if data_type == 'FLOAT32':
                packed = struct.pack('<f', float(value))
            else:
                is_signed = type_info['signed']
                packed = struct.pack('<i' if is_signed else '<I', int(value))
            
            word1 = struct.unpack('<H', packed[0:2])[0]
            word2 = struct.unpack('<H', packed[2:4])[0]
            registers.extend([word1, word2])
        elif data_type in ['INT64', 'UINT64', 'FLOAT64']:
            if data_type == 'FLOAT64':
                packed = struct.pack('<d', float(value))
            else:
                is_signed = type_info['signed']
                packed = struct.pack('<q' if is_signed else '<Q', int(value))
            
            for i in range(0, 8, 2):
                word = struct.unpack('<H', packed[i:i+2])[0]
                registers.append(word)
        
        return registers
    
    @staticmethod
    def registers_to_value(registers, data_type):
        """
        将Modbus寄存器列表转换为数值
        
        Args:
            registers: 寄存器列表 (16位整数)
            data_type: 数据类型
            
        Returns:
            转换后的数值
        """
        type_info = DATA_TYPES[data_type]
        
        if data_type == 'INT16':
            val = registers[0]
            if val & 0x8000:
                val -= 0x10000
            return val
        elif data_type == 'UINT16':
            return registers[0]
        elif data_type in ['INT32', 'UINT32', 'FLOAT32']:
            packed = struct.pack('<HH', registers[0], registers[1])
            if data_type == 'FLOAT32':
                return struct.unpack('<f', packed)[0]
            else:
                is_signed = type_info['signed']
                return struct.unpack('<i' if is_signed else '<I', packed)[0]
        elif data_type in ['INT64', 'UINT64', 'FLOAT64']:
            packed = struct.pack('<HHHH', registers[0], registers[1], registers[2], registers[3])
            if data_type == 'FLOAT64':
                return struct.unpack('<d', packed)[0]
            else:
                is_signed = type_info['signed']
                return struct.unpack('<q' if is_signed else '<Q', packed)[0]
        
        return None

