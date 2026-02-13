#!/usr/bin/env python3
"""
FreeXCraft 服务器自动续期脚本
每小时自动访问续期页面并点击续期按钮
"""

import asyncio
import logging
from datetime import datetime
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('renewal.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置信息
URL = "https://freexcraft.com/external-renew"
SUBDOMAIN = "laohu.xmania.me"
TIMEOUT = 30000  # 30秒超时


async def renew_server():
    """执行服务器续期操作"""
    logger.info("="*60)
    logger.info(f"开始执行服务器续期 - {datetime.now()}")
    logger.info("="*60)
    
    try:
        async with async_playwright() as p:
            # 启动浏览器（无头模式）
            logger.info("正在启动浏览器...")
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # 创建新页面
            page = await browser.new_page()
            
            # 设置超时时间
            page.set_default_timeout(TIMEOUT)
            
            # 访问续期页面
            logger.info(f"正在访问 {URL}")
            await page.goto(URL, wait_until="networkidle")
            logger.info("页面加载完成")
            
            # 等待输入框出现
            logger.info("正在等待输入框...")
            await page.wait_for_selector('input[type="text"]', state="visible")
            
            # 填写子域名
            logger.info(f"正在填写子域名: {SUBDOMAIN}")
            await page.fill('input[type="text"]', SUBDOMAIN)
            logger.info("子域名填写完成")
            
            # 等待一下让页面处理
            await page.wait_for_timeout(1000)
            
            # 点击 "Renew & Start" 按钮
            logger.info("正在点击 Renew & Start 按钮...")
            
            # 尝试多种选择器来找到按钮
            button_clicked = False
            selectors = [
                'button:has-text("Renew & Start")',
                'button:has-text("Renew")',
                'button[type="submit"]',
                '.btn:has-text("Renew")',
            ]
            
            for selector in selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        await button.click()
                        button_clicked = True
                        logger.info(f"成功点击按钮（选择器: {selector}）")
                        break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败: {e}")
                    continue
            
            if not button_clicked:
                logger.warning("未找到按钮，尝试使用坐标点击...")
                # 如果找不到按钮，尝试点击页面中心偏下的位置（按钮通常在那里）
                await page.mouse.click(715, 635)
                logger.info("已执行坐标点击")
            
            # 等待响应
            await page.wait_for_timeout(3000)
            
            # 检查是否有成功消息
            success_messages = [
                "Server renewed",
                "already running",
                "renewed, but the server is already running"
            ]
            
            page_content = await page.content()
            success = any(msg.lower() in page_content.lower() for msg in success_messages)
            
            if success:
                logger.info("✓ 续期成功！服务器已续期并启动")
            else:
                # 截图保存状态
                screenshot_path = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                await page.screenshot(path=screenshot_path)
                logger.warning(f"无法确认续期状态，已保存截图: {screenshot_path}")
            
            # 关闭浏览器
            await browser.close()
            logger.info("浏览器已关闭")
            
            return success
            
    except Exception as e:
        logger.error(f"续期过程出错: {str(e)}", exc_info=True)
        return False


async def main():
    """主函数"""
    try:
        success = await renew_server()
        
        if success:
            logger.info("="*60)
            logger.info("续期任务完成 ✓")
            logger.info("="*60)
        else:
            logger.warning("="*60)
            logger.warning("续期任务完成，但状态未确认")
            logger.warning("="*60)
            
    except Exception as e:
        logger.error(f"主程序错误: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
