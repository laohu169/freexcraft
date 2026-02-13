# FreeXCraft 服务器自动续期

这个 GitHub Actions 工作流会每小时自动访问 FreeXCraft 的续期页面，填写你的服务器子域名并点击续期按钮。

## 功能

- ✅ 每小时自动执行（在每小时的第5分钟）
- ✅ 自动填写子域名 `laohu.xmania.me`
- ✅ 自动点击 "Renew & Start" 按钮
- ✅ 记录详细日志
- ✅ 支持手动触发
- ✅ 无需账号密码

## 设置步骤

### 1. 创建 GitHub 仓库

1. 登录 GitHub
2. 创建一个新的仓库（可以是私有仓库）
3. 记下仓库地址

### 2. 上传文件

将以下文件上传到你的 GitHub 仓库：

```
你的仓库/
├── .github/
│   └── workflows/
│       └── auto-renew.yml
├── renew.py
└── README.md
```

### 3. 启用 GitHub Actions

1. 进入你的仓库页面
2. 点击 "Actions" 标签
3. 如果提示启用 Actions，点击 "I understand my workflows, go ahead and enable them"

### 4. 修改配置（可选）

如果你需要修改子域名，编辑 `renew.py` 文件：

```python
SUBDOMAIN = "你的子域名.xmania.me"
```

如果你需要修改执行频率，编辑 `.github/workflows/auto-renew.yml` 文件：

```yaml
schedule:
  - cron: '5 * * * *'  # 每小时第5分钟执行
  # 其他示例：
  # - cron: '0 */2 * * *'  # 每2小时执行
  # - cron: '0 0 * * *'    # 每天执行一次
```

## 使用方法

### 自动执行

配置完成后，GitHub Actions 会按照设定的时间自动运行，无需任何操作。

### 手动执行

如果你想立即执行一次续期：

1. 进入仓库的 "Actions" 标签
2. 点击左侧的 "Auto Renew Server"
3. 点击右侧的 "Run workflow" 按钮
4. 点击绿色的 "Run workflow" 确认

### 查看日志

1. 进入 "Actions" 标签
2. 点击任意一次执行记录
3. 点击 "renew" 查看详细日志
4. 可以下载 "renewal-logs" 附件查看完整日志

## 工作流程

1. GitHub Actions 按计划启动
2. 设置 Python 环境
3. 安装 Playwright 浏览器自动化工具
4. 执行 `renew.py` 脚本：
   - 打开浏览器访问续期页面
   - 填写子域名
   - 点击 "Renew & Start" 按钮
   - 记录执行结果
5. 上传日志文件

## 故障排除

### Actions 没有运行

- 检查仓库的 Actions 是否已启用
- 确保 `.github/workflows/auto-renew.yml` 文件路径正确
- 私有仓库可能需要检查 Actions 配额

### 续期失败

- 查看日志了解具体错误
- 检查网站是否可访问
- 确认子域名拼写正确

### 查看详细日志

在 Actions 执行记录中下载 "renewal-logs" 附件，里面包含完整的执行日志。

## 注意事项

- GitHub Actions 的免费配额：公开仓库无限制，私有仓库每月 2000 分钟
- 每次执行大约需要 1-2 分钟
- 按每小时执行一次计算，每月约需 50-100 分钟
- 建议定期检查日志确保正常运行

## 技术栈

- Python 3.11
- Playwright（浏览器自动化）
- GitHub Actions

## 许可

本项目仅供学习和个人使用。
