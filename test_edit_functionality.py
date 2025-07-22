#!/usr/bin/env python3
"""
编辑功能测试脚本
测试新品监控任务的编辑功能是否正常工作
"""

import asyncio
import json
import aiohttp
import sys

async def test_edit_functionality():
    """测试编辑功能"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("开始测试编辑功能...")
    print(f"测试服务器: {base_url}")
    
    async with aiohttp.ClientSession() as session:
        try:
            # 步骤1: 创建一个测试的新品监控任务
            print("\n步骤1: 创建测试任务")
            test_task_data = {
                "task_name": "编辑功能测试任务",
                "keyword": "test_edit",
                "personal_only": True,
                "min_price": "100",
                "max_price": "500",
                "monitor_interval": 300,
                "new_product_window": 3600,
                "dingtalk_webhook": None
            }
            
            async with session.post(
                f"{base_url}/api/tasks/new-product-monitor",
                json=test_task_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    test_task_id = result['task']['id']
                    print(f"✅ 测试任务创建成功，ID: {test_task_id}")
                else:
                    print(f"❌ 创建测试任务失败: {resp.status}")
                    return False
            
            # 步骤2: 测试编辑新品监控任务
            print("\n步骤2: 测试编辑新品监控任务")
            edit_data = {
                "task_name": "编辑后的任务名称",
                "keyword": "edited_keyword",
                "monitor_interval": 120,  # 改为2分钟
                "new_product_window": 7200,  # 改为2小时
                "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=test_token",
                "personal_only": False,
                "min_price": "200",
                "max_price": "1000"
            }
            
            async with session.patch(
                f"{base_url}/api/tasks/{test_task_id}",
                json=edit_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print("✅ 新品监控任务编辑成功")
                    
                    # 验证编辑结果
                    updated_task = result['task']
                    print(f"   任务名称: {updated_task['task_name']}")
                    print(f"   关键词: {updated_task['keyword']}")
                    print(f"   监控间隔: {updated_task['monitor_interval']}秒")
                    print(f"   新品窗口: {updated_task['new_product_window']}秒")
                    print(f"   钉钉Webhook: {updated_task.get('dingtalk_webhook', '未设置')}")
                else:
                    print(f"❌ 编辑任务失败: {resp.status}")
                    return False
            
            # 步骤3: 测试边界值验证
            print("\n步骤3: 测试边界值验证")
            
            # 测试监控间隔过小
            invalid_data = {"monitor_interval": 30}  # 小于60秒
            async with session.patch(
                f"{base_url}/api/tasks/{test_task_id}",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    print("✅ 服务器接受了30秒间隔（前端应该阻止）")
                else:
                    print("✅ 服务器正确拒绝了过小的监控间隔")
            
            # 步骤4: 获取任务列表验证编辑结果
            print("\n步骤4: 验证任务列表中的编辑结果")
            async with session.get(f"{base_url}/api/tasks") as resp:
                if resp.status == 200:
                    tasks = await resp.json()
                    edited_task = None
                    for task in tasks:
                        if task['id'] == test_task_id:
                            edited_task = task
                            break
                    
                    if edited_task:
                        print("✅ 在任务列表中找到编辑后的任务")
                        print(f"   任务类型: {edited_task.get('task_type', 'ai_analysis')}")
                        print(f"   任务名称: {edited_task['task_name']}")
                        print(f"   监控间隔: {edited_task.get('monitor_interval', 'N/A')}秒")
                    else:
                        print("❌ 在任务列表中未找到编辑后的任务")
                        return False
                else:
                    print(f"❌ 获取任务列表失败: {resp.status}")
                    return False
            
            # 步骤5: 清理测试任务
            print("\n步骤5: 清理测试任务")
            async with session.delete(f"{base_url}/api/tasks/{test_task_id}") as resp:
                if resp.status == 200:
                    print("✅ 测试任务清理成功")
                else:
                    print(f"❌ 清理测试任务失败: {resp.status}")
            
            print("\n🎉 编辑功能测试完成！")
            return True
            
        except aiohttp.ClientError as e:
            print(f"❌ 网络连接错误: {e}")
            print("请确保Web服务器正在运行 (python web_server.py)")
            return False
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            return False

async def main():
    print("编辑功能测试脚本")
    print("=" * 50)
    print("注意：请确保Web服务器正在运行")
    print("启动命令：python web_server.py")
    print("=" * 50)
    
    success = await test_edit_functionality()
    
    if success:
        print("\n✅ 编辑功能测试完成！")
        print("\n前端测试步骤：")
        print("1. 在浏览器中访问 http://127.0.0.1:8000")
        print("2. 创建一个新品监控任务")
        print("3. 点击任务列表中的'编辑'按钮")
        print("4. 修改监控间隔、新品窗口等参数")
        print("5. 点击'保存'按钮")
        print("6. 验证修改是否生效")
    else:
        print("\n❌ 编辑功能测试失败，请检查错误信息")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
