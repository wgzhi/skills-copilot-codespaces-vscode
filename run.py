
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPC Modbus TCP 网关启动脚本
"""

import sys
import os


def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'PyQt5',
        'pymodbus',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("OPC Modbus TCP 网关 v1.0")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    try:
        from main_gui import main
        print("正在启动图形界面...")
        main()
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

