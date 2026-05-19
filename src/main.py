"""
缓存优化器 CLI 入口
提供命令行接口用于运行缓存优化和查看报告
"""
import os
import sys
import json
import click

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import CacheOptimizerPipeline


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """CacheOptimizer - 缓存策略优化工具"""
    pass


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='输出文件路径')
@click.option('--verbose', '-v', is_flag=True, help='输出详细日志')
def optimize(input_path, output, verbose):
    """运行缓存优化分析"""
    click.echo("开始运行缓存优化分析...")

    # 创建并运行流水线
    pipeline = CacheOptimizerPipeline(verbose=verbose)
    results = pipeline.run(input_path)

    # 保存结果
    if output:
        output_path = output
    else:
        # 默认输出路径
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_name}_analysis.json")

    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    click.echo(f"分析完成！结果已保存到: {output_path}")

    # 输出摘要
    if results.get("status") == "success":
        click.echo("\n✓ 缓存优化分析成功完成")
        summary = results.get("summary", {})
        click.echo(f"  - 成功执行: {summary.get('successful_agents', 0)} 个Agent")
        click.echo(f"  - 失败执行: {summary.get('failed_agents', 0)} 个Agent")

        recommendations = results.get("key_recommendations", [])
        if recommendations:
            click.echo("\n关键建议:")
            for i, rec in enumerate(recommendations[:5], 1):
                click.echo(f"  {i}. {rec}")
    else:
        click.echo("\n✗ 分析过程中出现错误")
        if "error" in results:
            click.echo(f"  错误信息: {results['error']}")


@cli.command()
@click.argument('report_path', type=click.Path(exists=True))
@click.option('--format', '-f', 'fmt', type=click.Choice(['json', 'summary']), default='summary', help='输出格式')
def report(report_path, fmt):
    """查看分析报告"""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if fmt == 'json':
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            # 输出摘要格式
            click.echo("=" * 60)
            click.echo("缓存优化分析报告")
            click.echo("=" * 60)

            status = data.get("status", "unknown")
            click.echo(f"\n状态: {status}")

            summary = data.get("summary", {})
            click.echo(f"\n执行摘要:")
            click.echo(f"  - 总Agent数: {summary.get('total_agents', 0)}")
            click.echo(f"  - 成功执行: {summary.get('successful_agents', 0)}")
            click.echo(f"  - 失败执行: {summary.get('failed_agents', 0)}")

            # 显示各Agent状态
            pipeline_results = data.get("pipeline_results", {})
            if pipeline_results:
                click.echo("\n各Agent执行状态:")
                for agent_name, result in pipeline_results.items():
                    agent_status = result.get("status", "unknown")
                    status_icon = "✓" if agent_status == "success" else "✗"
                    click.echo(f"  {status_icon} {agent_name}: {agent_status}")

            # 显示关键建议
            recommendations = data.get("key_recommendations", [])
            if recommendations:
                click.echo("\n关键建议:")
                for i, rec in enumerate(recommendations[:10], 1):
                    click.echo(f"  {i}. {rec}")

            click.echo("\n" + "=" * 60)

    except Exception as e:
        click.echo(f"读取报告失败: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()