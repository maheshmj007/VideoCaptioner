# coding:utf-8
from enum import Enum

from PyQt5.QtCore import QLocale
from PyQt5.QtGui import QColor
from qfluentwidgets import (
    BoolValidator,
    ConfigItem,
    ConfigSerializer,
    EnumSerializer,
    FolderValidator,
    OptionsConfigItem,
    OptionsValidator,
    QConfig,
    RangeConfigItem,
    RangeValidator,
    Theme,
    qconfig,
)

from app.config import SETTINGS_PATH, WORK_PATH

from ..core.entities import (
    FasterWhisperModelEnum,
    LLMServiceEnum,
    SplitTypeEnum,
    TargetLanguageEnum,
    TranscribeLanguageEnum,
    TranscribeModelEnum,
    TranslatorServiceEnum,
    VadMethodEnum,
    WhisperModelEnum,
)


class Language(Enum):
    """Software language"""

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class SubtitleLayoutEnum(Enum):
    """Subtitle layout"""

    TRANSLATE_ON_TOP = "Translation on top"
    ORIGINAL_ON_TOP = "Original on top"
    ONLY_ORIGINAL = "Original only"
    ONLY_TRANSLATE = "Translation only"


class LanguageSerializer(ConfigSerializer):
    """Language serializer"""

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """Application configuration"""

    # LLM configuration
    llm_service = OptionsConfigItem(
        "LLM",
        "LLMService",
        LLMServiceEnum.PUBLIC,
        OptionsValidator(LLMServiceEnum),
        EnumSerializer(LLMServiceEnum),
    )

    openai_model = ConfigItem("LLM", "OpenAI_Model", "gpt-4o-mini")
    openai_api_key = ConfigItem("LLM", "OpenAI_API_Key", "")
    openai_api_base = ConfigItem("LLM", "OpenAI_API_Base", "https://api.openai.com/v1")

    silicon_cloud_model = ConfigItem("LLM", "SiliconCloud_Model", "gpt-4o-mini")
    silicon_cloud_api_key = ConfigItem("LLM", "SiliconCloud_API_Key", "")
    silicon_cloud_api_base = ConfigItem(
        "LLM", "SiliconCloud_API_Base", "https://api.siliconflow.cn/v1"
    )

    deepseek_model = ConfigItem("LLM", "DeepSeek_Model", "deepseek-chat")
    deepseek_api_key = ConfigItem("LLM", "DeepSeek_API_Key", "")
    deepseek_api_base = ConfigItem(
        "LLM", "DeepSeek_API_Base", "https://api.deepseek.com/v1"
    )

    ollama_model = ConfigItem("LLM", "Ollama_Model", "llama2")
    ollama_api_key = ConfigItem("LLM", "Ollama_API_Key", "ollama")
    ollama_api_base = ConfigItem("LLM", "Ollama_API_Base", "http://localhost:11434/v1")

    lm_studio_model = ConfigItem("LLM", "LmStudio_Model", "qwen2.5:7b")
    lm_studio_api_key = ConfigItem("LLM", "LmStudio_API_Key", "lmstudio")
    lm_studio_api_base = ConfigItem(
        "LLM", "LmStudio_API_Base", "http://localhost:1234/v1"
    )

    gemini_model = ConfigItem("LLM", "Gemini_Model", "gemini-pro")
    gemini_api_key = ConfigItem("LLM", "Gemini_API_Key", "")
    gemini_api_base = ConfigItem(
        "LLM",
        "Gemini_API_Base",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    chatglm_model = ConfigItem("LLM", "ChatGLM_Model", "glm-4")
    chatglm_api_key = ConfigItem("LLM", "ChatGLM_API_Key", "")
    chatglm_api_base = ConfigItem(
        "LLM", "ChatGLM_API_Base", "https://open.bigmodel.cn/api/paas/v4"
    )

    # Public model
    public_model = ConfigItem("LLM", "Public_Model", "gpt-4o-mini")
    public_api_key = ConfigItem(
        "LLM", "Public_API_Key", "please-do-not-use-for-personal-purposes"
    )
    public_api_base = ConfigItem("LLM", "Public_API_Base", "https://ddg.bkfeng.top/v1")

    # ------------------- Translation configuration -------------------
    translator_service = OptionsConfigItem(
        "Translate",
        "TranslatorServiceEnum",
        TranslatorServiceEnum.BING,
        OptionsValidator(TranslatorServiceEnum),
        EnumSerializer(TranslatorServiceEnum),
    )
    need_reflect_translate = ConfigItem(
        "Translate", "NeedReflectTranslate", False, BoolValidator()
    )
    deeplx_endpoint = ConfigItem("Translate", "DeeplxEndpoint", "")
    batch_size = RangeConfigItem("Translate", "BatchSize", 10, RangeValidator(5, 30))
    thread_num = RangeConfigItem("Translate", "ThreadNum", 10, RangeValidator(1, 100))

    # ------------------- Transcription configuration -------------------
    transcribe_model = OptionsConfigItem(
        "Transcribe",
        "TranscribeModel",
        TranscribeModelEnum.BIJIAN,
        OptionsValidator(TranscribeModelEnum),
        EnumSerializer(TranscribeModelEnum),
    )
    use_asr_cache = ConfigItem("Transcribe", "UseASRCache", True, BoolValidator())
    transcribe_language = OptionsConfigItem(
        "Transcribe",
        "TranscribeLanguage",
        TranscribeLanguageEnum.ENGLISH,
        OptionsValidator(TranscribeLanguageEnum),
        EnumSerializer(TranscribeLanguageEnum),
    )

    # ------------------- Whisper Cpp configuration -------------------
    whisper_model = OptionsConfigItem(
        "Whisper",
        "WhisperModel",
        WhisperModelEnum.TINY,
        OptionsValidator(WhisperModelEnum),
        EnumSerializer(WhisperModelEnum),
    )

    # ------------------- Faster Whisper configuration -------------------
    faster_whisper_program = ConfigItem(
        "FasterWhisper",
        "Program",
        "faster-whisper-xxl.exe",
    )
    faster_whisper_model = OptionsConfigItem(
        "FasterWhisper",
        "Model",
        FasterWhisperModelEnum.TINY,
        OptionsValidator(FasterWhisperModelEnum),
        EnumSerializer(FasterWhisperModelEnum),
    )
    faster_whisper_model_dir = ConfigItem("FasterWhisper", "ModelDir", "")
    faster_whisper_device = OptionsConfigItem(
        "FasterWhisper", "Device", "cuda", OptionsValidator(["cuda", "cpu"])
    )
    # VAD parameters
    faster_whisper_vad_filter = ConfigItem(
        "FasterWhisper", "VadFilter", True, BoolValidator()
    )
    faster_whisper_vad_threshold = RangeConfigItem(
        "FasterWhisper", "VadThreshold", 0.4, RangeValidator(0, 1)
    )
    faster_whisper_vad_method = OptionsConfigItem(
        "FasterWhisper",
        "VadMethod",
        VadMethodEnum.SILERO_V4,
        OptionsValidator(VadMethodEnum),
        EnumSerializer(VadMethodEnum),
    )
    # Voice extraction
    faster_whisper_ff_mdx_kim2 = ConfigItem(
        "FasterWhisper", "FfMdxKim2", False, BoolValidator()
    )
    # Text processing parameters
    faster_whisper_one_word = ConfigItem(
        "FasterWhisper", "OneWord", True, BoolValidator()
    )
    # Prompt
    faster_whisper_prompt = ConfigItem("FasterWhisper", "Prompt", "")

    # ------------------- Whisper API configuration -------------------
    whisper_api_base = ConfigItem("WhisperAPI", "WhisperApiBase", "")
    whisper_api_key = ConfigItem("WhisperAPI", "WhisperApiKey", "")
    whisper_api_model = OptionsConfigItem("WhisperAPI", "WhisperApiModel", "")
    whisper_api_prompt = ConfigItem("WhisperAPI", "WhisperApiPrompt", "")

    # ------------------- Subtitle configuration -------------------
    need_optimize = ConfigItem("Subtitle", "NeedOptimize", False, BoolValidator())
    need_translate = ConfigItem("Subtitle", "NeedTranslate", False, BoolValidator())
    need_split = ConfigItem("Subtitle", "NeedSplit", False, BoolValidator())
    split_type = OptionsConfigItem(
        "Subtitle",
        "SplitType",
        SplitTypeEnum.SENTENCE,
        OptionsValidator(SplitTypeEnum),
        EnumSerializer(SplitTypeEnum),
    )
    target_language = OptionsConfigItem(
        "Subtitle",
        "TargetLanguage",
        TargetLanguageEnum.CHINESE_SIMPLIFIED,
        OptionsValidator(TargetLanguageEnum),
        EnumSerializer(TargetLanguageEnum),
    )
    max_word_count_cjk = ConfigItem(
        "Subtitle", "MaxWordCountCJK", 25, RangeValidator(8, 100)
    )
    max_word_count_english = ConfigItem(
        "Subtitle", "MaxWordCountEnglish", 20, RangeValidator(8, 100)
    )
    needs_remove_punctuation = ConfigItem(
        "Subtitle", "NeedsRemovePunctuation", True, BoolValidator()
    )
    custom_prompt_text = ConfigItem("Subtitle", "CustomPromptText", "")

    # ------------------- Subtitle synthesis configuration -------------------
    soft_subtitle = ConfigItem("Video", "SoftSubtitle", False, BoolValidator())
    need_video = ConfigItem("Video", "NeedVideo", True, BoolValidator())

    # ------------------- Subtitle style configuration -------------------
    subtitle_style_name = ConfigItem("SubtitleStyle", "StyleName", "default")
    subtitle_layout = ConfigItem("SubtitleStyle", "Layout", "Translation on top")
    subtitle_preview_image = ConfigItem("SubtitleStyle", "PreviewImage", "")

    # ------------------- Save configuration -------------------
    work_dir = ConfigItem("Save", "Work_Dir", WORK_PATH, FolderValidator())

    # ------------------- Software interface configuration -------------------
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", False, BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )
    language = OptionsConfigItem(
        "MainWindow",
        "Language",
        Language.AUTO,
        OptionsValidator(Language),
        LanguageSerializer(),
        restart=True,
    )

    # ------------------- Update configuration -------------------
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator()
    )


cfg = Config()
cfg.themeMode.value = Theme.DARK
cfg.themeColor.value = QColor("#ff28f08b")
qconfig.load(SETTINGS_PATH, cfg)
