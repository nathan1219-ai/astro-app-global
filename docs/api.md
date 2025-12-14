## API 概览

### 系统
- `GET /api/health`
- `GET /api/bedrock/test?sign&zodiac&element&language`

### 推送
- `POST /api/push/prefs`、`GET /api/push/prefs/{user_id}`
- `POST /api/push/generate`
- `GET /api/push/today/{user_id}?day&language`
- `POST /api/push/send`
- `POST /api/push/send-detail`
- `POST /api/push/send-detail-tokens`
- `POST /api/push/token`
- `GET /api/push/tokens/{user_id}?language`
- `DELETE /api/push/token`
- `POST /api/push/tokens`、`DELETE /api/push/tokens`

### 会员
- `GET /api/membership/{user_id}`
- `GET /api/membership/status/{user_id}`
- `POST /api/membership/upgrade`
- `POST /api/membership/reminders/run`

### 支付 Stripe
- `POST /api/pay/stripe/checkout`
- `GET /api/pay/stripe/confirm?session_id&user_id&level&months`
- `POST /api/pay/stripe/webhook`

### 支付 PayPal
- `POST /api/pay/paypal/order`
- `GET /api/pay/paypal/capture?order_id&user_id&level&months`
- `POST /api/pay/paypal/webhook`

### 社区
- `POST /api/community/post`
- `GET /api/community/list?sign&zodiac&language&offset&limit`
- `POST /api/community/like/{post_id}`
