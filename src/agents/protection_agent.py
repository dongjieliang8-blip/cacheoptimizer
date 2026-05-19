"""
防护设计 Agent
负责设计缓存防护机制、容错处理和降级策略
"""
import json
from ..utils import call_llm


def analyze(data):
    """
    分析并设计缓存防护机制

    Args:
        data: 包含当前架构和风险评估的字典

    Returns:
        dict: 缓存防护设计方案
    """
    system_prompt = """你是一个缓存防护专家，负责设计缓存系统的防护机制和容错处理方案。
    请根据提供的数据，设计以下内容：
    1. 缓存穿透防护（布隆过滤器、空值缓存）
    2. 缓存雪崩防护（TTL随机化、限流）
    3. 缓存击穿防护（互斥锁、永不过期）
    4. 数据一致性保障
    5. 降级策略
    6. 监控告警机制

    请以JSON格式返回防护方案，包含以下字段：
    - penetration_protection: 缓存穿透防护方案
    - avalanche_protection: 缓存雪崩防护方案
    - breakdown_protection: 缓存击穿防护方案
    - consistency_guarantee: 数据一致性保障方案
    - degradation_strategy: 降级策略
    - monitoring_alerts: 监控告警机制
    - implementation_plan: 实施计划"""

    prompt = f"""请根据以下信息设计缓存防护方案：

当前缓存架构：{json.dumps(data.get('cache_architecture', {}), ensure_ascii=False, indent=2)}
流量分析结果：{json.dumps(data.get('traffic_analysis', {}), ensure_ascii=False, indent=2)}
风险评估：{json.dumps(data.get('risk_assessment', {}), ensure_ascii=False, indent=2)}
当前配置：{data.get('current_cache_config', {})}

请提供详细的缓存防护设计方案，包括具体的防护措施和应急处理流程。"""

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
            result["agent"] = "protection_agent"
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "agent": "protection_agent",
                "status": "success",
                "protection_plan": response,
                "raw_response": True
            }
    except Exception as e:
        return {
            "agent": "protection_agent",
            "status": "error",
            "error": str(e)
        }