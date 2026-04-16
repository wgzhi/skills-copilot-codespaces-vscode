
# OPC Modbus TCP 网关

一款功能强大的工业通信网关软件，实现OPC DA到Modbus TCP协议的转换。

## 功能特性

1. **OPC DA 客户端** - 支持从OPC DA服务器获取数据
2. **Modbus TCP 服务器** - 提供标准的Modbus TCP服务器功能
3. **多种数据类型支持** - INT16、UINT16、INT32、UINT32、FLOAT32、FLOAT64、INT64、UINT64
4. **工程管理** - 支持工程的保存与加载
5. **CSV 导入导出** - 方便批量配置标签
6. **无限制寄存器** - 支持65536个寄存器地址空间

## 系统要求

- Python 3.7+
- Windows操作系统（OPC DA需要Windows环境）

## 安装步骤

### 1. 克隆或下载项目

```bash
cd /workspace
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 运行程序

```bash
python main_gui.py
```

### 基本使用流程

1. **配置OPC DA服务器
   - 在"OPC DA配置"区域选择或输入OPC服务器名称
   - 点击"连接"按钮连接到OPC服务器

2. **配置Modbus TCP服务器
   - 设置Modbus端口（默认502）
   - 设置数据刷新间隔

3. **添加标签映射**
   - 输入OPC标签名称
   - 设置对应的Modbus寄存器地址
   - 选择数据类型
   - 点击"添加标签"

4. **启动网关**
   - 点击"启动网关"按钮开始数据转发

## 数据类型说明

| 数据类型 | 长度（寄存器） | 说明 |
|---------|--------------|------|
| INT16 | 1 | 16位有符号整数 |
| UINT16 | 1 | 16位无符号整数 |
| INT32 | 2 | 32位有符号整数 |
| UINT32 | 2 | 32位无符号整数 |
| FLOAT32 | 2 | 32位浮点数 |
| FLOAT64 | 4 | 64位浮点数 |
| INT64 | 4 | 64位有符号整数 |
| UINT64 | 4 | 64位无符号整数 |

## CSV文件格式

导入/导出的CSV文件应包含以下列：

- `tag_name`: OPC标签名称
- `register_addr`: Modbus寄存器地址
- `data_type`: 数据类型
- `description`: 标签描述
- `register_type`: 寄存器类型（holding/input）

示例CSV内容：

```csv
tag_name,register_addr,data_type,description,register_type
Random.Int1,0,INT16,随机整数1,holding
Random.Real1,1,FLOAT32,随机浮点数1,holding
```

## 工程文件格式

工程文件使用JSON格式保存，包含以下信息：
- OPC服务器配置
- Modbus端口配置
- 刷新速率
- 标签映射配置

## 注意事项

1. **OPC DA需要在Windows环境下运行，本软件提供模拟模式可在任何环境下测试
2. 首次使用建议先用模拟模式测试功能
3. 生产环境请确保OPC服务器已正确安装并运行
4. Modbus端口502可能需要管理员权限
5. 确保防火墙允许Modbus TCP连接

## 常见问题

### Q: 如何连接到真实的OPC DA服务器？

A: 在Windows环境下，安装OpenOPC库：

```bash
pip install pywin32
pip install OpenOPC-Python3x
```

### Q: 支持哪些OPC DA服务器？

A: 支持所有标准的OPC DA服务器，如：
- Matrikon OPC Simulation Server
- Kepware KEPServerEX
- Siemens OPC Server
- 其他符合OPC DA 2.0/3.0规范的服务器

### Q: Modbus TCP客户端如何连接？

A: 使用任何标准的Modbus TCP客户端软件，如：
- Modbus Poll
- Modbus Master
- 自行开发的Modbus TCP客户端

## 项目结构

```
/workspace/
├── config.py              # 配置文件
├── data_converter.py     # 数据类型转换模块
├── opc_client.py        # OPC DA客户端模块
├── modbus_server.py      # Modbus TCP服务器模块
├── project_manager.py   # 工程管理模块
├── gateway_controller.py # 主控制器模块
├── main_gui.py          # 图形用户界面
├── requirements.txt      # 依赖包列表
└── README.md            # 说明文档
```

## 技术栈

- **GUI框架**: PyQt5
- **Modbus协议**: pymodbus
- **OPC DA**: OpenOPC (Windows环境)
- **数据处理**: struct, numpy

## 许可证

本项目仅供学习和商业使用。

## 支持

如有问题或建议，请联系开发者。

