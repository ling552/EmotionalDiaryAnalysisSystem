# 情绪日记分析系统（Emotional Diary Analysis System）

一个轻量级的情绪日记 Web 应用：用户可记录每日心情与生活事件，系统对日记文本进行情绪分析，自动生成情绪标签与得分，并通过图表展示情绪变化趋势，同时提供简单的心理建议。

- 主题色：马卡龙蓝 + 马卡龙粉
- 前端：HTML / CSS / JavaScript（Chart.js）
- 后端：Python Django

## 功能

- 用户管理
  - 注册 / 登录 / 退出
  - 个人信息管理（邮箱）
  - 修改密码
- 日记管理
  - 新建 / 查看列表 / 编辑 / 删除
  - 关键词搜索、按日期筛选
  - 日记与用户账号关联隔离
- 情绪分析
  - 基于词典匹配的轻量情绪识别
  - 计算情绪得分并保存
- 情绪统计与建议
  - 近 30 条日记情绪得分折线图
  - 情绪占比（环形图）
  - 根据近期情绪状态给出心理建议

## 运行环境

- Python 3.9+
- Django 4.x / 5.x
- 默认数据库：SQLite

## 快速开始

### 1) 安装依赖

在项目根目录：

```bash
pip install -r requirements.txt
```

### 2) 进入 Django 项目目录

`manage.py` 位于 `emotion_diary/` 下：

```bash
cd emotion_diary
```

### 3) 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4) 启动开发服务器

```bash
python manage.py runserver 127.0.0.1:8000
```

浏览器访问：

- http://127.0.0.1:8000/login/
- http://127.0.0.1:8000/register/

## 目录结构

```text
EmotionalDiaryAnalysisSystem/
├─ requirements.txt
├─ README.md
├─ LICENSE
└─ emotion_diary/
   ├─ manage.py
   ├─ emotion_diary/               # 项目配置
   ├─ users/                       # 用户模块
   ├─ diary/                       # 日记模块（Diary 模型）
   ├─ analysis/                    # 情绪分析与建议
   ├─ templates/                   # HTML 模板
   └─ static/                      # 静态资源（CSS/JS/Images）
```

## 使用说明

1. 注册并登录
2. 进入“日记”创建日记（建议写入包含情绪词的文本，如“开心/焦虑/压力/难过”等）
3. 在“统计”页面查看趋势图与情绪占比，并阅读系统建议

## 常见问题（FAQ）

### 1) 提交表单出现 403 CSRF Forbidden

如果你通过 IDE 预览代理端口访问（例如 `http://127.0.0.1:xxxxx/`），Django 的 CSRF Origin 校验可能不通过。

推荐做法：

- 直接访问 `http://127.0.0.1:8000/`（最稳定）

如需使用代理端口，请在 `emotion_diary/settings.py` 的 `CSRF_TRUSTED_ORIGINS` 中加入对应的 origin。

### 2) 运行 `python manage.py migrate` 提示找不到 manage.py

请确认当前工作目录在 `emotion_diary/`：

```bash
cd emotion_diary
python manage.py migrate
```

## License

本项目使用 MIT License，详见 [LICENSE](./LICENSE)。
