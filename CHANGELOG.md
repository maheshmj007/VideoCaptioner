# Changelog

## 2025.02.07

### Bug fixes and other improvements

- Fixed incorrect language issue with Google Translate
- Fixed inaccurate Microsoft Translate issue
- Fixed WinError display issue when CUDA device is not selected
- Fixed synthesis failure issue
- Fixed ASS monolingual subtitle content missing issue

## 2024.2.06

### Core functionality enhancements

- Complete code architecture refactoring with overall performance optimization
- Separated subtitle optimization and translation functionality modules for more flexible processing options
- Added batch processing functionality: supports batch subtitles, batch transcription, batch subtitle video synthesis
- Comprehensive UI interface and interaction detail optimization

### AI model and translation upgrades

- Extended LLM support: added SiliconCloud, DeepSeek, Ollama, Gemini, ChatGLM and other models
- Integrated multiple translation services: DeepLx, Bing, Google, LLM
- Added faster-whisper-large-v3-turbo model support
- Added multiple VAD (Voice Activity Detection) methods
- Support for custom reflection translation toggle
- Subtitle segmentation supports semantic/sentence modes
- Optimization of subtitle segmentation, optimization, and translation prompts
- Optimization of subtitle and transcription caching mechanisms
- Optimized Chinese subtitle auto-wrapping functionality
- Added vertical screen subtitle styles
- Improved subtitle timeline switching mechanism to eliminate flickering issues

### Bug fixes and other improvements

- Fixed Whisper API usage issue
- Added support for multiple subtitle video formats
- Fixed transcription error issues in some cases
- Optimized video working directory structure
- Added log viewing functionality
- Added subtitle optimization for Thai, German and other languages
- Fixed numerous bugs...

## 2024.12.07

- Added Faster-whisper support for better audio-to-subtitle quality
- Support for VAD voice breakpoint detection, greatly reducing hallucination phenomena
- Support for voice separation, separating video background noise
- Support for disabling video synthesis
- Added subtitle maximum length setting
- Added subtitle ending punctuation removal setting
- Optimized prompts for optimization and translation
- Optimized LLM subtitle segmentation error situations
- Fixed audio conversion format inconsistency issue

## 2024.11.23

- Added Whisper-v3 model support, significantly improving speech recognition accuracy
- Optimized subtitle segmentation algorithm for a more natural reading experience
- 修复检测模型可用性时的稳定性问题

## 2024.11.20

- 支持自定义调节字幕位置和样式
- 新增字幕优化和翻译过程的实时日志查看
- 修复使用 API 时的自动翻译问题
- 优化视频工作目录结构,提升文件管理效率

## 2024.11.17

- 支持双语/单语字幕灵活导出
- 新增文稿匹配提示对齐功能
- 修复字幕导入时的稳定性问题
- 修复非中文路径下载模型的兼容性问题

## 2024.11.13

- 新增 Whisper API 调用支持
- 支持导入 cookie.txt 下载各大视频平台资源
- 字幕文件名自动与视频保持一致
- 软件主页新增运行日志实时查看
- 统一和完善软件内部功能
