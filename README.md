# 护网漏洞库

护网（HW）期间漏洞情报汇总，包含 0day / 1day / nday 漏洞数据。

> 原数据维护于腾讯文档，因人数限制迁移至此。

## 数据格式

每漏洞一个独立 TOML 文件，按年份目录存放：

```
docs/
├── 2023/  ← 325 条
├── 2024/  ← 455 条
├── 2025/  ← 333 条
└── 2026/  ← x 条
```

## 提交漏洞

### 方式一：提交 Issue（推荐）

1. 在站点页面顶部点击「＋ 提交漏洞」
2. 填写表单 → 自动创建 GitHub Issue
3. 维护者审核后打 `审核通过` label
4. GitHub Actions 自动提取数据 → 写入 TOML → 重建站点

### 方式二：提交 PR

直接往 `docs/{year}/` 目录新增 TOML 文件提交 PR，格式参考：

```toml
vendor = "厂商名"
name = "漏洞名称"
type = "RCE"
version = "受影响版本"
path = "/利用路径"
detail = "漏洞详情 / POC"
fix = "处置建议"
date = "0730"
label = "0day"        # 0day | 1day | nday
verifier = "AdySec"   # 验真人（2025+）
```

### 方式三：发送邮件

发送漏洞信息至 [admin@adysec.com](mailto:admin@adysec.com)，包含厂商、漏洞名称、类型、POC 等关键信息。

## 目录说明

```
.github/
├── ISSUE_TEMPLATE/submit-vulnerability.md   # Issue 模板
└── workflows/update-data.yml                # 审核通过后自动更新
docs/
├── {year}/*.toml                            # 源数据（TOML）
└── assets/css/style.css                     # 暗黑模式样式
scripts/
├── build-static.py      # 核心：TOML → 静态 HTML
└── process-issue.py     # Issue → TOML（GitHub Actions 用）
index.html / 2023.html / ...                 # 构建产物
CNAME                                         # 自定义域名
.nojekyll                                    # 禁用 Jekyll
```
