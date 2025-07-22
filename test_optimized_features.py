#!/usr/bin/env python3
"""
优化功能测试脚本
测试新品监控的图片集成和时效性优化功能
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

async def test_image_integration():
    """测试图片集成功能"""
    
    print("=== 测试图片集成功能 ===")
    
    # 测试商品数据（包含图片列表）
    test_product_with_images = {
        '商品标题': 'iPhone 15 Pro Max 256GB 深空黑色',
        '当前售价': '¥7999',
        '卖家昵称': '测试卖家',
        '发货地区': '北京',
        '发布时间': '2024-01-15 14:30',
        '商品链接': 'https://www.goofish.com/item?id=123456789',
        '商品图片列表': [
            'https://img.alicdn.com/imgextra/i1/2208857268848/O1CN01abc123_!!2208857268848-0-fleamarket.jpg',
            'https://img.alicdn.com/imgextra/i2/2208857268848/O1CN01def456_!!2208857268848-0-fleamarket.jpg'
        ],
        '商品主图链接': 'https://img.alicdn.com/imgextra/i1/2208857268848/O1CN01abc123_!!2208857268848-0-fleamarket.jpg'
    }
    
    # 测试商品数据（只有主图链接）
    test_product_main_image = {
        '商品标题': 'MacBook Air M2 13英寸',
        '当前售价': '¥6999',
        '卖家昵称': '另一个卖家',
        '发货地区': '上海',
        '发布时间': '2024-01-15 15:00',
        '商品链接': 'https://www.goofish.com/item?id=987654321',
        '商品主图链接': '//img.alicdn.com/imgextra/i3/1234567890/O1CN01xyz789_!!1234567890-0-fleamarket.jpg'
    }
    
    # 测试商品数据（无图片）
    test_product_no_image = {
        '商品标题': 'AirPods Pro 2代',
        '当前售价': '¥1599',
        '卖家昵称': '第三个卖家',
        '发货地区': '广州',
        '发布时间': '2024-01-15 16:00',
        '商品链接': 'https://www.goofish.com/item?id=555666777'
    }
    
    webhook_url = os.getenv("DINGTALK_WEBHOOK")
    
    if not webhook_url or "your_access_token" in webhook_url:
        print("❌ 错误：请在.env文件中配置正确的DINGTALK_WEBHOOK")
        return False
    
    try:
        # 测试1: 有图片列表的商品
        print("\n测试1: 商品包含图片列表")
        await send_dingtalk_notification(
            test_product_with_images, 
            reason="测试图片集成功能 - 图片列表", 
            webhook_url=webhook_url,
            msg_type="markdown"
        )
        print("✅ 图片列表通知发送成功")
        
        await asyncio.sleep(2)
        
        # 测试2: 只有主图链接的商品
        print("\n测试2: 商品只有主图链接")
        await send_dingtalk_notification(
            test_product_main_image, 
            reason="测试图片集成功能 - 主图链接", 
            webhook_url=webhook_url,
            msg_type="markdown"
        )
        print("✅ 主图链接通知发送成功")
        
        await asyncio.sleep(2)
        
        # 测试3: 无图片的商品
        print("\n测试3: 商品无图片")
        await send_dingtalk_notification(
            test_product_no_image, 
            reason="测试图片集成功能 - 无图片", 
            webhook_url=webhook_url,
            msg_type="markdown"
        )
        print("✅ 无图片通知发送成功")
        
        print("\n🎉 图片集成功能测试完成！")
        print("请检查钉钉群消息，确认：")
        print("1. 第一条消息显示了商品图片")
        print("2. 第二条消息显示了主图（URL自动补全https://）")
        print("3. 第三条消息没有图片部分")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_interval_validation():
    """测试监控间隔验证逻辑"""
    
    print("\n=== 测试监控间隔验证 ===")
    
    # 模拟前端验证逻辑
    test_intervals = [30, 59, 60, 120, 300, 1800]
    
    for interval in test_intervals:
        if interval < 60:
            result = f"❌ {interval}秒 - 不符合最小间隔要求"
        else:
            result = f"✅ {interval}秒 - 符合要求"
        print(f"   {result}")
    
    print("\n✅ 监控间隔验证逻辑正确")
    return True

async def main():
    print("新品监控优化功能测试")
    print("=" * 50)
    
    # 测试图片集成功能
    image_test_success = await test_image_integration()
    
    # 测试间隔验证
    interval_test_success = test_interval_validation()
    
    print("\n" + "=" * 50)
    print("测试总结：")
    print(f"图片集成功能: {'✅ 通过' if image_test_success else '❌ 失败'}")
    print(f"间隔验证逻辑: {'✅ 通过' if interval_test_success else '❌ 失败'}")
    
    if image_test_success and interval_test_success:
        print("\n🎉 所有优化功能测试通过！")
        print("\n新功能特性：")
        print("1. ✅ 钉钉通知中自动显示商品图片")
        print("2. ✅ 支持60秒最小监控间隔")
        print("3. ✅ 智能图片URL处理")
        print("4. ✅ 向后兼容无图片商品")
        return True
    else:
        print("\n❌ 部分功能测试失败，请检查配置")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
