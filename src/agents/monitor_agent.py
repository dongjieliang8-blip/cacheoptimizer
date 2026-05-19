"""
监控调优 Agent
负责监控缓存性能、自动调优和持续优化
"""
import json
from ..utils import call_llm


def analyze(data):
    """
    分析并设计监控调优方案

    Args:
        data: 包含当前架构、防护方案和性能指标的字典

    Returns:
        dict: 监控调优方案
    """
    system_prompt = """你是一个缓存监控调优专家，负责设计缓存监控体系和自动调优策略。
    请根据提供的数据，设计以下内容：
    1. 监控指标体系（命中率、延迟、内存使用等）
    2. 告警规则设计
    3. 自动调优策略
    4. 性能基线建立
    5. 持续优化机制

    请以JSON格式返回监控调优方案，包含以下字段：
    - monitoring_metrics: 监控指标体系
    - alert_rules: 告警规则设计
    - auto_tuning: 自动调优策略
    - performance_baseline: 性能基线
    - continuous_optimization: 持续优化机制
    - dashboard_design: 监控面板设计
    - implementation_guide: 实施指南"""

    prompt = f"""请根据以下信息设计缓存监控调优方案：

当前缓存架构：{json.dumps(data.get('cache_architecture', {}), ensure_ascii=False, indent=2)}
防护方案：{json.dumps(data.get('protection_plan', {}), ensure_ascii=False, indent=2)}
当前性能指标：{json.dumps(data.get('performance_metrics', {}), ensure_ascii=False, indent=2)}
流量分析结果：{json.dumps(data.get('traffic_analysis', {}), ensure_ascii=False, indent=2)}

请提供详细的监控调优方案，包括具体的监控指标、告警阈值和调优策略。"""

    try:
        response = call_llm(prompt, system_prompt)

        # 尝试解析JSON响应
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            result = json.loads(json_str)
            result["agent"] = "monitor_agent"
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "agent": "monitor_agent",
                "status": "success",
                "monitoring_plan": response,
                "raw_response": True
            }
    except Exception as e:
        return {
            "agent": "monitor_agent",
            "status": "error",
            "error": str(e)
        }