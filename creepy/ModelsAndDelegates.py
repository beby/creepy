from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
 

class PluginConfigurationListModel(QAbstractListModel):
    def __init__(self, plugins, parent=None):
        super(PluginConfigurationListModel, self).__init__(parent)
        self.plugins = plugins
       
        
    def rowCount(self,index):
        return len(self.plugins)
    
    
    def data(self,index,role):
        plugin= self.plugins[index.row()]
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(plugin.name)
            if role == Qt.DecorationRole:
                if plugin.plugin_object.configured:
                    return  QPixmap(os.path.join(os.getcwd(), "creepy", "include", "add.png"))
                else:
                    return  QPixmap(os.path.join(os.getcwd(), "creepy", "include", "analyze.png"))
        else: 
            return QVariant()
        
    
class ProjectWizardPluginListModel(QAbstractListModel):
    def __init__(self, plugins, parent=None):
        super(ProjectWizardPluginListModel, self).__init__(parent)
        self.plugins = plugins
        self.checkedPlugins = set()
    
    def rowCount(self, index):
        return len(self.plugins)
    
    def data(self, index, role):
        plugin = self.plugins[index.row()][0]
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(plugin.name)
            if role == Qt.DecorationRole:
                return  QPixmap(os.path.join(os.getcwd(), "creepy", "include", "add.png"))
            if role == Qt.CheckStateRole:
                if plugin:
                    return (Qt.Checked if plugin.name in self.checkedPlugins else Qt.Unchecked)
                    
        else: 
            return QVariant()
                  
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            plugin = self.plugins[index.row()][0]
            if value == Qt.Checked:
                self.checkedPlugins.add(plugin.name)
            else:
                self.checkedPlugins.discard(plugin.name)
            return True
        return QFileSystemModel.setData(self, index, value, role)
                  
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractListModel.flags(self, index)|Qt.ItemIsUserCheckable)

    
    
class ProjectWizardPossibleTargetsTable(QAbstractTableModel):
    def __init__(self, targets, parents=None):
        super(ProjectWizardPossibleTargetsTable, self).__init__()
        self.targets = targets
        
    def rowCount(self, index):
        return len(self.targets)
    
    def columnCount(self, index):
        return 5
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == 0:
                return QVariant("Plugin")
            elif section == 1:
                return QVariant("Picture")
            elif section == 2:
                return QVariant("Username")
            elif section == 3:
                return QVariant("Full Name")
            elif section == 4:
                return QVariant("Details")
        return QVariant(int(section + 1))

    
    def data(self, index, role):
        target = self.targets[index.row()]
        if index.isValid() and (0 <= index.row() < len(self.targets)) and target: 
            column = index.column()
            if role == Qt.DecorationRole:
                if column == 1:
                    picturePath = os.path.join(os.getcwd(), "creepy", "temp", target['targetPicture'])
                    if picturePath and os.path.exists(picturePath):
                        pixmap = QPixmap(picturePath)
                        return QIcon(pixmap.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.FastTransformation))
                    else:
                        pixmap = QPixmap(os.path.join(os.getcwd(), "creepy", "include", "add.png"))
                        pixmap.scaled(20, 20, Qt.IgnoreAspectRatio)
                        return QIcon(pixmap)
            if role == Qt.DisplayRole:
                if column == 0:
                    return QVariant(target['pluginName'])
                elif column == 1:
                    return QVariant()
                elif column == 2:
                    return QVariant(target['targetUsername'])
                elif column == 3:
                    return QVariant(target['targetFullname'])
                elif column == 4:
                    return QVariant(target['targetDetails'])
                
            
        else: 
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled)
        
    def mimeTypes(self):
        return [ "application/target.tableitem.creepy" ] 
    
    def mimeData(self, indices):
        mimeData = QMimeData()
        encodedData = QByteArray()
        stream = QDataStream(encodedData, QIODevice.WriteOnly)
        for index in indices:
            if index.column() == 1:
                d = QVariant(self.data(index, Qt.DecorationRole))
            else:
                d = QVariant(self.data(index, Qt.DisplayRole).toString())
            stream << d
        mimeData.setData("application/target.tableitem.creepy", encodedData)
        return mimeData  
           
class ProjectWizardSelectedTargetsTable(QAbstractTableModel):
    def __init__(self, targets, parents=None):
        super(ProjectWizardSelectedTargetsTable, self).__init__()
        self.targets = targets
        
    def rowCount(self,index):
        return len(self.targets)
    
    def columnCount(self,index):
        return 5
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == 0:
                return QVariant("Plugin")
            elif section == 1:
                return QVariant("Picture")
            elif section == 2:
                return QVariant("Username")
            elif section == 3:
                return QVariant("Full Name")
            elif section == 4:
                return QVariant("Details")
        return QVariant(int(section + 1))

    
    def data(self, index, role):
        target = self.targets[index.row()]
        
        if index.isValid() and target:
            column = index.column()
            if role == Qt.DecorationRole:
                if column == 1:
                    pixmap = target['targetPicture']
                    return pixmap
            if role == Qt.DisplayRole:
                if column == 0:
                    return QVariant(target['pluginName'])
                if column == 1:
                    return QVariant()
                elif column == 2:
                    return QVariant(target['targetUsername'])
                elif column == 3:
                    return QVariant(target['targetFullname'])
                elif column == 4:
                    return QVariant(target['targetDetails'])
                
                
            else: 
                return QVariant()

    
    def insertRow(self, row, parent=QModelIndex()):
        self.insertRows(row, 1, parent)

    def insertRows(self, rows, count, parent=QModelIndex()):
        for row in rows:
            self.targets.append(row)
            self.beginInsertRows(parent, len(self.targets), len(self.targets))
            self.endInsertRows()
        
        
        return True
    
    def flags(self, index):
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|Qt.ItemIsDropEnabled)
        
    def mimeTypes(self):
        return [ "application/target.tableitem.creepy" ] 
        
    def dropMimeData(self, data, action, row, column, parent):
        if data.hasFormat("application/target.tableitem.creepy"):
            encodedData = data.data("application/target.tableitem.creepy")
            stream = QDataStream(encodedData, QIODevice.ReadOnly)
            columnsList = []
            qVariant = QVariant()
            while not stream.atEnd():
                stream >> qVariant
                columnsList.append(qVariant.toPyObject()) 
            draggedRows = [columnsList[x:x+5] for x in range(0,len(columnsList),5)]
            droppedRows = []
            for row in draggedRows:
                #Ensure we are not putting duplicates in the target list
                if all(row[2] != target['targetUsername'] and row[0] != target['pluginName'] for target in self.targets):
                    droppedRows.append({'targetUsername':row[3], 'targetFullname':row[2], 'targetPicture':row[1], 'targetDetails':row[4], 'pluginName':row[0]})
            self.insertRows(droppedRows, len(droppedRows), parent)
                
        return True        
            