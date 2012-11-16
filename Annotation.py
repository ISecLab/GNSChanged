# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# code@gns3.net
#

from PyQt4 import QtGui, QtCore
import GNS3.Globals as globals
import GNS3.UndoFramework as undo

class Annotation(QtGui.QGraphicsTextItem):
    """ Text annotation for the topology
    """

    def __init__(self, parent=None):

        QtGui.QGraphicsTextItem.__init__(self, parent)
        self.setFont(QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold))
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.rotation = 0
        #self.autoGenerated = False
        self.deviceName = None
        self.deviceIf = None
        self.setZValue(1)
        self.prevText = None
        
    def keyPressEvent(self, event):

        key = event.key()
        if key == QtCore.Qt.Key_Left and event.modifiers() == QtCore.Qt.AltModifier and self.rotation > -360:
            if self.rotation:
                self.rotate(-self.rotation)
            self.rotation -= 1
            self.rotate(self.rotation)
        elif key == QtCore.Qt.Key_Right and event.modifiers() == QtCore.Qt.AltModifier and self.rotation < 360:
            if self.rotation:
                self.rotate(-self.rotation)
            self.rotation += 1
            self.rotate(self.rotation)
        else:
            QtGui.QGraphicsTextItem.keyPressEvent(self, event)

    def editText(self):

        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setSelected(True)
        self.setFocus()
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)

    def mouseDoubleClickEvent(self, event):

        self.prevText = self.toPlainText()
        self.editText()

    def focusOutEvent(self, event):

        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, False)

        # unselect text
        cursor = self.textCursor()
        if (cursor.hasSelection()):
            cursor.clearSelection()
            self.setTextCursor(cursor)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        if self.toPlainText().isEmpty():
            globals.GApp.topology.removeItem(self)
            return
        if self.prevText and self.prevText != self.toPlainText():
#            if self.autoGenerated:
#                self.autoGenerated = False
            command = undo.NewAnnotationText(self, self.prevText)
            globals.GApp.topology.undoStack.push(command)
        return QtGui.QGraphicsTextItem.focusOutEvent(self, event)

    def paint(self, painter, option, widget=None):
        
        QtGui.QGraphicsTextItem.paint(self, painter, option, widget)
        
        # Don't draw if not activated
        if globals.GApp.workspace.flg_showLayerPos == False:
            return
        
        # Show layer level of this node
        brect = self.boundingRect()
        
        # Don't draw if the object is too small ...
        if brect.width() < 20 or brect.height() < 20:
            return
        
        center = self.mapFromItem(self, brect.width() / 2.0, brect.height() / 2.0)
        
        painter.setBrush(QtCore.Qt.red)
        painter.setPen(QtCore.Qt.red)
        painter.drawRect((brect.width() / 2.0) - 10, (brect.height() / 2.0) - 10, 20,20)
        
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("TypeWriter", 14, QtGui.QFont.Bold))
        zval = str(int(self.zValue()))
        painter.drawText(QtCore.QPointF(center.x() - 4, center.y() + 4), zval)

