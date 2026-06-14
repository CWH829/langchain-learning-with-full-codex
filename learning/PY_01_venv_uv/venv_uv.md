# PY-01 venv / uv 环境笔记

## 本节目标

理解 Python 项目里的“解释器、虚拟环境、依赖管理、IDE 解释器配置”分别是什么，并能自己判断依赖到底装到了哪个环境里。

这次实际完成的环境闭环：

```text
安装 uv -> 选择 Python 版本 -> 创建 .venv -> uv sync 安装依赖 -> PyCharm 选择 .venv 解释器
```

## 核心概念

Python 解释器是能运行 Python 代码的程序，例如：

```text
C:\Users\Caowenhan\AppData\Local\Programs\Python\Python312\python.exe
```

虚拟环境是项目自己的隔离运行环境。本项目的虚拟环境是：

```text
E:\Java\project\langchain-learning-with-full-codex\.venv
```

项目真正应该使用的解释器是：

```text
E:\Java\project\langchain-learning-with-full-codex\.venv\Scripts\python.exe
```

`uv` 是依赖和虚拟环境管理工具。可以先粗略类比成 Python 生态里的 Maven/Gradle + venv 管理器，但不要完全等同：Python 的解释器版本、虚拟环境和包安装位置更容易混在一起出问题。

## 常用命令

检查 uv：

```powershell
uv --version
```

用指定 Python 版本创建虚拟环境：

```powershell
uv venv --python 3.12
```

根据 `pyproject.toml` 和 `uv.lock` 同步依赖：

```powershell
uv sync
```

添加新依赖，并写入 `pyproject.toml` 和 `uv.lock`：

```powershell
uv add langchain-openai
```

运行项目脚本：

```powershell
uv run python -m learning.LC_02_minimal_agent.hello_agent
```

确认当前项目虚拟环境里的 Python：

```powershell
.\.venv\Scripts\python.exe --version
```

确认依赖是否真的装进当前 `.venv`：

```powershell
.\.venv\Scripts\python.exe -c "import langchain; print(langchain.__version__)"
```

## 这次踩过的坑

### 1. `pip install` 装错环境

如果直接执行：

```powershell
pip install langchain-openai
```

它可能装到全局 Python，而不是当前项目 `.venv`。结果就是运行项目时仍然报：

```text
ImportError: Initializing ChatOpenAI requires the langchain-openai package.
```

本项目优先使用：

```powershell
uv add langchain-openai
```

### 2. `.venv` 存在不等于依赖已安装

`.venv\Scripts\python.exe` 能运行，只说明虚拟环境存在；还要用 import 验证依赖：

```powershell
.\.venv\Scripts\python.exe -c "import langchain; print(langchain.__version__)"
```

### 3. Python 版本太新可能让 IDE 或依赖链更难排查

本项目一开始使用 Python 3.14，PyCharm 解释器识别一直卡住。后来切换到 Python 3.12 后，环境更稳定。

学习阶段建议优先选稳定版本，例如 Python 3.12，而不是追最新解释器。

### 4. PyCharm 要选择项目 `.venv`，不是全局 Python

PyCharm 解释器路径应选择：

```text
E:\Java\project\langchain-learning-with-full-codex\.venv\Scripts\python.exe
```

不要选择全局路径，例如：

```text
C:\Users\...\Python312\python.exe
```

全局 Python 只是创建虚拟环境的基础解释器；项目运行应使用 `.venv` 里的解释器。

## Java 开发者视角

可以这样类比：

```text
Python 解释器版本        类似 JDK 版本
.venv                  类似当前项目独立的运行环境
pyproject.toml          类似 pom.xml / build.gradle 的依赖声明
uv.lock                 类似 lock file，记录精确依赖解析结果
uv sync                 类似根据声明和 lock 同步依赖
uv add xxx              类似添加依赖并更新配置
```

但 Python 和 Java 最大不同是：包安装位置跟“当前使用哪个解释器”强绑定。排查 Python 依赖问题时，第一反应应该是确认：

```text
代码用哪个 python.exe 运行？
依赖装进了哪个 python.exe 对应的环境？
IDE 是否也用同一个 python.exe？
```

## 本次总结

PY-01 的关键收获不是记住某个命令，而是形成排查顺序：

```text
先看解释器路径 -> 再看虚拟环境 -> 再看依赖是否装进去 -> 最后看 IDE 是否选对解释器
```

以后遇到 `ModuleNotFoundError` 或 IDE 识别异常，先用 `.venv\Scripts\python.exe -c "import xxx"` 验证项目环境，不要急着反复 `pip install`。
