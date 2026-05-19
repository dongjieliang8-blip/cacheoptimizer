# CacheOptimizer — 缓存策略优化 Agent

基于多 Agent 长链推理的缓存策略优化系统。

## 安装

```bash
pip install -r requirements.txt
```

## 配置

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
DEEPSEEK_MODEL=mimo-v2.5
```

## 使用

```bash
# 运行缓存优化
python -m src.main optimize --input ./demo/sample_data/sample_traffic.json

# 查看报告
python -m src.main report --input ./output/cacheoptimizer_report.json
```

## 项目结构

```
cacheoptimizer/
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── utils.py
│   └── agents/
│       ├── traffic_analyzer.py
│       ├── cache_architect.py
│       ├── protection_agent.py
│       └── monitor_agent.py
├── demo/sample_data/
├── tests/
├── requirements.txt
└── APPLICATION.md
```
