#!/usr/bin/env python3
"""
钉钉通知功能测试脚本
用于验证钉钉机器人通知是否正常工作
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# 导入spider_v2中的钉钉通知函数
sys.path.append('.')
from spider_v2 import send_dingtalk_notification

# 加载环境变量
load_dotenv()

async def test_dingtalk_notification():
    """测试钉钉通知功能"""
    
    # 测试商品数据
    test_product = {
        '商品标题': 'nerf iPhone 15 Pro Max 256GB 深空黑色',
        '当前售价': '¥7999',
        '卖家昵称': '测试卖家',
        '发货地区': '北京',
        '发布时间': '2024-01-15 14:30',
        '商品链接': 'https://www.goofish.com/item?id=123456789'
    }
    
    # 从环境变量获取钉钉webhook
    webhook_url = os.getenv("DINGTALK_WEBHOOK")
    
    if not webhook_url or "your_access_token" in webhook_url:
        print("错误：请在.env文件中配置正确的DINGTALK_WEBHOOK")
        print("格式：DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=b5b5b7bce6bc5bac5d766cbbdab7f9c3e4888297706b351ff31f367150f66eef")
        return False
    
    print("开始测试钉钉通知功能...")
    print(f"Webhook URL: {webhook_url}")
    print(f"测试商品: {test_product['商品标题']}")
    
    try:
        # 测试markdown格式
        print("\n测试1: Markdown格式通知")
        await send_dingtalk_notification(
            test_product, 
            reason="nerf这是一个测试通知", 
            webhook_url=webhook_url,
            msg_type="markdown"
        )
        print("✅ Markdown格式通知发送成功")
        
        # 等待一下再发送下一个
        await asyncio.sleep(2)
        
        # 测试文本格式
        print("\n测试2: 文本格式通知")
        await send_dingtalk_notification(
            test_product, 
            reason="nerf这是一个文本格式测试通知", 
            webhook_url=webhook_url,
            msg_type="text"
        )
        print("✅ 文本格式通知发送成功")
        
        print("\n🎉 所有测试通过！钉钉通知功能正常工作。")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_dingtalk_notification())
    sys.exit(0 if success else 1)
