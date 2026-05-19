"""
流量分析 Agent
负责分析流量模式、识别热点数据和优化机会
"""
import json
from ..utils import call_llm


def analyze(data):
    """
    分析流量数据，识别缓存优化机会

    Args:
        data: 包含流量统计和端点信息的字典

    Returns:
        dict: 流量分析结果
    """
    system_prompt = """你是一个流量分析专家，负责分析API流量模式并识别缓存优化机会。
    请根据提供的流量数据，分析以下内容：
    1. 热点数据识别
    2. 流量模式分析
    3. 缓存命中率评估
    4. 优化机会识别

    请以JSON格式返回分析结果，包含以下字段：
    - hot_data: 热点数据列表
    - traffic_patterns: 流量模式分析
    - cache_hit_analysis: 缓存命中率分析
    - optimization_opportunities: 优化机会列表
    - recommendations: 具体建议"""

    prompt = f"""请分析以下流量数据并提供缓存优化建议：

服务名称：{data.get('service_name', '未知服务')}
时间范围：{data.get('time_range', {})}
流量摘要：{data.get('traffic_summary', {})}
端点信息：{json.dumps(data.get('endpoints', []), ensure_ascii=False, indent=2)}
热点键：{json.dumps(data.get('hot_keys', []), ensure_ascii=False, indent=2)}
当前缓存配置：{data.get('current_cache_config', {})}
数据库指标：{data.get('database_metrics', {})}

请提供详细的流量分析报告和缓存优化建议。"""

    try:
        response = call_llm(prompt, system_prompt)

        # 尝试解析JSON响应
        try:
            # 尝试提取JSON部分
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            result = json.loads(json_str)
            result["agent"] = "traffic_analyzer"
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回原始响应
            return {
                "agent": "traffic_analyzer",
                "status": "success",
                "analysis": response,
                "raw_response": True
            }
    except Exception as e:
        return {
            "agent": "traffic_analyzer",
            "status": "error",
            "error": str(e)
        }