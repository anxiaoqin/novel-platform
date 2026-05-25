# 网文创作平台

一个面向网文作者的在线创作平台，支持小说管理、章节编辑、AI辅助写作。

## 技术栈

- **前端**：Vue 3 + Vite + Element Plus + Pinia
- **后端**：Flask + SQLAlchemy + Gunicorn
- **数据库**：PostgreSQL (Supabase)
- **部署**：Render (后端) + Vercel (前端)

## 本地开发

### 后端
```bash
cd novel_platform_backend
pip install -r requirements.txt
python app.py
```

### 前端
```bash
npm install
npm run dev
```

## 环境变量

### 后端 (Render)
| 变量 | 说明 |
|------|------|
| DATABASE_URL | PostgreSQL连接字符串 |
| SECRET_KEY | JWT密钥 |
| ALLOWED_ORIGINS | 允许的前端域名 |
| PORT | 服务端口（Render自动注入） |

### 前端 (Vercel)
| 变量 | 说明 |
|------|------|
| VITE_API_URL | 后端API地址 |

## 项目结构
```
├── novel_platform_backend/   # Flask后端
│   ├── app.py               # 主应用
│   ├── requirements.txt     # Python依赖
│   ├── Procfile             # Render启动命令
│   └── runtime.txt          # Python版本
├── src/                     # Vue前端
│   ├── api/                 # API封装
│   ├── views/               # 页面组件
│   ├── stores/              # Pinia状态
│   └── router/              # 路由配置
├── package.json             # Node依赖
├── vite.config.js           # Vite配置
└── vercel.json              # Vercel部署配置
```
