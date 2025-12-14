# Astro App Global

## 概述
- 前端：Vue 3 + Vite，包含卡牌渲染、分享导出、引导注册、会员与支付、推送管理
- 后端：FastAPI，提供命理计算、AI 文案包、推送、支付、分享奖励与短链、认证等接口

## 代码结构
- `frontend/` 前端应用
- `backend/` 后端服务

## 环境要求
- Python 3.10
- Node.js 18（包管理器使用 npm）

## 本地启动（开发模式）
- 后端
  - 进入 `backend` 目录
  - 创建并激活虚拟环境（Windows PowerShell）：
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`
  - 安装依赖：
    - `pip install -r requirements.txt`
  - 运行服务：
    - `uvicorn app:app --host 127.0.0.1 --port 8000 --reload`
- 前端
  - 进入 `frontend` 目录
  - 安装依赖：`npm install`
  - 启动开发服务：`npm run dev`
  - 默认访问 `http://localhost:5173`，已配置代理到后端 `http://127.0.0.1:8000`

## 环境变量（最小集）
- 后端（`backend/.env`）
  - `PUBLIC_BASE_URL`（必填，用于短链和 OG 抓取，如 `https://app.example.com`）
  - `STRIPE_SECRET_KEY`、`STRIPE_WEBHOOK_SECRET`
  - `PAYPAL_WEBHOOK_ID`
  - `AWS_REGION` 或 `AWS_DEFAULT_REGION`
  - `FCM_CREDENTIALS_PATH` 或 `GOOGLE_APPLICATION_CREDENTIALS`
- 前端（`frontend/.env` 或 `frontend/.env.development`）
  - `VITE_GOOGLE_CLIENT_ID`（Google 登录）
  - 如需自定义后端地址：`VITE_API_BASE=https://api.example.com/api`

## 环境变量示例
- `backend/.env`（示例）
  - `PUBLIC_BASE_URL=https://app.example.com`
  - `STRIPE_SECRET_KEY=sk_live_...`
  - `STRIPE_WEBHOOK_SECRET=whsec_...`
  - `PAYPAL_WEBHOOK_ID=...`
  - `AWS_REGION=ap-southeast-2`
  - `FCM_CREDENTIALS_PATH=C:\\path\\to\\firebase.json`
- `frontend/.env.development`（示例）
  - `VITE_API_BASE=http://127.0.0.1:8000/api`
  - `VITE_GOOGLE_CLIENT_ID=...apps.googleusercontent.com`

## 关键接口
- 认证：`POST /api/auth/register`、`POST /api/auth/login`、`GET /api/auth/check`、`POST /api/auth/oauth/google`、`POST /api/auth/oauth/apple`
- 个人偏好：`POST /api/profile/lang`、`POST /api/profile/consent`
- 命理与卡牌：`POST /api/calc`、`GET /api/user/fate/{user_id}`、`GET /api/card/details`、`GET /api/card/free-pack`、`GET /api/card/premium-pack`、`GET /api/card/line-detail`
- 推送：偏好/令牌/发送/详版/失败重试
- 支付：Stripe（checkout/confirm/webhook）、PayPal（order/capture/webhook）
- 分享与奖励：`POST /api/share/success`、`POST /api/share/referral`、`POST /api/share/referral-paid`、`GET /api/share/permissions/{user_id}`、`POST /api/share/consume-credit`、`POST /api/share/shorten`、`GET /s/{code}`、`GET /api/share/og-image`

## 分享与短链
- 自动生成短链 `/s/{code}`，OG/Twitter 元信息按语言本地化
- 前端一键导出平台尺寸：Instagram(1080×1350)、TikTok(1080×1920 PNG)、Facebook(1200×630)、WhatsApp(750×1000 WebP)

## 安全与合规
- GDPR 同意位：`POST /api/profile/consent`
- Webhook 验签：Stripe/PayPal
- 不提交任何密钥或凭据（如 `google-services.json`、`.env`）

## 分支策略
- 以 `main` 为主；后续如需 `develop` 将另行说明

## 常见问题
- **无法访问后端**：检查前端 `VITE_API_BASE` 与后端监听端口
- **短链不抓取**：确保 `PUBLIC_BASE_URL` 指向公网域名，OG 页可被平台爬取
- **推送失败**：检查 FCM 服务账号路径与令牌有效性

## 联系方式
- 协作者：TREAMENG（GitHub）
- Owner 邮箱：nathan.dengshuai@gmail.com
