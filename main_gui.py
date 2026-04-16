
"""
OPC Modbus TCP 网关主界面
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QFileDialog, QMessageBox, QGroupBox,
                             QSplitter, QSpinBox, QStatusBar, QTabWidget)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from gateway_controller import GatewayController
from config import DATA_TYPES


class SignalHandler(QObject):
    """信号处理类，用于线程安全的UI更新"""
    log_message = pyqtSignal(str)
    data_updated = pyqtSignal(dict)


class GatewayGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = GatewayController()
        self.signal_handler = SignalHandler()
        
        self.controller.opc_client.on_data_update = self._on_data_update_callback
        
        self.init_ui()
        self.init_signals()
        self.apply_tags_to_table()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('OPC Modbus TCP 网关 v1.0')
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        top_panel = self.create_top_panel()
        main_layout.addWidget(top_panel)
        
        splitter = QSplitter(Qt.Vertical)
        
        tags_panel = self.create_tags_panel()
        splitter.addWidget(tags_panel)
        
        log_panel = self.create_log_panel()
        splitter.addWidget(log_panel)
        
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status('就绪')
    
    def create_top_panel(self) -> QWidget:
        """创建顶部控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        opc_group = QGroupBox('OPC DA 配置')
        opc_layout = QHBoxLayout(opc_group)
        
        opc_layout.addWidget(QLabel('OPC服务器:'))
        self.opc_server_combo = QComboBox()
        self.opc_server_combo.setEditable(True)
        self.refresh_opc_servers()
        opc_layout.addWidget(self.opc_server_combo, 1)
        
        self.btn_refresh_servers = QPushButton('刷新服务器')
        self.btn_refresh_servers.clicked.connect(self.refresh_opc_servers)
        opc_layout.addWidget(self.btn_refresh_servers)
        
        self.btn_connect_opc = QPushButton('连接')
        self.btn_connect_opc.clicked.connect(self.toggle_opc_connection)
        opc_layout.addWidget(self.btn_connect_opc)
        
        layout.addWidget(opc_group)
        
        modbus_group = QGroupBox('Modbus TCP 配置')
        modbus_layout = QHBoxLayout(modbus_group)
        
        modbus_layout.addWidget(QLabel('端口:'))
        self.modbus_port_spin = QSpinBox()
        self.modbus_port_spin.setRange(1, 65535)
        self.modbus_port_spin.setValue(502)
        modbus_layout.addWidget(self.modbus_port_spin)
        
        modbus_layout.addWidget(QLabel('刷新间隔(ms):'))
        self.refresh_rate_spin = QSpinBox()
        self.refresh_rate_spin.setRange(100, 60000)
        self.refresh_rate_spin.setValue(1000)
        modbus_layout.addWidget(self.refresh_rate_spin)
        
        modbus_layout.addStretch()
        
        self.btn_start_gateway = QPushButton('启动网关')
        self.btn_start_gateway.setMinimumWidth(120)
        self.btn_start_gateway.clicked.connect(self.toggle_gateway)
        modbus_layout.addWidget(self.btn_start_gateway)
        
        layout.addWidget(modbus_group)
        
        file_group = QGroupBox('工程管理')
        file_layout = QHBoxLayout(file_group)
        
        self.btn_new_project = QPushButton('新建工程')
        self.btn_new_project.clicked.connect(self.new_project)
        file_layout.addWidget(self.btn_new_project)
        
        self.btn_load_project = QPushButton('加载工程')
        self.btn_load_project.clicked.connect(self.load_project)
        file_layout.addWidget(self.btn_load_project)
        
        self.btn_save_project = QPushButton('保存工程')
        self.btn_save_project.clicked.connect(self.save_project)
        file_layout.addWidget(self.btn_save_project)
        
        file_layout.addWidget(QLabel('    '))
        
        self.btn_import_csv = QPushButton('导入CSV')
        self.btn_import_csv.clicked.connect(self.import_csv)
        file_layout.addWidget(self.btn_import_csv)
        
        self.btn_export_csv = QPushButton('导出CSV')
        self.btn_export_csv.clicked.connect(self.export_csv)
        file_layout.addWidget(self.btn_export_csv)
        
        file_layout.addStretch()
        
        layout.addWidget(file_group)
        
        return panel
    
    def create_tags_panel(self) -> QWidget:
        """创建标签管理面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        add_tag_layout = QHBoxLayout()
        
        add_tag_layout.addWidget(QLabel('OPC标签:'))
        self.tag_name_edit = QLineEdit()
        self.tag_name_edit.setPlaceholderText('例如: Random.Int1')
        add_tag_layout.addWidget(self.tag_name_edit, 1)
        
        add_tag_layout.addWidget(QLabel('寄存器地址:'))
        self.register_addr_spin = QSpinBox()
        self.register_addr_spin.setRange(0, 65535)
        add_tag_layout.addWidget(self.register_addr_spin)
        
        add_tag_layout.addWidget(QLabel('数据类型:'))
        self.data_type_combo = QComboBox()
        for dtype in DATA_TYPES.keys():
            self.data_type_combo.addItem(dtype)
        add_tag_layout.addWidget(self.data_type_combo)
        
        add_tag_layout.addWidget(QLabel('描述:'))
        self.tag_desc_edit = QLineEdit()
        self.tag_desc_edit.setPlaceholderText('标签描述')
        add_tag_layout.addWidget(self.tag_desc_edit, 1)
        
        self.btn_add_tag = QPushButton('添加标签')
        self.btn_add_tag.clicked.connect(self.add_tag)
        add_tag_layout.addWidget(self.btn_add_tag)
        
        layout.addLayout(add_tag_layout)
        
        self.tags_table = QTableWidget()
        self.tags_table.setColumnCount(5)
        self.tags_table.setHorizontalHeaderLabels(['OPC标签', '寄存器地址', '数据类型', '描述', '当前值'])
        self.tags_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tags_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.tags_table)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_remove_tag = QPushButton('删除选中标签')
        self.btn_remove_tag.clicked.connect(self.remove_selected_tag)
        btn_layout.addWidget(self.btn_remove_tag)
        
        self.btn_clear_tags = QPushButton('清空所有标签')
        self.btn_clear_tags.clicked.connect(self.clear_tags)
        btn_layout.addWidget(self.btn_clear_tags)
        
        layout.addLayout(btn_layout)
        
        return panel
    
    def create_log_panel(self) -> QWidget:
        """创建日志面板"""
        panel = QGroupBox('运行日志')
        layout = QVBoxLayout(panel)
        
        self.log_text = QTableWidget()
        self.log_text.setColumnCount(2)
        self.log_text.setHorizontalHeaderLabels(['时间', '消息'])
        self.log_text.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.log_text.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.log_text.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.log_text)
        
        return panel
    
    def init_signals(self):
        """初始化信号连接"""
        self.signal_handler.log_message.connect(self.append_log)
        self.signal_handler.data_updated.connect(self.update_tags_values)
    
    def refresh_opc_servers(self):
        """刷新OPC服务器列表"""
        current_text = self.opc_server_combo.currentText()
        self.opc_server_combo.clear()
        
        servers = self.controller.get_available_opc_servers()
        for server in servers:
            self.opc_server_combo.addItem(server)
        
        if current_text:
            index = self.opc_server_combo.findText(current_text)
            if index >= 0:
                self.opc_server_combo.setCurrentIndex(index)
    
    def toggle_opc_connection(self):
        """切换OPC连接状态"""
        if self.controller.opc_client.connected:
            self.controller.disconnect_opc()
            self.btn_connect_opc.setText('连接')
            self.opc_server_combo.setEnabled(True)
            self.btn_refresh_servers.setEnabled(True)
            self.update_status('OPC已断开')
            self.append_log('OPC服务器已断开连接')
        else:
            server_name = self.opc_server_combo.currentText()
            if not server_name:
                QMessageBox.warning(self, '警告', '请选择OPC服务器')
                return
            
            if self.controller.connect_opc(server_name):
                self.btn_connect_opc.setText('断开')
                self.opc_server_combo.setEnabled(False)
                self.btn_refresh_servers.setEnabled(False)
                self.update_status('OPC已连接')
                self.append_log(f'已连接到OPC服务器: {server_name}')
            else:
                QMessageBox.critical(self, '错误', '连接OPC服务器失败')
    
    def toggle_gateway(self):
        """切换网关运行状态"""
        if self.controller.is_running():
            self.controller.stop_gateway()
            self.btn_start_gateway.setText('启动网关')
            self.btn_start_gateway.setStyleSheet('')
            self.update_status('网关已停止')
            self.append_log('网关已停止')
        else:
            if not self.controller.opc_client.connected:
                server_name = self.opc_server_combo.currentText()
                if not server_name:
                    QMessageBox.warning(self, '警告', '请先连接OPC服务器')
                    return
                if not self.controller.connect_opc(server_name):
                    QMessageBox.critical(self, '错误', '连接OPC服务器失败')
                    return
            
            self.controller.project_manager.set_modbus_port(self.modbus_port_spin.value())
            self.controller.project_manager.set_refresh_rate(self.refresh_rate_spin.value())
            
            self.controller.start_gateway()
            self.btn_start_gateway.setText('停止网关')
            self.btn_start_gateway.setStyleSheet('background-color: #ff6b6b; color: white;')
            self.update_status('网关运行中')
            self.append_log('网关已启动')
    
    def add_tag(self):
        """添加标签"""
        tag_name = self.tag_name_edit.text().strip()
        register_addr = self.register_addr_spin.value()
        data_type = self.data_type_combo.currentText()
        description = self.tag_desc_edit.text().strip()
        
        if not tag_name:
            QMessageBox.warning(self, '警告', '请输入OPC标签名称')
            return
        
        self.controller.add_tag(tag_name, register_addr, data_type, description)
        self.apply_tags_to_table()
        
        self.tag_name_edit.clear()
        self.tag_desc_edit.clear()
        self.register_addr_spin.setValue(self.register_addr_spin.value() + DATA_TYPES[data_type]['length'])
        
        self.append_log(f'已添加标签: {tag_name}')
    
    def remove_selected_tag(self):
        """删除选中的标签"""
        current_row = self.tags_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的标签')
            return
        
        tag_item = self.tags_table.item(current_row, 0)
        if tag_item:
            tag_name = tag_item.text()
            self.controller.remove_tag(tag_name)
            self.apply_tags_to_table()
            self.append_log(f'已删除标签: {tag_name}')
    
    def clear_tags(self):
        """清空所有标签"""
        reply = QMessageBox.question(
            self, '确认', '确定要清空所有标签吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.controller.opc_client.tags.clear()
            self.apply_tags_to_table()
            self.append_log('已清空所有标签')
    
    def apply_tags_to_table(self):
        """将标签应用到表格"""
        self.tags_table.setRowCount(0)
        
        for tag_name, tag_info in self.controller.opc_client.tags.items():
            row = self.tags_table.rowCount()
            self.tags_table.insertRow(row)
            
            self.tags_table.setItem(row, 0, QTableWidgetItem(tag_name))
            self.tags_table.setItem(row, 1, QTableWidgetItem(str(tag_info['register_addr'])))
            self.tags_table.setItem(row, 2, QTableWidgetItem(tag_info['data_type']))
            self.tags_table.setItem(row, 3, QTableWidgetItem(tag_info['description']))
            
            value = tag_info.get('last_value', '-')
            self.tags_table.setItem(row, 4, QTableWidgetItem(str(value)))
    
    def new_project(self):
        """新建工程"""
        reply = QMessageBox.question(
            self, '确认', '新建工程将清空当前配置，确定继续吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.controller.opc_client.tags.clear()
            self.controller.project_manager.__init__()
            self.apply_tags_to_table()
            self.opc_server_combo.setCurrentText('')
            self.modbus_port_spin.setValue(502)
            self.refresh_rate_spin.setValue(1000)
            self.append_log('已新建工程')
    
    def load_project(self):
        """加载工程"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '加载工程', '', '工程文件 (*.json);;所有文件 (*.*)'
        )
        
        if file_path:
            if self.controller.load_project(file_path):
                self.opc_server_combo.setCurrentText(self.controller.project_manager.get_opc_server())
                self.modbus_port_spin.setValue(self.controller.project_manager.get_modbus_port())
                self.refresh_rate_spin.setValue(self.controller.project_manager.get_refresh_rate())
                self.apply_tags_to_table()
                self.append_log(f'已加载工程: {file_path}')
            else:
                QMessageBox.critical(self, '错误', '加载工程失败')
    
    def save_project(self):
        """保存工程"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存工程', '', '工程文件 (*.json);;所有文件 (*.*)'
        )
        
        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            if self.controller.save_project(file_path):
                self.append_log(f'工程已保存到: {file_path}')
            else:
                QMessageBox.critical(self, '错误', '保存工程失败')
    
    def import_csv(self):
        """导入CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '导入CSV', '', 'CSV文件 (*.csv);;所有文件 (*.*)'
        )
        
        if file_path:
            if self.controller.project_manager.import_csv(file_path):
                self.controller._apply_project_config()
                self.apply_tags_to_table()
                self.append_log(f'已从CSV导入: {file_path}')
            else:
                QMessageBox.critical(self, '错误', '导入CSV失败')
    
    def export_csv(self):
        """导出CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, '导出CSV', '', 'CSV文件 (*.csv);;所有文件 (*.*)'
        )
        
        if file_path:
            if not file_path.endswith('.csv'):
                file_path += '.csv'
            
            self.controller._update_project_from_current()
            if self.controller.project_manager.export_csv(file_path):
                self.append_log(f'CSV已导出到: {file_path}')
            else:
                QMessageBox.critical(self, '错误', '导出CSV失败')
    
    def _on_data_update_callback(self, data):
        """数据更新回调（线程安全）"""
        self.signal_handler.data_updated.emit(data)
    
    def update_tags_values(self, data):
        """更新标签值显示"""
        for row in range(self.tags_table.rowCount()):
            tag_item = self.tags_table.item(row, 0)
            if tag_item:
                tag_name = tag_item.text()
                if tag_name in data:
                    value = data[tag_name].get('value', '-')
                    self.tags_table.setItem(row, 4, QTableWidgetItem(str(value)))
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.showMessage(message)
    
    def append_log(self, message):
        """添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        row = self.log_text.rowCount()
        self.log_text.insertRow(row)
        self.log_text.setItem(row, 0, QTableWidgetItem(timestamp))
        self.log_text.setItem(row, 1, QTableWidgetItem(message))
        
        self.log_text.scrollToBottom()
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.controller.is_running():
            self.controller.stop_gateway()
        
        self.controller.disconnect_opc()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    gui = GatewayGUI()
    gui.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

