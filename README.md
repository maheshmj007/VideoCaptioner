<div align="center">
  <img src="./docs/images/logo.png"alt="VideoCaptioner Logo" width="100">
  <p>Kaka Subtitle Assistant</p>
  <h1>VideoCaptioner</h1>
  <p>A video subtitle processing assistant based on Large Language Models (LLM), supporting speech recognition, subtitle segmentation, optimization, and translation in full workflow</p>

[简体中文](./README.md) / [正體中文](./docs/README_TW.md) / English / [日本語](./docs/README_JA.md)

</div>

## Project Introduction

Kaka Subtitle Assistant (VideoCaptioner) is simple to operate and requires no high-end configuration. It supports both online API calls and local offline processing (with GPU support) for speech recognition, utilizing Large Language Models for intelligent subtitle segmentation, correction, and translation. It provides one-click full workflow processing for subtitle videos, creating stunning subtitle effects.

The latest version supports practical features including VAD, voice separation, character-level timestamps, and batch subtitle processing.

- Use powerful speech recognition engines without GPU requirements to generate accurate subtitles
- LLM-based intelligent segmentation and sentence breaking for more natural and fluent subtitle reading
- AI subtitle multi-threaded optimization and translation, adjusting subtitle format for more authentic and professional expression
- Support for batch video subtitle synthesis to improve processing efficiency
- Intuitive subtitle editing and viewing interface with real-time preview and quick editing support
- Low model token consumption with built-in basic LLM models for out-of-the-box usage

## Interface Preview

<div align="center">
  <img src="https://github.com/maheshmj007/VideoCaptioner/blob/master/resource/assets/front_page_preview.png" alt="Software Interface Preview" width="90%" style="border-radius: 5px;">
</div>

