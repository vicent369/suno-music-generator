# Suno API 音乐生成器

一个基于Flask的Web应用，用于调用Suno API生成音乐并在网页上播放。

## 功能特性

- 🎵 通过文本描述生成音乐
- 🎨 支持多种模型版本（V3.5、V4、V4.5）
- 🎼 支持纯音乐（无人声）生成
- 📱 响应式设计，支持移动端
- ⏳ 实时状态轮询
- 🎧 在线播放和下载功能

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env_example.txt` 为 `.env` 文件，并填入你的Suno API密钥：

```
SUNO_API_KEY=your_suno_api_key_here
```

### 3. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 使用方法

1. 在文本框中输入音乐描述
2. 选择模型版本
3. 选择是否生成纯音乐
4. 点击"生成音乐"按钮
5. 等待生成完成，即可在线播放或下载

## 项目结构

```
project/
├── app.py              # Flask主应用
├── requirements.txt     # Python依赖
├── env_example.txt     # 环境变量示例
├── README.md          # 项目说明
├── templates/
│   └── index.html     # 前端页面
└── generated_audios/   # 生成的音频文件目录
```

## API接口

### POST /api/generate
生成音乐任务

**请求参数：**
- `prompt` (必填): 音乐描述
- `model` (可选): 模型版本，默认V4
- `make_instrumental` (可选): 是否生成纯音乐
- `is_public` (可选): 是否公开作品

### GET /api/status/<task_id>
查询任务状态

**返回数据：**
- `status`: 任务状态
- `audio_url`: 音频文件URL
- `image_url`: 封面图片URL
- `video_url`: 视频文件URL

## 注意事项

1. 需要有效的Suno API密钥
2. 音乐生成可能需要几分钟时间
3. 建议在生产环境中使用HTTPS
4. 请遵守Suno API的使用条款

## 故障排除

### 常见问题

1. **API密钥错误**: 检查 `.env` 文件中的 `SUNO_API_KEY` 是否正确
2. **生成超时**: 音乐生成可能需要较长时间，请耐心等待
3. **网络错误**: 检查网络连接和API服务状态

### 日志查看

应用会在控制台输出详细的请求和响应日志，便于调试。 