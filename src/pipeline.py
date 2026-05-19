"""
缓存优化流水线编排
按顺序执行四个Agent：流量分析、缓存架构、防护设计、监控调优
"""
import json
import os
from typing import Dict, Any, Optional

from .agents import traffic_analyzer, cache_architect, protection_agent, monitor_agent


class CacheOptimizerPipeline:
    """缓存优化流水线"""

    def __init__(self, verbose: bool = False):
        """
        初始化流水线

        Args:
            verbose: 是否输出详细日志
        """
        self.verbose = verbose
        self.results = {}

    def log(self, message: str):
        """输出日志"""
        if self.verbose:
            print(f"[CacheOptimizer] {message}")

    def run(self, input_path: str) -> Dict[str, Any]:
        """
        运行完整的缓存优化流水线

        Args:
            input_path: 输入数据文件路径

        Returns:
            dict: 汇总结果
        """
        self.log(f"开始运行缓存优化流水线，输入文件: {input_path}")

        # 1. 加载输入数据
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
            self.log("输入数据加载成功")
        except Exception as e:
            return {
                "status": "error",
                "error": f"加载输入数据失败: {str(e)}"
            }

        # 2. 执行流量分析
        self.log("执行流量分析...")
        traffic_result = traffic_analyzer.analyze(input_data)
        self.results["traffic_analysis"] = traffic_result

        if traffic_result.get("status") == "error":
            self.log(f"流量分析失败: {traffic_result.get('error')}")
        else:
            self.log("流量分析完成")

        # 3. 执行缓存架构设计
        self.log("执行缓存架构设计...")
        architect_data = {
            "current_cache_config": input_data.get("current_cache_config", {}),
            "traffic_analysis": traffic_result,
            "hot_data": traffic_result.get("hot_data", []),
            "endpoints": input_data.get("endpoints", [])
        }
        architect_result = cache_architect.analyze(architect_data)
        self.results["cache_architecture"] = architect_result

        if architect_result.get("status") == "error":
            self.log(f"缓存架构设计失败: {architect_result.get('error')}")
        else:
            self.log("缓存架构设计完成")

        # 4. 执行防护设计
        self.log("执行防护设计...")
        protection_data = {
            "cache_architecture": architect_result,
            "traffic_analysis": traffic_result,
            "risk_assessment": self._assess_risks(input_data, traffic_result),
            "current_cache_config": input_data.get("current_cache_config", {})
        }
        protection_result = protection_agent.analyze(protection_data)
        self.results["protection_plan"] = protection_result

        if protection_result.get("status") == "error":
            self.log(f"防护设计失败: {protection_result.get('error')}")
        else:
            self.log("防护设计完成")

        # 5. 执行监控调优
        self.log("执行监控调优...")
        monitor_data = {
            "cache_architecture": architect_result,
            "protection_plan": protection_result,
            "performance_metrics": input_data.get("traffic_summary", {}),
            "traffic_analysis": traffic_result
        }
        monitor_result = monitor_agent.analyze(monitor_data)
        self.results["monitoring_plan"] = monitor_result

        if monitor_result.get("status") == "error":
            self.log(f"监控调优失败: {monitor_result.get('error')}")
        else:
            self.log("监控调优完成")

        # 6. 生成汇总结果
        summary = self._generate_summary()
        self.log("流水线执行完成")

        return summary

    def _assess_risks(self, input_data: Dict, traffic_result: Dict) -> Dict:
        """评估风险"""
        cache_config = input_data.get("current_cache_config", {})
        traffic_summary = input_data.get("traffic_summary", {})

        risks = {
            "memory_usage_risk": "high" if cache_config.get("current_memory_usage_mb", 0) / cache_config.get("max_memory_mb", 1) > 0.85 else "low",
            "hit_rate_risk": "high" if traffic_summary.get("cache_hit_rate", 0) < 0.5 else "low",
            "latency_risk": "high" if traffic_summary.get("p99_latency_ms", 0) > 500 else "low",
            "error_rate_risk": "high" if traffic_summary.get("error_rate", 0) > 0.01 else "low"
        }

        return {
            "overall_risk": "high" if any(v == "high" for v in risks.values()) else "low",
            "details": risks
        }

    def _generate_summary(self) -> Dict[str, Any]:
        """生成汇总结果"""
        # 检查所有Agent是否都成功执行
        all_success = all(
            result.get("status") == "success"
            for result in self.results.values()
        )

        summary = {
            "status": "success" if all_success else "partial",
            "pipeline_results": self.results,
            "summary": {
                "total_agents": 4,
                "successful_agents": sum(
                    1 for result in self.results.values()
                    if result.get("status") == "success"
                ),
                "failed_agents": sum(
                    1 for result in self.results.values()
                    if result.get("status") == "error"
                )
            }
        }

        # 提取关键建议
        recommendations = []
        for agent_name, result in self.results.items():
            if result.get("status") == "success":
                # 尝试从结果中提取建议
                if "recommendations" in result:
                    recommendations.extend(result["recommendations"])
                elif "suggestions" in result:
                    recommendations.extend(result["suggestions"])

        summary["key_recommendations"] = recommendations[:10]  # 最多10条建议

        return summary

    def save_results(self, output_path: str):
        """保存结果到文件"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            self.log(f"结果已保存到: {output_path}")
            return True
        except Exception as e:
            self.log(f"保存结果失败: {str(e)}")
            return False