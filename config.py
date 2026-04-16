
"""
配置文件
"""

DEFAULT_MODBUS_PORT = 502
DEFAULT_OPC_REFRESH_RATE = 1000  # ms
MAX_REGISTERS = 65536

DATA_TYPES = {
    'INT16': {'length': 1, 'signed': True},
    'UINT16': {'length': 1, 'signed': False},
    'INT32': {'length': 2, 'signed': True},
    'UINT32': {'length': 2, 'signed': False},
    'FLOAT32': {'length': 2, 'signed': True},
    'FLOAT64': {'length': 4, 'signed': True},
    'INT64': {'length': 4, 'signed': True},
    'UINT64': {'length': 4, 'signed': False},
}

