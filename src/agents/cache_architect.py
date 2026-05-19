"""
缓存架构 Agent
负责设计缓存策略、架构优化和配置建议
"""
import json
from ..utils import call_llm


def analyze(data):
    """
    分析缓存架构并提供优化方案

    Args:
        data: 包含当前架构和流量分析结果的字典

    Returns:
        dict: 缓存架构优化方案
    """
    system_prompt = """你是一个缓存架构专家，负责设计高效的缓存策略和架构优化方案。
    请根据提供的数据，设计以下内容：
    1. 缓存层级设计（L1/L2/L3缓存）
    2. 缓存策略选择（LRU、LFU、TTL等）
    3. 缓存键设计规范
    4. 数据一致性方案
    5. 容量规划

    请以JSON格式返回架构方案，包含以下字段：
    - cache_hierarchy: 缓存层级设计
    - cache_strategy: 缓存策略方案
    - key_design: 缓存键设计规范
    - consistency_plan: 数据一致性方案
    - capacity_planning: 容量规划
    - implementation_guide: 实施指南"""

    prompt = f"""请根据以下信息设计缓存架构优化方案：

当前缓存配置：{data.get('current_cache_config', {})}
流量分析结果：{json.dumps(data.get('traffic_analysis', {}), ensure_ascii=False, indent=2)}
热点数据：{json.dumps(data.get('hot_data', []), ensure_ascii=False, indent=2)}
端点信息：{json.dumps(data.get('endpoints', []), ensure_ascii=False, indent=2)}

请提供详细的缓存架构设计方案，包括具体的配置建议和实施步骤。"""

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
            result["agent"] = "cache_architect"
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "agent": "cache_architect",
                "status": "success",
                "architecture": response,
                "raw_response": True
            }
    except Exception as e:
        return {
            "agent": "cache_architect",
            "status": "error",
            "error": str(e)
        }