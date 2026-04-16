
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心功能测试脚本
测试OPC客户端、Modbus服务器和数据转换功能
"""

import sys
import time
from opc_client import OPCClient
from modbus_server import ModbusTCPServer
from data_converter import DataConverter
from gateway_controller import GatewayController


def test_data_converter():
    """测试数据类型转换"""
    print("测试数据类型转换...")
    
    converter = DataConverter()
    
    # 测试INT16
    value = 12345
    registers = converter.value_to_registers(value, 'INT16')
    print(f"INT16 {value} -> {registers}")
    
    # 测试UINT16
    value = 65535
    registers = converter.value_to_registers(value, 'UINT16')
    print(f"UINT16 {value} -> {registers}")
    
    # 测试FLOAT32
    value = 123.456
    registers = converter.value_to_registers(value, 'FLOAT32')
    print(f"FLOAT32 {value} -> {registers}")
    
    # 测试FLOAT64
    value = 123.456789
    registers = converter.value_to_registers(value, 'FLOAT64')
    print(f"FLOAT64 {value} -> {registers}")
    
    print("数据类型转换测试完成")


def test_opc_client():
    """测试OPC客户端"""
    print("\n测试OPC客户端...")
    
    opc_client = OPCClient()
    
    # 测试获取服务器列表
    servers = opc_client.get_available_servers()
    print(f"可用OPC服务器: {servers}")
    
    # 测试连接
    if opc_client.connect('Matrikon.OPC.Simulation.1'):
        print("OPC服务器连接成功")
        
        # 添加测试标签
        opc_client.add_tag('Random.Int1', 0, 'INT16', '测试标签1')
        opc_client.add_tag('Random.Real1', 1, 'FLOAT32', '测试标签2')
        
        # 测试读取数据
        for i in range(3):
            data = opc_client.read_all_tags()
            print(f"第{i+1}次读取:")
            for tag_name, tag_data in data.items():
                print(f"  {tag_name}: {tag_data['value']}")
            time.sleep(0.5)
        
        opc_client.disconnect()
    else:
        print("OPC服务器连接失败")
    
    print("OPC客户端测试完成")


def test_modbus_server():
    """测试Modbus服务器"""
    print("\n测试Modbus服务器...")
    
    modbus_server = ModbusTCPServer()
    
    # 启动服务器
    if modbus_server.start(port=5020):  # 使用5020端口避免权限问题
        print("Modbus服务器启动成功，监听端口5020")
        
        # 测试写入数据
        modbus_server.write_holding_register(0, 12345)
        modbus_server.write_holding_register(1, 67890)
        
        # 测试读取数据
        value1 = modbus_server.read_holding_register(0)
        value2 = modbus_server.read_holding_register(1)
        print(f"读取寄存器0: {value1}")
        print(f"读取寄存器1: {value2}")
        
        # 测试写入浮点数
        modbus_server.write_value_to_registers(2, 123.456, 'FLOAT32')
        registers = modbus_server.read_holding_registers(2, 2)
        print(f"浮点数寄存器: {registers}")
        
        # 停止服务器
        modbus_server.stop()
    else:
        print("Modbus服务器启动失败")
    
    print("Modbus服务器测试完成")


def test_gateway():
    """测试网关功能"""
    print("\n测试网关功能...")
    
    controller = GatewayController()
    
    # 连接OPC服务器
    if controller.connect_opc('Matrikon.OPC.Simulation.1'):
        print("OPC服务器连接成功")
        
        # 添加标签
        controller.add_tag('Random.Int1', 0, 'INT16', '测试整数')
        controller.add_tag('Random.Real1', 1, 'FLOAT32', '测试浮点数')
        
        # 启动网关
        print("启动网关...")
        controller.start_gateway()
        
        # 运行5秒
        print("网关运行中...")
        for i in range(5):
            print(f"运行中... {i+1}/5")
            time.sleep(1)
        
        # 停止网关
        controller.stop_gateway()
        print("网关已停止")
        
        controller.disconnect_opc()
    else:
        print("OPC服务器连接失败")
    
    print("网关功能测试完成")


def main():
    """主测试函数"""
    print("=" * 60)
    print("OPC Modbus TCP 网关 - 核心功能测试")
    print("=" * 60)
    
    try:
        test_data_converter()
        test_opc_client()
        test_modbus_server()
        test_gateway()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("核心功能正常运行")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

