# Cosmic Totem Arcana

## 概述
文案生成、推送、会员与支付的全栈实现。前端基于 Vite + Vue3，后端基于 FastAPI，集成 Amazon Bedrock、FCM、Stripe、PayPal。

## 目录结构
- frontend：前端应用
- backend：后端服务

## 环境配置
在 `backend/.env` 填写：
- FCM_CREDENTIALS_PATH 或 GOOGLE_APPLICATION_CREDENTIALS
- STRIPE_SECRET_KEY、STRIPE_WEBHOOK_SECRET、STRIPE_PRICE_PREMIUM、STRIPE_PRICE_VIP、PUBLIC_BASE_URL、CORS_ORIGINS
- PAYPAL_ENV、PAYPAL_CLIENT_ID、PAYPAL_CLIENT_SECRET、PAYPAL_WEBHOOK_ID
- AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY、AWS_REGION、BEDROCK_MODEL_ID

## 启动
后端：在 `backend` 目录运行 `uvicorn app:app --host 127.0.0.1 --port 8000 --reload`
前端：在 `frontend` 目录运行 `npm run dev`，访问 `http://localhost:5173/`（端口占用时自动切换）

## 关键页面
- `/membership`：Stripe/PayPal 支付与会员刷新
- `/push`：设备 Token 注册、批量管理、发送明细与失败重试
- `/`：卡牌首页

## Webhook
- Stripe：`/api/pay/stripe/webhook`
- PayPal：`/api/pay/paypal/webhook`

## 健康检查
`GET /api/health` 返回关键配置加载状态

## 开发与部署建议
- 使用 `.env` 管理密钥，不入库
- CORS 按前端端口与域名维护 `CORS_ORIGINS`
- 订阅价格使用 `subscription` 模式，续费事件联动更新会员到期

## 部署
### 前提
- Python 3.11.x、Node.js 18+、npm
- Stripe/PayPal 测试或生产凭据
- Firebase 服务账号 JSON（FCM）
- AWS 账户（Bedrock）

### 后端
1. 配置环境变量到 `backend/.env`
2. 生产运行示例（Windows）：
   - 前台启动：`uvicorn app:app --host 0.0.0.0 --port 8000`
   - 后台服务：使用任务计划或 NSSM 注册为服务，执行同上命令
3. 反向代理（示例 Nginx）：
   - 将 `https://api.yourdomain.com` 代理到 `http://127.0.0.1:8000`
   - Webhook 路径：`/api/pay/stripe/webhook`、`/api/pay/paypal/webhook`
4. CORS：在 `.env` 设置 `CORS_ORIGINS=https://your-frontend-domain`

### 前端
1. 设置 API 基础地址：`frontend/.env.production`
   - `VITE_API_BASE=https://api.yourdomain.com/api`
2. 构建：`npm run build`
3. 部署 `frontend/dist` 到静态服务器（Nginx/Apache/Netlify 等）

### Stripe 配置
- Webhook 端点：`https://api.yourdomain.com/api/pay/stripe/webhook`
- 事件：`checkout.session.completed`、`invoice.payment_succeeded`、`invoice.payment_failed`、`customer.subscription.updated`
- 签名密钥：写入 `STRIPE_WEBHOOK_SECRET`
- 价格：
  - 一次性价格 → Checkout `mode=payment`
  - 订阅价格（recurring） → Checkout `mode=subscription`

### PayPal 配置
- 环境：`PAYPAL_ENV=sandbox` 或 `live`
- 凭据：`PAYPAL_CLIENT_ID`、`PAYPAL_CLIENT_SECRET`
- Webhook ID：`PAYPAL_WEBHOOK_ID`
- 端点：`https://api.yourdomain.com/api/pay/paypal/webhook`

### 验证清单
- 健康检查：`GET /api/health`
- 前端页面：`/membership`、`/push`
- 支付联调：前端点击 `Pay/PayPal` → 返回后会员更新；Webhook 回调成功（200）
- 推送联调：注册 Token → `Send Detail` 查看逐条结果 → `Retry Failed`

### 迁移与数据
- 使用 `sqlite`：首启自动建表，数据位于 `backend/data.db`
- 备份策略：定期复制数据库文件或迁移到托管数据库（PostgreSQL/MySQL）

### 运维建议
- 日志与告警：Webhook 签名失败/订阅失败加入告警渠道（邮件/Slack）
- 安全：为管理接口加入鉴权（JWT/API Key），限制敏感操作权限
- 域名与 TLS：为前后端与 Webhook 使用 HTTPS 与有效证书
