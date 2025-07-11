# 🚀 Vercel + Flask 部署指南

## 步骤一：准备代码

### 1. 确保文件结构正确
```
project/
├── app.py              # Flask主应用
├── api/
│   └── index.py        # Vercel API入口
├── templates/
│   └── index.html      # 前端页面
├── requirements.txt     # Python依赖
├── vercel.json         # Vercel配置
└── .env                # 环境变量（本地开发用）
```

### 2. 检查关键文件
- ✅ `app.py` - Flask应用
- ✅ `api/index.py` - Vercel入口
- ✅ `vercel.json` - 部署配置
- ✅ `requirements.txt` - 依赖列表

## 步骤二：注册Vercel账号

1. 访问 [Vercel官网](https://vercel.com/)
2. 点击 "Sign Up"
3. 选择 "Continue with GitHub"（推荐）
4. 授权GitHub账号

## 步骤三：部署项目

### 方法一：通过GitHub部署（推荐）

1. **推送代码到GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

2. **在Vercel中导入项目**
   - 登录Vercel控制台
   - 点击 "New Project"
   - 选择你的GitHub仓库
   - 点击 "Import"

3. **配置环境变量**
   - 在项目设置中找到 "Environment Variables"
   - 添加变量：
     - **Name**: `SUNO_API_KEY`
     - **Value**: 你的Suno API密钥
   - 点击 "Save"

4. **部署**
   - 点击 "Deploy"
   - 等待部署完成（通常1-2分钟）

### 方法二：通过Vercel CLI部署

1. **安装Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登录Vercel**
   ```bash
   vercel login
   ```

3. **部署项目**
   ```bash
   vercel
   ```

4. **设置环境变量**
   ```bash
   vercel env add SUNO_API_KEY
   ```

## 步骤四：配置自定义域名（可选）

1. **购买域名**
   - 在阿里云/腾讯云购买域名
   - 或使用免费域名服务

2. **添加域名到Vercel**
   - 在项目设置中找到 "Domains"
   - 点击 "Add Domain"
   - 输入你的域名

3. **配置DNS**
   - 在域名提供商处添加CNAME记录
   - 指向Vercel提供的地址

## 步骤五：测试部署

### 1. 检查部署状态
- 访问Vercel控制台
- 查看部署日志
- 确认没有错误

### 2. 测试功能
- 访问你的Vercel URL
- 测试音乐生成功能
- 确认音频播放正常

## 常见问题解决

### 1. 部署失败
**问题**: Build failed
**解决**: 
- 检查 `requirements.txt` 是否正确
- 确认Python版本兼容
- 查看构建日志

### 2. 环境变量问题
**问题**: API调用失败
**解决**:
- 确认 `SUNO_API_KEY` 已正确设置
- 检查环境变量是否生效

### 3. 路由问题
**问题**: 404错误
**解决**:
- 检查 `vercel.json` 配置
- 确认 `api/index.py` 存在

### 4. 静态文件问题
**问题**: 模板文件无法加载
**解决**:
- 确认 `templates/` 目录结构正确
- 检查文件路径

## 部署后的优势

✅ **完全免费**
- 无限制的部署
- 自动HTTPS
- 全球CDN

✅ **自动部署**
- 连接GitHub后自动部署
- 每次推送代码自动更新

✅ **高性能**
- 边缘计算
- 全球加速
- 自动扩展

✅ **易于管理**
- 简洁的控制台
- 详细的日志
- 实时监控

## 下一步

部署成功后，你可以：
1. 分享你的音乐生成器网站
2. 添加更多功能
3. 优化用户体验
4. 考虑添加数据库存储

需要帮助解决任何问题吗？ 