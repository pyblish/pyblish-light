from Qt import QtWidgets, QtGui, QtCore

from . import model


class Item(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(Item, self).__init__()

        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(8)
        font.setWeight(400)

        self.font = font
        self.colors = {
            "warning": QtGui.QColor("#EE2222"),
            "ok": QtGui.QColor("#77AE24"),
            "active": QtGui.QColor("#99CEEE"),
            "idle": QtCore.Qt.white,
            "font": QtGui.QColor("#DDD"),
            "inactive": QtGui.QColor("#888"),
            "hover": QtGui.QColor(255, 255, 255, 10),
            "selected": QtGui.QColor(255, 255, 255, 20),
        }

    def paint(self, painter, option, index):
        """Paint checkbox and text
         _
        |_|  My label

        """

        rect = QtCore.QRectF(option.rect)
        rect.setWidth(rect.height())
        rect.adjust(6, 6, -6, -6)

        path = QtGui.QPainterPath()
        path.addRect(rect)

        check_color = self.colors["idle"]

        if index.data(model.IsProcessing) is True:
            check_color = self.colors["active"]

        elif index.data(model.HasFailed) is True:
            check_color = self.colors["warning"]

        elif index.data(model.HasSucceeded) is True:
            check_color = self.colors["ok"]

        elif index.data(model.HasProcessed) is True:
            check_color = self.colors["ok"]

        metrics = painter.fontMetrics()

        rect = QtCore.QRectF(option.rect.adjusted(rect.width() + 12, 2, 0, -2))
        assert rect.width() > 0

        label = index.data(model.Label)
        label = metrics.elidedText(label,
                                   QtCore.Qt.ElideRight,
                                   rect.width() - 20)

        font_color = self.colors["idle"]
        if not index.data(model.IsChecked):
            font_color = self.colors["inactive"]

        hover = QtGui.QPainterPath()
        hover.addRect(option.rect.adjusted(0, 0, -1, -1))

        # Maintan reference to state, so we can restore it once we're done
        painter.save()

        # Draw label
        painter.setFont(self.font)
        painter.setPen(QtGui.QPen(font_color))
        painter.drawText(rect, label)

        # Draw checkbox
        pen = QtGui.QPen(check_color, 1)
        painter.setPen(pen)

        if index.data(model.IsOptional):
            painter.drawPath(path)

            if index.data(model.IsChecked):
                painter.fillPath(path, check_color)

        elif not index.data(model.IsIdle) and index.data(model.IsChecked):
                painter.fillPath(path, check_color)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.fillPath(hover, self.colors["hover"])

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillPath(hover, self.colors["selected"])

        # Ok, we're done, tidy up.
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(option.rect.width(), 20)


class Terminal(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(Terminal, self).__init__()

        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(8)
        font.setWeight(400)

        self.font = font
        self.colors = {
            "warning": QtGui.QColor("#EE2222"),
            "ok": QtGui.QColor("#77AE24"),
            "active": QtGui.QColor("#99CEEE"),
            "idle": QtCore.Qt.white,
            "font": QtGui.QColor("#DDD"),
            "inactive": QtGui.QColor("#888"),
            "hover": QtGui.QColor(255, 255, 255, 10),
            "selected": QtGui.QColor(255, 255, 255, 20),
        }

    def paint(self, painter, option, index):
        """Paint checkbox and text
         _
        |_|  My label

        """

        rect = QtCore.QRectF(option.rect)
        rect.setWidth(rect.height())
        rect.adjust(6, 6, -6, -6)

        path = QtGui.QPainterPath()
        path.addRect(rect)

        metrics = painter.fontMetrics()

        rect = QtCore.QRectF(option.rect.adjusted(rect.width() + 12, 2, 0, -2))
        assert rect.width() > 0

        label = index.data(model.Label)
        label = metrics.elidedText(label,
                                   QtCore.Qt.ElideRight,
                                   rect.width() - 20)

        font_color = self.colors["idle"]

        hover = QtGui.QPainterPath()
        hover.addRect(option.rect.adjusted(0, 0, -1, -1))

        # Maintan reference to state, so we can restore it once we're done
        painter.save()

        # Draw label
        painter.setFont(self.font)
        painter.setPen(QtGui.QPen(font_color))
        painter.drawText(rect, label)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.fillPath(hover, self.colors["hover"])

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillPath(hover, self.colors["selected"])

        # Ok, we're done, tidy up.
        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(option.rect.width(), 20)