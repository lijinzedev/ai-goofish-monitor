#!/usr/bin/env python3
"""
前端功能测试脚本
用于验证新品监控任务的前端集成是否正常工作
"""

import asyncio
import json
import aiohttp
import sys

async def test_frontend_integration():
    """测试前端集成功能"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("开始测试前端集成功能...")
    print(f"测试服务器: {base_url}")
    
    async with aiohttp.ClientSession() as session:
        try:
            # 测试1: 检查系统状态
            print("\n测试1: 检查系统状态")
            async with session.get(f"{base_url}/api/settings/status") as resp:
                if resp.status == 200:
                    status = await resp.json()
                    print("✅ 系统状态API正常")
                    print(f"   钉钉webhook配置: {'已配置' if status['env_file']['dingtalk_webhook_set'] else '未配置'}")
                else:
                    print(f"❌ 系统状态API失败: {resp.status}")
                    return False
            
            # 测试2: 获取任务列表
            print("\n测试2: 获取任务列表")
            async with session.get(f"{base_url}/api/tasks") as resp:
                if resp.status == 200:
                    tasks = await resp.json()
                    print(f"✅ 任务列表API正常，共 {len(tasks)} 个任务")
                    
                    # 检查是否有新品监控任务
                    monitor_tasks = [t for t in tasks if t.get('task_type') == 'new_product_monitor']
                    print(f"   其中新品监控任务: {len(monitor_tasks)} 个")
                else:
                    print(f"❌ 任务列表API失败: {resp.status}")
                    return False
            
            # 测试3: 创建新品监控任务
            print("\n测试3: 创建新品监控任务")
            test_task_data = {
                "task_name": "测试新品监控",
                "keyword": "test",
                "personal_only": True,
                "min_price": "100",
                "max_price": "500",
                "monitor_interval": 300,
                "new_product_window": 1800,
                "dingtalk_webhook": None
            }
            
            async with session.post(
                f"{base_url}/api/tasks/new-product-monitor",
                json=test_task_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print("✅ 新品监控任务创建API正常")
                    print(f"   创建的任务ID: {result['task']['id']}")
                    test_task_id = result['task']['id']
                else:
                    error_data = await resp.json()
                    print(f"❌ 新品监控任务创建失败: {resp.status}")
                    print(f"   错误信息: {error_data.get('detail', '未知错误')}")
                    return False
            
            # 测试4: 更新任务状态
            print("\n测试4: 更新任务状态")
            update_data = {"enabled": False}
            async with session.patch(
                f"{base_url}/api/tasks/{test_task_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    print("✅ 任务更新API正常")
                else:
                    print(f"❌ 任务更新失败: {resp.status}")
                    return False
            
            # 测试5: 删除测试任务
            print("\n测试5: 删除测试任务")
            async with session.delete(f"{base_url}/api/tasks/{test_task_id}") as resp:
                if resp.status == 200:
                    print("✅ 任务删除API正常")
                else:
                    print(f"❌ 任务删除失败: {resp.status}")
                    return False
            
            print("\n🎉 所有前端集成测试通过！")
            return True
            
        except aiohttp.ClientError as e:
            print(f"❌ 网络连接错误: {e}")
            print("请确保Web服务器正在运行 (python web_server.py)")
            return False
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            return False

async def main():
    print("前端功能测试脚本")
    print("=" * 50)
    print("注意：请确保Web服务器正在运行")
    print("启动命令：python web_server.py")
    print("=" * 50)
    
    success = await test_frontend_integration()
    
    if success:
        print("\n✅ 前端集成测试完成，所有功能正常！")
        print("\n下一步：")
        print("1. 在浏览器中访问 http://127.0.0.1:8000")
        print("2. 点击 '🆕 新品监控任务' 按钮")
        print("3. 填写任务信息并创建")
        print("4. 检查任务列表中是否显示新的监控任务")
    else:
        print("\n❌ 前端集成测试失败，请检查错误信息")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
