import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import BodyLabel, MessageBoxBase

from app.config import ASSETS_PATH


class DonateDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Define QR code paths
        self.WECHAT_QR_PATH = os.path.join(ASSETS_PATH, "donate_green.jpg")
        self.ALIPAY_QR_PATH = os.path.join(ASSETS_PATH, "donate_blue.jpg")

        self.setup_ui()
        self.setWindowTitle(self.tr("支持作者"))

    def setup_ui(self):
        # Create title label
        self.titleLabel = BodyLabel(self.tr("感谢支持"), self)

        # Create description text
        self.descLabel = BodyLabel(
            self.tr(
                "目前本人精力有限，您的支持让我有动力继续折腾这个项目！\n感谢您对开源事业的热爱与支持！"
            ),
            self,
        )
        self.descLabel.setAlignment(Qt.AlignCenter)  # type: ignore

        # Create horizontal layout for two QR codes
        self.qrLayout = QHBoxLayout()

        # Create Alipay QR code label
        self.alipayContainer = QVBoxLayout()
        self.alipayQR = QLabel()
        self.alipayQR.setPixmap(
            QPixmap(self.ALIPAY_QR_PATH).scaled(
                300,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.SmoothTransformation,  # type: ignore
            )
        )
        self.alipayLabel = BodyLabel(self.tr("支付宝"))
        self.alipayLabel.setAlignment(Qt.AlignCenter)  # type: ignore
        self.alipayContainer.addWidget(self.alipayQR, alignment=Qt.AlignCenter)  # type: ignore
        self.alipayContainer.addWidget(self.alipayLabel)

        # Create WeChat QR code label
        self.wechatContainer = QVBoxLayout()
        self.wechatQR = QLabel()
        self.wechatQR.setPixmap(
            QPixmap(self.WECHAT_QR_PATH).scaled(
                300,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.SmoothTransformation,  # type: ignore
            )
        )
        self.wechatLabel = BodyLabel(self.tr("微信"))
        self.wechatLabel.setAlignment(Qt.AlignCenter)  # type: ignore
        self.wechatContainer.addWidget(self.wechatQR, alignment=Qt.AlignCenter)  # type: ignore
        self.wechatContainer.addWidget(self.wechatLabel)

        # Add QR codes to horizontal layout
        self.qrLayout.addLayout(self.alipayContainer)
        self.qrLayout.addLayout(self.wechatContainer)

        self.viewLayout.setSpacing(30)
        # Add to main layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.descLabel)
        # Add vertical spacing
        self.viewLayout.addLayout(self.qrLayout)

        # Set dialog minimum width
        self.widget.setMinimumWidth(800)
        # Set dialog minimum height
        self.widget.setMinimumHeight(500)

        # Hide yes button, only show cancel button
        self.yesButton.hide()
        self.cancelButton.setText(self.tr("关闭"))
