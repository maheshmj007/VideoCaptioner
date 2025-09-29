import webbrowser

from PyQt5.QtCore import Qt, QThread, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog, QLabel, QWidget
from qfluentwidgets import (
    ComboBoxSettingCard,
    CustomColorSettingCard,
    ExpandLayout,
    HyperlinkCard,
    InfoBar,
    OptionsSettingCard,
    PrimaryPushSettingCard,
    PushSettingCard,
    RangeSettingCard,
    ScrollArea,
    SettingCardGroup,
    SwitchSettingCard,
    setTheme,
    setThemeColor,
)
from qfluentwidgets import FluentIcon as FIF

from app.common.config import cfg
from app.common.signal_bus import signalBus
from app.components.EditComboBoxSettingCard import EditComboBoxSettingCard
from app.components.LineEditSettingCard import LineEditSettingCard
from app.config import AUTHOR, FEEDBACK_URL, HELP_URL, RELEASE_URL, VERSION, YEAR
from app.core.entities import LLMServiceEnum, TranslatorServiceEnum
from app.core.utils.test_opanai import get_openai_models, test_openai


class SettingInterface(ScrollArea):
    """Settings Interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(self.tr("Settings"))
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # 初始化所有设置组
        self.__initGroups()
        # 初始化所有配置卡片
        self.__initCards()
        # 初始化界面
        self.__initWidget()
        # 初始化布局
        self.__initLayout()
        # 连接信号和槽
        self.__connectSignalToSlot()

    def __initGroups(self):
        """Initialize all setting groups"""
        # Transcription group
        self.transcribeGroup = SettingCardGroup(self.tr("Transcription"), self.scrollWidget)
        # LLM configuration group
        self.llmGroup = SettingCardGroup(self.tr("LLM Configuration"), self.scrollWidget)
        # Translation service group
        self.translate_serviceGroup = SettingCardGroup(
            self.tr("Translation Service"), self.scrollWidget
        )
        # Translation & optimization group
        self.translateGroup = SettingCardGroup(self.tr("Translation & Optimization"), self.scrollWidget)
        # Subtitle synthesis group
        self.subtitleGroup = SettingCardGroup(
            self.tr("Subtitle Synthesis"), self.scrollWidget
        )
        # Save settings group
        self.saveGroup = SettingCardGroup(self.tr("Save Settings"), self.scrollWidget)
        # Personalization group
        self.personalGroup = SettingCardGroup(self.tr("Personalization"), self.scrollWidget)
        # About group
        self.aboutGroup = SettingCardGroup(self.tr("About"), self.scrollWidget)

    def __initCards(self):
        """Initialize all configuration cards"""
        # Transcription cards
        self.transcribeModelCard = ComboBoxSettingCard(
            cfg.transcribe_model,
            FIF.MICROPHONE,
            self.tr("Transcription Model"),
            self.tr("Speech-to-text recognition model to use"),
            texts=[model.value for model in cfg.transcribe_model.validator.options],  # type: ignore
            parent=self.transcribeGroup,
        )

        # LLM配置卡片
        self.__createLLMServiceCards()

        # 翻译配置卡片
        self.__createTranslateServiceCards()

        # Translation & optimization cards
        self.subtitleCorrectCard = SwitchSettingCard(
            FIF.EDIT,
            self.tr("Subtitle Correction"),
            self.tr("Whether to correct subtitles during processing"),
            cfg.need_optimize,
            self.translateGroup,
        )
        self.subtitleTranslateCard = SwitchSettingCard(
            FIF.LANGUAGE,
            self.tr("Subtitle Translation"),
            self.tr("Whether to translate subtitles during processing"),
            cfg.need_translate,
            self.translateGroup,
        )
        self.targetLanguageCard = ComboBoxSettingCard(
            cfg.target_language,
            FIF.LANGUAGE,
            self.tr("Target Language"),
            self.tr("Choose target language for translation"),
            texts=[lang.value for lang in cfg.target_language.validator.options],  # type: ignore
            parent=self.translateGroup,
        )

        # Subtitle synthesis cards
        self.subtitleStyleCard = HyperlinkCard(
            "",
            self.tr("Edit"),
            FIF.FONT,
            self.tr("Subtitle Style"),
            self.tr("Choose subtitle style (color, size, font, etc.)"),
            self.subtitleGroup,
        )
        self.subtitleLayoutCard = HyperlinkCard(
            "",
            self.tr("Edit"),
            FIF.FONT,
            self.tr("Subtitle Layout"),
            self.tr("Choose subtitle layout (monolingual, bilingual)"),
            self.subtitleGroup,
        )
        self.needVideoCard = SwitchSettingCard(
            FIF.VIDEO,
            self.tr("Generate Video"),
            self.tr("Enable to synthesize video; disable to skip"),
            cfg.need_video,
            self.subtitleGroup,
        )
        self.softSubtitleCard = SwitchSettingCard(
            FIF.FONT,
            self.tr("Soft Subtitles"),
            self.tr("When enabled, subtitles can be toggled/adjusted in the player; when disabled, subtitles are burned into the video"),
            cfg.soft_subtitle,
            self.subtitleGroup,
        )

        # Save settings cards
        self.savePathCard = PushSettingCard(
            self.tr("Working Folder"),
            FIF.SAVE,
            self.tr("Working Directory Path"),
            cfg.get(cfg.work_dir),
            self.saveGroup,
        )

        # Personalization cards
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr("App Theme"),
            self.tr("Change application appearance"),
            texts=[self.tr("Light"), self.tr("Dark"), self.tr("Use System Settings")],
            parent=self.personalGroup,
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr("Theme Color"),
            self.tr("Change application theme color"),
            self.personalGroup,
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface Scaling"),
            self.tr("Change size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%", self.tr("Use System Settings")],
            parent=self.personalGroup,
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr("Language"),
            self.tr("Set your preferred interface language"),
            texts=["Simplified Chinese", "Traditional Chinese", "English", self.tr("Use System Settings")],
            parent=self.personalGroup,
        )

        # About cards
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr("Open Help Page"),
            FIF.HELP,
            self.tr("Help"),
            self.tr("Discover new features and tips for using VideoCaptioner"),
            self.aboutGroup,
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr("Provide Feedback"),
            FIF.FEEDBACK,
            self.tr("Provide Feedback"),
            self.tr("Provide feedback to help us improve VideoCaptioner"),
            self.aboutGroup,
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr("Check for Updates"),
            FIF.INFO,
            self.tr("About"),
            "© "
            + self.tr("All Rights Reserved")
            + f" {YEAR}, {AUTHOR}. "
            + self.tr("Version")
            + " "
            + VERSION,
            self.aboutGroup,
        )

        # 添加卡片到对应的组
        self.translateGroup.addSettingCard(self.subtitleCorrectCard)
        self.translateGroup.addSettingCard(self.subtitleTranslateCard)
        self.translateGroup.addSettingCard(self.targetLanguageCard)

        self.subtitleGroup.addSettingCard(self.subtitleStyleCard)
        self.subtitleGroup.addSettingCard(self.subtitleLayoutCard)
        self.subtitleGroup.addSettingCard(self.needVideoCard)
        self.subtitleGroup.addSettingCard(self.softSubtitleCard)

        self.saveGroup.addSettingCard(self.savePathCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.personalGroup.addSettingCard(self.languageCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

    def __createLLMServiceCards(self):
        """Create configuration cards for LLM services"""
        # Service selection card
        self.llmServiceCard = ComboBoxSettingCard(
            cfg.llm_service,
            FIF.ROBOT,
            self.tr("LLM Service"),
            self.tr("Choose LLM service for subtitle segmentation, optimization, and translation"),
            texts=[service.value for service in cfg.llm_service.validator.options],  # type: ignore
            parent=self.llmGroup,
        )

        # Create OPENAI official API link card
        self.openaiOfficialApiCard = HyperlinkCard(
            "https://api.videocaptioner.cn/register?aff=UrLB",
            self.tr("Visit"),
            FIF.DEVELOPER_TOOLS,
            self.tr("VideoCaptioner Official API"),
            self.tr("Integrates multiple LLMs; supports high-concurrency subtitle optimization and translation"),
            self.llmGroup,
        )
        # 默认隐藏
        self.openaiOfficialApiCard.setVisible(False)

        # 定义每个服务的配置
        service_configs = {
            LLMServiceEnum.OPENAI: {
                "prefix": "openai",
                "api_key_cfg": cfg.openai_api_key,
                "api_base_cfg": cfg.openai_api_base,
                "model_cfg": cfg.openai_model,
                "default_base": "https://api.openai.com/v1",
                "default_models": [
                    "gpt-4o-mini",
                    "gpt-4o",
                    "claude-3-5-sonnet-20241022",
                ],
            },
            LLMServiceEnum.SILICON_CLOUD: {
                "prefix": "silicon_cloud",
                "api_key_cfg": cfg.silicon_cloud_api_key,
                "api_base_cfg": cfg.silicon_cloud_api_base,
                "model_cfg": cfg.silicon_cloud_model,
                "default_base": "https://api.siliconflow.cn/v1",
                "default_models": ["deepseek-ai/DeepSeek-V3"],
            },
            LLMServiceEnum.DEEPSEEK: {
                "prefix": "deepseek",
                "api_key_cfg": cfg.deepseek_api_key,
                "api_base_cfg": cfg.deepseek_api_base,
                "model_cfg": cfg.deepseek_model,
                "default_base": "https://api.deepseek.com/v1",
                "default_models": ["deepseek-chat"],
            },
            LLMServiceEnum.OLLAMA: {
                "prefix": "ollama",
                "api_key_cfg": cfg.ollama_api_key,
                "api_base_cfg": cfg.ollama_api_base,
                "model_cfg": cfg.ollama_model,
                "default_base": "http://localhost:11434/v1",
                "default_models": ["qwen2.5:7b"],
            },
            LLMServiceEnum.LM_STUDIO: {
                "prefix": "LM Studio",
                "api_key_cfg": cfg.lm_studio_api_key,
                "api_base_cfg": cfg.lm_studio_api_base,
                "model_cfg": cfg.lm_studio_model,
                "default_base": "http://localhost:1234/v1",
                "default_models": ["qwen2.5:7b"],
            },
            LLMServiceEnum.GEMINI: {
                "prefix": "gemini",
                "api_key_cfg": cfg.gemini_api_key,
                "api_base_cfg": cfg.gemini_api_base,
                "model_cfg": cfg.gemini_model,
                "default_base": "https://generativelanguage.googleapis.com/v1beta/openai/",
                "default_models": ["gemini-2.0-flash-exp"],
            },
            LLMServiceEnum.CHATGLM: {
                "prefix": "chatglm",
                "api_key_cfg": cfg.chatglm_api_key,
                "api_base_cfg": cfg.chatglm_api_base,
                "model_cfg": cfg.chatglm_model,
                "default_base": "https://open.bigmodel.cn/api/paas/v4",
                "default_models": ["glm-4-flash"],
            },
            LLMServiceEnum.PUBLIC: {
                "prefix": "public",
                "api_key_cfg": cfg.public_api_key,
                "api_base_cfg": cfg.public_api_base,
                "model_cfg": cfg.public_model,
                "default_base": "https://api.public-model.com/v1",
                "default_models": ["public-model"],
            },
        }

        # 创建服务配置映射
        self.llm_service_configs = {}

        # 为每个服务创建配置卡片
        for service, config in service_configs.items():
            prefix = config["prefix"]

            # 如果是公益模型，只添加配置不创建卡片
            if service == LLMServiceEnum.PUBLIC:
                self.llm_service_configs[service] = {
                    "cards": [],
                    "api_base": None,
                    "api_key": None,
                    "model": None,
                }
                continue

            # Create API Key card
            api_key_card = LineEditSettingCard(
                config["api_key_cfg"],
                FIF.FINGERPRINT,
                self.tr("API Key"),
                self.tr(f"Enter your {service.value} API Key"),
                "sk-" if service != LLMServiceEnum.OLLAMA else "",
                self.llmGroup,
            )
            setattr(self, f"{prefix}_api_key_card", api_key_card)

            # Create Base URL card
            api_base_card = LineEditSettingCard(
                config["api_base_cfg"],
                FIF.LINK,
                self.tr("Base URL"),
                self.tr(f"Enter {service.value} Base URL, must contain /v1"),
                config["default_base"],
                self.llmGroup,
            )
            setattr(self, f"{prefix}_api_base_card", api_base_card)

            # Create model selection card
            model_card = EditComboBoxSettingCard(
                config["model_cfg"],
                FIF.ROBOT,  # type: ignore
                self.tr("Model"),
                self.tr(f"Select {service.value} model"),
                config["default_models"],
                self.llmGroup,
            )
            setattr(self, f"{prefix}_model_card", model_card)

            # 存储服务配置
            cards = [api_key_card, api_base_card, model_card]

            self.llm_service_configs[service] = {
                "cards": cards,
                "api_base": api_base_card,
                "api_key": api_key_card,
                "model": model_card,
            }

        # Create check connection card
        self.checkLLMConnectionCard = PushSettingCard(
            self.tr("Check Connection"),
            FIF.LINK,
            self.tr("Check LLM Connection"),
            self.tr("Check API connectivity and fetch model list"),
            self.llmGroup,
        )

        # 初始化显示状态
        self.__onLLMServiceChanged(self.llmServiceCard.comboBox.currentText())

    def __createTranslateServiceCards(self):
        """Create configuration cards for translation services"""
        # Translation service selection card
        self.translatorServiceCard = ComboBoxSettingCard(
            cfg.translator_service,
            FIF.ROBOT,
            self.tr("Translation Service"),
            self.tr("Select translation service"),
            texts=[
                service.value
                for service in cfg.translator_service.validator.options  # type: ignore
            ],
            parent=self.translate_serviceGroup,
        )

        # Reflective translation switch
        self.needReflectTranslateCard = SwitchSettingCard(
            FIF.EDIT,
            self.tr("Enable Reflective Translation"),
            self.tr("Improves translation quality but uses more time and tokens"),
            cfg.need_reflect_translate,
            self.translate_serviceGroup,
        )

        # DeepLx backend configuration
        self.deeplxEndpointCard = LineEditSettingCard(
            cfg.deeplx_endpoint,
            FIF.LINK,
            self.tr("DeepLx Backend"),
            self.tr("Enter DeepLx backend URL (required when DeepLx is enabled)"),
            "https://api.deeplx.org/translate",
            self.translate_serviceGroup,
        )

        # Batch size configuration
        self.batchSizeCard = RangeSettingCard(
            cfg.batch_size,
            FIF.ALIGNMENT,
            self.tr("Batch Size"),
            self.tr("Number of subtitles per batch; multiple of 10 recommended"),
            parent=self.translate_serviceGroup,
        )

        # Thread count configuration
        self.threadNumCard = RangeSettingCard(
            cfg.thread_num,
            FIF.SPEED_HIGH,
            self.tr("Thread Count"),
            self.tr(
                "Number of parallel requests; increase when allowed by provider for higher speed"
            ),
            parent=self.translate_serviceGroup,
        )

        # 添加卡片到翻译服务组
        self.translate_serviceGroup.addSettingCard(self.translatorServiceCard)
        self.translate_serviceGroup.addSettingCard(self.needReflectTranslateCard)
        self.translate_serviceGroup.addSettingCard(self.deeplxEndpointCard)
        self.translate_serviceGroup.addSettingCard(self.batchSizeCard)
        self.translate_serviceGroup.addSettingCard(self.threadNumCard)

        # 初始化显示状态
        self.__onTranslatorServiceChanged(
            self.translatorServiceCard.comboBox.currentText()
        )

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # type: ignore
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # 初始化样式表
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")

        # 初始化翻译服务配置卡片的显示状态
        self.__onTranslatorServiceChanged(
            self.translatorServiceCard.comboBox.currentText()
        )

        self.setStyleSheet(
            """        
            SettingInterface, #scrollWidget {
                background-color: transparent;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QLabel#settingLabel {
                font: 33px 'Microsoft YaHei';
                background-color: transparent;
                color: white;
            }
        """
        )

    def __initLayout(self):
        """初始化布局"""
        self.settingLabel.move(36, 30)

        # 添加转录配置卡片
        self.transcribeGroup.addSettingCard(self.transcribeModelCard)

        # 添加LLM配置卡片
        self.llmGroup.addSettingCard(self.llmServiceCard)
        # 添加OPENAI官方API链接卡片
        self.llmGroup.addSettingCard(self.openaiOfficialApiCard)
        for config in self.llm_service_configs.values():
            for card in config["cards"]:
                self.llmGroup.addSettingCard(card)
        self.llmGroup.addSettingCard(self.checkLLMConnectionCard)

        # 将所有组添加到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.transcribeGroup)
        self.expandLayout.addWidget(self.llmGroup)
        self.expandLayout.addWidget(self.translate_serviceGroup)
        self.expandLayout.addWidget(self.translateGroup)
        self.expandLayout.addWidget(self.subtitleGroup)
        self.expandLayout.addWidget(self.saveGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __connectSignalToSlot(self):
        """Connect signals and slots"""
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # LLM服务切换
        self.llmServiceCard.comboBox.currentTextChanged.connect(
            self.__onLLMServiceChanged
        )

        # 翻译服务切换
        self.translatorServiceCard.comboBox.currentTextChanged.connect(
            self.__onTranslatorServiceChanged
        )

        # 检查 LLM 连接
        self.checkLLMConnectionCard.clicked.connect(self.checkLLMConnection)

        # 保存路径
        self.savePathCard.clicked.connect(self.__onsavePathCardClicked)

        # 字幕样式修改跳转
        self.subtitleStyleCard.linkButton.clicked.connect(
            lambda: self.window().switchTo(self.window().subtitleStyleInterface)  # type: ignore
        )
        self.subtitleLayoutCard.linkButton.clicked.connect(
            lambda: self.window().switchTo(self.window().subtitleStyleInterface)  # type: ignore
        )

        # 个性化
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.themeColorCard.colorChanged.connect(setThemeColor)

        # 反馈
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL))  # type: ignore
        )

        # 关于
        self.aboutCard.clicked.connect(self.checkUpdate)

        # 全局 signalBus
        self.transcribeModelCard.comboBox.currentTextChanged.connect(
            signalBus.transcription_model_changed
        )
        self.subtitleCorrectCard.checkedChanged.connect(
            signalBus.subtitle_optimization_changed
        )
        self.subtitleTranslateCard.checkedChanged.connect(
            signalBus.subtitle_translation_changed
        )
        self.targetLanguageCard.comboBox.currentTextChanged.connect(
            signalBus.target_language_changed
        )
        self.softSubtitleCard.checkedChanged.connect(signalBus.soft_subtitle_changed)
        self.needVideoCard.checkedChanged.connect(signalBus.need_video_changed)

    def __showRestartTooltip(self):
        """Show restart tooltip"""
        InfoBar.success(
            self.tr("Updated Successfully"),
            self.tr("Settings will take effect after restart"),
            duration=1500,
            parent=self,
        )

    def __onsavePathCardClicked(self):
        """Handle save path card click"""
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select Folder"), "./")
        if not folder or cfg.get(cfg.work_dir) == folder:
            return
        cfg.set(cfg.work_dir, folder)
        self.savePathCard.setContent(folder)

    def checkLLMConnection(self):
        """Check LLM connection"""
        # 获取当前选中的服务
        current_service = LLMServiceEnum(self.llmServiceCard.comboBox.currentText())

        # 获取服务配置
        service_config = self.llm_service_configs.get(current_service)
        if not service_config:
            return

        # 如果是公益模型，使用配置文件中的值
        if current_service == LLMServiceEnum.PUBLIC:
            api_base = cfg.public_api_base.value
            api_key = cfg.public_api_key.value
            model = cfg.public_model.value
        else:
            api_base = (
                service_config["api_base"].lineEdit.text()
                if service_config["api_base"]
                else ""
            )
            api_key = (
                service_config["api_key"].lineEdit.text()
                if service_config["api_key"]
                else ""
            )
            model = (
                service_config["model"].comboBox.currentText()
                if service_config["model"]
                else ""
            )

        # Check if API Base is a valid URL
        if not api_base.startswith("http"):
            InfoBar.error(
                self.tr("Error"),
                self.tr("Please enter a valid API Base including /v1"),
                duration=3000,
                parent=self,
            )
            return

        # Disable check button and show loading state
        self.checkLLMConnectionCard.button.setEnabled(False)
        self.checkLLMConnectionCard.button.setText(self.tr("Checking..."))

        # 创建并启动线程
        self.connection_thread = LLMConnectionThread(api_base, api_key, model)
        self.connection_thread.finished.connect(self.onConnectionCheckFinished)
        self.connection_thread.error.connect(self.onConnectionCheckError)
        self.connection_thread.start()

    def onConnectionCheckError(self, message):
        """Handle connection check error"""
        self.checkLLMConnectionCard.button.setEnabled(True)
        self.checkLLMConnectionCard.button.setText(self.tr("Check Connection"))
        InfoBar.error(self.tr("LLM connection test error"), message, duration=3000, parent=self)

    def onConnectionCheckFinished(self, is_success, message, models):
        """Handle connection check finished"""
        self.checkLLMConnectionCard.button.setEnabled(True)
        self.checkLLMConnectionCard.button.setText(self.tr("Check Connection"))

        # 获取当前服务
        current_service = LLMServiceEnum(self.llmServiceCard.comboBox.currentText())

        if models:
            # 更新当前服务的模型列表
            service_config = self.llm_service_configs.get(current_service)
            if service_config and service_config["model"]:
                temp = service_config["model"].comboBox.currentText()
                service_config["model"].setItems(models)
                service_config["model"].comboBox.setCurrentText(temp)

            InfoBar.success(
                self.tr("Fetched model list successfully:"),
                self.tr("Total ") + str(len(models)) + self.tr(" models"),
                duration=3000,
                parent=self,
            )
        if not is_success:
            InfoBar.error(
                self.tr("LLM connection test error"), message, duration=3000, parent=self
            )
        else:
            InfoBar.success(
                self.tr("LLM connection test successful"), message, duration=3000, parent=self
            )

    def checkUpdate(self):
        webbrowser.open(RELEASE_URL)

    def __onLLMServiceChanged(self, service):
        """处理LLM服务切换事件"""
        current_service = LLMServiceEnum(service)

        # 隐藏所有卡片
        for config in self.llm_service_configs.values():
            for card in config["cards"]:
                card.setVisible(False)

        # 隐藏OPENAI官方API链接卡片
        self.openaiOfficialApiCard.setVisible(False)

        # 显示选中服务的卡片
        if current_service in self.llm_service_configs:
            for card in self.llm_service_configs[current_service]["cards"]:
                card.setVisible(True)

            # 为OLLAMA和LM_STUDIO设置默认API Key
            service_config = self.llm_service_configs[current_service]
            if current_service == LLMServiceEnum.OLLAMA and service_config["api_key"]:
                # 如果API Key为空，设置默认值"ollama"
                if not service_config["api_key"].lineEdit.text():
                    service_config["api_key"].lineEdit.setText("ollama")
            if (
                current_service == LLMServiceEnum.LM_STUDIO
                and service_config["api_key"]
            ):
                # 如果API Key为空，设置默认值 "lm-studio"
                if not service_config["api_key"].lineEdit.text():
                    service_config["api_key"].lineEdit.setText("lm-studio")

            # 如果是OPENAI服务，显示官方API链接卡片
            if current_service == LLMServiceEnum.OPENAI:
                self.openaiOfficialApiCard.setVisible(True)

        # 更新布局
        self.llmGroup.adjustSize()
        self.expandLayout.update()

    def __onTranslatorServiceChanged(self, service):
        openai_cards = [
            self.needReflectTranslateCard,
            self.batchSizeCard,
        ]
        deeplx_cards = [self.deeplxEndpointCard]

        all_cards = openai_cards + deeplx_cards
        for card in all_cards:
            card.setVisible(False)

        # 根据选择的服务显示相应的配置卡片
        if service in [TranslatorServiceEnum.DEEPLX.value]:
            for card in deeplx_cards:
                card.setVisible(True)
        elif service in [TranslatorServiceEnum.OPENAI.value]:
            for card in openai_cards:
                card.setVisible(True)

        # 更新布局
        self.translate_serviceGroup.adjustSize()
        self.expandLayout.update()


class LLMConnectionThread(QThread):
    finished = pyqtSignal(bool, str, list)
    error = pyqtSignal(str)

    def __init__(self, api_base, api_key, model):
        super().__init__()
        self.api_base = api_base
        self.api_key = api_key
        self.model = model

    def run(self):
        """检查 LLM 连接并获取模型列表"""
        try:
            is_success, message = test_openai(self.api_base, self.api_key, self.model)
            models = get_openai_models(self.api_base, self.api_key)
            self.finished.emit(is_success, message, models)
        except Exception as e:
            self.error.emit(str(e))