![Page Preview](https://github.com/maheshmj007/VideoCaptioner/blob/master/resource/assets/preview_1_1.png)
![Page Preview](https://github.com/maheshmj007/VideoCaptioner/blob/master/resource/assets/preview_1_2.png)

## Testing

Full workflow processing of a 14-minute 1080P [Bilibili English TED video](https://www.bilibili.com/video/BV1jT411X7Dz), using local Whisper model for speech recognition and `gpt-4o-mini` model for optimization and translation to Chinese, with a total processing time of approximately **4 minutes**.

Based on background calculations, model optimization and translation costs less than ￥0.01 (calculated at OpenAI official pricing).

For specific test result images of subtitle and video synthesis effects, please refer to [TED Video Test](./docs/test.md)

## Quick Start

### Windows Users

#### Method 1: Using Packaged Program (Recommended)

The software is relatively lightweight with a package size of less than 60MB, integrating all necessary environments and ready to run after download.

1. Download the latest version executable from the [Release](https://github.com/WEIFENG2333/VideoCaptioner/releases) page. Or: [LanZou Download](https://wwwm.lanzoue.com/ii14G2pdsbej)

2. Open the installer to install

3. LLM API configuration (for subtitle segmentation and correction), you can use [this project's relay station](https://api.videocaptioner.cn)

4. Translation configuration, choose whether to enable translation and translation service (default uses Microsoft Translate with average quality, recommend using LLM translation)

5. Speech recognition configuration (default uses B interface, use local transcription for languages other than Chinese and English)

6. Drag video files to the software window for fully automatic processing

Tip: Each step supports individual processing and file drag-and-drop. For specific model selection and parameter configuration instructions, please see below.

### macOS / Linux Users

1. Clone the project and enter the directory

```bash
git clone https://github.com/WEIFENG2333/VideoCaptioner.git
cd VideoCaptioner
```

2. Run the startup script

```bash
chmod +x run.sh
./run.sh
```

The script will automatically:

- Detect Python environment
- Create virtual environment and install Python dependencies
- Detect system tools (ffmpeg, aria2)
- Start the application

**Note**: macOS users need to install Homebrew first, and may need to install Xcode command line tools on first run.

<details>
<summary>Manual Installation Steps</summary>
 

1. Install ffmpeg and Aria2 download tools

```bash
brew install ffmpeg
brew install aria2
brew install python@3.**
```

2. Clone the project

```bash
git clone https://github.com/WEIFENG2333/VideoCaptioner.git
cd VideoCaptioner
```

3. Install dependencies

```bash
python3.** -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the program

```bash
python main.py
```

</details>



## Basic Configuration

### 1. LLM API Configuration

LLM large models are used for subtitle segmentation, subtitle optimization, and subtitle translation (if LLM large model translation is selected).

| Configuration Item | Description                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| SiliconCloud   | [SiliconCloud Official](https://cloud.siliconflow.cn/i/onCHcaDx) Configuration method please refer to [Configuration Documentation](./docs/llm_config.md)<br>Low concurrency, recommend setting threads below 5. |
| DeepSeek       | [DeepSeek Official](https://platform.deepseek.com), recommend using `deepseek-v3` model,<br>Official website services seem unstable recently.                                 |
| Ollama Local     | [Ollama Official](https://ollama.com)                                                                                                                 |
| Built-in Public Model   | Built-in basic large language model (`gpt-4o-mini`) (Public service unstable, strongly recommend using your own model API)                                                                  |
| OpenAI Compatible Interface | If you have APIs from other service providers, you can directly fill them in the software. base_url and api_key                                                                                     |

Note: If the API service provider doesn't support high concurrency, please lower the "Thread Count" in software settings to avoid request errors.

---

If you want high concurrency, or want to use high-quality large models like OpenAI or Claude for subtitle correction and translation within the software.

You can use this project's ✨LLM API Relay Station✨: [https://api.videocaptioner.cn](https://api.videocaptioner.cn)

It supports high concurrency with extremely high cost-effectiveness and offers a wide selection of domestic and international models.

After registration and obtaining the key, configure as follows in settings:

BaseURL: `https://api.videocaptioner.cn/v1`

API-key: `Get from Personal Center - API Token page.`

💡 Model Selection Recommendations (High cost-effectiveness models I've carefully selected at each quality level):

- High Quality Choice: `claude-sonnet-4-20250514` (Cost Ratio: 3)

- Higher Quality Choice: `gpt-5-2025-08-07`, `gemini-2.5-pro` (Cost Ratio: 1.25)

- Medium Quality Choice: `gpt-5-mini`, `gemini-2.5-flash` (Cost Ratio: 0.3)

This site supports ultra-high concurrency, you can max out the thread count in the software~ Processing speed is very fast~

More detailed API configuration tutorial: [Relay Station Configuration](./docs/llm_config.md#中转站配置)

---

## 2. Translation Configuration

| Configuration Item         | Description                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| LLM Large Model Translation | 🌟 Best translation quality choice. Uses AI large models for translation, better understanding of context, more natural translation. Requires configuring LLM API in settings (such as OpenAI, DeepSeek, etc.) |
| DeepLx Translation    | Relatively reliable translation. Based on DeepL translation, requires configuring your own backend interface.                                                                       |
| Microsoft Translation       | Uses Microsoft's translation service, very fast speed                                                                                                |
| Google Translation       | Google's translation service, fast speed, but requires network environment that can access Google                                                                              |

Recommend using `LLM Large Model Translation` for the best translation quality.

### 3. Speech Recognition Interface Description

| Interface Name         | Supported Languages                                           | Running Mode | Description                                                                                                              |
| ---------------- | -------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| B Interface            | Chinese and English only                                   | Online     | Free, relatively fast speed                                                                                                    |
| J Interface            | Chinese and English only                                   | Online     | Free, relatively fast speed                                                                                                    |
| WhisperCpp       | Chinese, Japanese, Korean, English and 99 other languages, good foreign language effects   | Local     | (Actually unstable in use) Requires downloading transcription models<br>Chinese recommends medium and above models<br>English etc. can achieve good results with smaller models.              |
| fasterWhisper 👍 | Chinese, English and 99 other languages, excellent foreign language effects, more accurate timeline | Local     | （🌟Highly Recommended🌟）Requires downloading programs and transcription models<br>Supports CUDA, faster speed, accurate transcription.<br>Super accurate timestamp subtitles.<br>Recommend priority use |

### 4. Local Whisper Speech Recognition Models

Whisper versions include WhisperCpp and fasterWhisper (recommended), with the latter having better effects. Both require downloading models within the software.

| Model        | Disk Space | Memory Usage | Description                                |
| ----------- | -------- | -------- | ----------------------------------- |
| Tiny        | 75 MiB   | ~273 MB  | Transcription is average, only for testing              |
| Small       | 466 MiB  | ~852 MB  | English recognition effect is already good                |
| Medium      | 1.5 GiB  | ~2.1 GB  | Chinese recognition recommends using at least this version          |
| Large-v2 👍 | 2.9 GiB  | ~3.9 GB  | Good effect, recommend use if configuration allows        |
| Large-v3    | 2.9 GiB  | ~3.9 GB  | Community feedback may have hallucination/subtitle duplication issues |

Recommended model: `Large-v2` is stable with good quality.

Note: The above models can be downloaded directly within the software on domestic networks.

### 5. Manuscript Matching

- In the "Subtitle Optimization and Translation" page, includes "Manuscript Matching" option, supporting the following **one or more** content types to assist subtitle correction and translation:

| Type       | Description                                 | Example                                                                                                                                                |
| ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Glossary     | Professional terms, names, specific word correction reference table | Machine Learning->Machine Learning<br>Musk->Elon Musk<br>打call -> 应援<br>图灵斑图<br>公交车悖论                                                             |
| Original Manuscript | Original manuscript or related content of the video             | Complete speech drafts, course handouts, etc.                                                                                                                                |
| Correction Requirements   | Specific correction requirements related to content               | Unify personal pronouns, standardize professional terms, etc.<br>Fill in **content-related** requirements, [Example Reference](https://github.com/WEIFENG2333/VideoCaptioner/issues/59#issuecomment-2495849752) |

- If manuscript assistance is needed for subtitle optimization, fill in manuscript information first during full workflow processing, then start task processing
- Note: When using small LLM models with low context parameters, recommend controlling manuscript content within 1000 characters. If using models with larger context, manuscript content can be appropriately increased.

No special requirements, generally not filled.

### 6. Cookie Configuration

When using URL download functionality, if you encounter the following situations:

1. Video websites require login information to download;
2. Can only download lower resolution videos;
3. Verification required when network conditions are poor;

- Please refer to [Cookie Configuration Instructions](./docs/get_cookies.md) to obtain Cookie information, and place the cookies.txt file in the `AppData` directory of the software installation directory to download high-quality videos normally.

## Software Workflow Introduction

The simple processing workflow of the program is as follows:

```
Speech Recognition Transcription -> Subtitle Segmentation (Optional) -> Subtitle Optimization Translation (Optional) -> Subtitle Video Synthesis
```

## Main Software Features

The software leverages the advantages of Large Language Models (LLM) in understanding context to further process subtitles generated from speech recognition. Effectively corrects typos and unifies professional terminology, making subtitle content more accurate and coherent, bringing users an excellent viewing experience!

#### 1. Multi-platform Video Download and Processing

- Supports mainstream video platforms at home and abroad (Bilibili, YouTube, Xiaohongshu, TikTok, X, Xigua Video, Douyin, etc.)
- Automatically extracts and processes original video subtitles

#### 2. Professional Speech Recognition Engine

- Provides multiple interface online recognition with effects comparable to Jianying (free, high-speed)
- Supports local Whisper models (privacy protection, offline capable)

#### 3. Intelligent Subtitle Error Correction

- Automatically optimizes professional terminology, code snippets and mathematical formula formats
- Context-based sentence segmentation optimization to improve reading experience
- Supports manuscript prompts, using original manuscripts or related prompts to optimize subtitle segmentation

#### 4. High-quality Subtitle Translation

- Context-aware intelligent translation ensuring translations consider the entire text
- Uses Prompt guidance for large model reflection translation to improve translation quality
- Uses sequence fuzzy matching algorithm to ensure complete timeline consistency

#### 5. Subtitle Style Adjustment

- Rich subtitle style templates (science popularization style, news style, anime style, etc.)
- Multiple format subtitle videos (SRT, ASS, VTT, TXT)

For novice users, explanations of some software options:

#### 1. Speech Transcription Page

- `VAD Filter`: When enabled, VAD (Voice Activity Detection) will filter voice segments without human voice, thereby reducing hallucination phenomena. Recommend keeping default enabled state. If unsure, other VAD options recommend keeping defaults.

- `Audio Separation`: When enabled, uses MDX-Net for noise reduction processing, effectively separating human voice and background music, thereby improving audio quality. Recommend only enabling in noisy videos.

#### 2. Subtitle Optimization and Translation Page

- `Intelligent Segmentation`: When enabled, generates character-level timestamps during full workflow processing, then uses LLM large models for segmentation, providing a more perfect viewing experience in videos. Has two modes: sentence-based segmentation and semantic-based segmentation. Configure according to your needs.

- `Subtitle Correction`: When enabled, uses LLM large models to correct subtitle content (such as: English word capitalization, punctuation, typos, mathematical formulas and code formatting, etc.), improving subtitle quality.

- `Reflection Translation`: When enabled, uses LLM large models for reflection translation, improving translation quality. Correspondingly increases request time and token consumption. (Option enabled in Settings Page - LLM Large Model Translation - Reflection Translation.)

- `Manuscript Prompt`: When filled, this part will also be sent as prompts to large models to assist subtitle optimization and translation.

#### 3. Subtitle Video Synthesis Page

- `Video Synthesis`: When enabled, synthesizes subtitle videos; disabling skips the video synthesis process.

- `Soft Subtitles`: When enabled, subtitles won't be burned into the video, processing speed is extremely fast. However, soft subtitles require some players (like PotPlayer) support to display and play. Also, soft subtitle styles are not the software-adjusted subtitle styles, but the player's default white style.

Main project directory structure description:

```
VideoCaptioner/
├── runtime/                    # Runtime environment directory
├── resources/                  # Software resource file directory (binary programs, icons, etc., and downloaded faster-whisper programs)
├── work-dir/                   # Working directory, processed videos and subtitle files are saved here
├── AppData/                    # Application data directory
    ├── cache/                  # Cache directory, caches transcription and large model request data.
    ├── models/                 # Stores Whisper model files
    ├── logs/                   # Log directory, records software running status
    ├── settings.json           # Stores user settings
    └──  cookies.txt            # Video platform cookie information (required for downloading high-definition videos)
└── VideoCaptioner.exe          # Main program executable file
```

## 📝 Notes

1. The quality of subtitle segmentation is crucial to the viewing experience. The software can intelligently reorganize character-by-character subtitles into paragraphs that conform to natural language habits and perfectly synchronize with video frames.

2. During processing, only text content is sent to large language models, without timeline information, which greatly reduces processing overhead.

3. In the translation process, we adopt Andrew Ng's "translate-reflect-translate" methodology. This iterative optimization approach ensures translation accuracy.

4. When processing YouTube links, video subtitles are automatically downloaded, saving transcription steps and greatly reducing operation time.

## 🤝 Contributing

The project is continuously improving. If you encounter bugs during use, please submit [Issues](https://github.com/WEIFENG2333/VideoCaptioner/issues) and Pull Requests to help improve the project.

## 📝 Changelog

To view the complete update history, please visit [CHANGELOG.md](./CHANGELOG.md)

## 💖 Support Author

If you find the project helpful, please give it a Star!

<details>
<summary>Donation Support</summary>
<div align="center">
  <img src="./docs/images/alipay.jpg" alt="Alipay QR Code" width="30%">
  <img src="./docs/images/wechat.jpg" alt="WeChat QR Code" width="30%">
</div>
</details>

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WEIFENG2333/VideoCaptioner&type=Date)](https://star-history.com/#WEIFENG2333/VideoCaptioner&Date)
