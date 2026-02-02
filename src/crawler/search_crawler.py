"""采招网搜索爬虫 - 真实实现（改进版）"""
import time
import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser
import structlog

logger = structlog.get_logger()


class CrawlerConfig:
    """爬虫配置"""
    def __init__(self, min_delay=2.0, max_delay=5.0, max_retries=3):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_retries = max_retries


class SearchCrawler:
    """采招网搜索爬虫"""
    
    BASE_URL = "https://search.bidcenter.com.cn/search"
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, keywords: List[str], config: CrawlerConfig):
        """
        初始化爬虫
        
        Args:
            keywords: 搜索关键字列表
            config: 爬虫配置
        """
        self.keywords = keywords
        self.config = config
        self.playwright = None
        self.browser = None
    
    def _get_random_user_agent(self) -> str:
        """返回随机 User-Agent"""
        return random.choice(self.USER_AGENTS)
    
    def _get_delay(self) -> float:
        """返回随机延迟时间"""
        return random.uniform(self.config.min_delay, self.config.max_delay)
    
    def _init_browser(self):
        """初始化浏览器"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            
            # 使用更真实的浏览器配置
            self.browser = self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                ]
            )
            logger.info("browser.initialized")
    
    def _close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
            logger.info("browser.closed")
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        解析日期字符串
        
        Args:
            date_str: 日期字符串
            
        Returns:
            datetime: 解析后的日期
        """
        if not date_str:
            return None
        
        try:
            date_str = date_str.strip()
            
            # 标准格式 YYYY-MM-DD
            if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                return datetime.strptime(date_str[:10], "%Y-%m-%d")
            
            # 中文格式
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
            if match:
                year, month, day = match.groups()
                return datetime(int(year), int(month), int(day))
                
        except Exception as e:
            logger.warning("date_parse_failed", date_str=date_str, error=str(e))
        
        return None
    
    def parse_markdown_content(self, markdown: str) -> List[Dict]:
        """
        从 Markdown 内容中解析项目列表
        
        Args:
            markdown: 页面提取的 Markdown 内容
            
        Returns:
            List[Dict]: 解析后的项目列表
        """
        items = []
        
        # 按行分割
        lines = markdown.strip().split('\n')
        
        current_item = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测新项目的开始（信息类型 + 标题）
            # 格式: "招标公告 项目标题 (广告,标识在内容中)"
            if any(t in line for t in ['招标公告', '中标结果', '招标变更', '采购信息', '拟在建项目', '拍卖转让']):
                # 保存上一个项目
                if current_item and current_item.get('title'):
                    items.append(current_item)
                
                # 开始新项目
                current_item = {
                    'id': None,
                    'title': '',
                    'info_type': '',
                    'publish_date': None,
                    'province': None,
                    'city': None,
                    'district': None,
                    'owner_unit': None,
                    'budget_amount': None,
                    'procurement_type': None,
                    'bidding_deadline': None,
                    'keywords_matched': [],
                    'project_address': None,
                    'attachments': [],
                    'source_url': ''
                }
                
                # 提取信息类型
                for info_type in ['招标公告', '中标结果', '招标变更', '采购信息', '拟在建项目', '拍卖转让']:
                    if line.startswith(info_type):
                        current_item['info_type'] = info_type
                        # 提取标题（去除信息类型和括号内容）
                        title = line[len(info_type):].strip()
                        # 去除括号内容
                        title = re.sub(r'\s*\([^)]*\)\s*$', '', title)
                        current_item['title'] = title.strip()
                        break
            
            elif current_item:
                # 解析采购预算
                if '采购预算：' in line or '中标金额：' in line:
                    match = re.search(r'[采购预算|中标金额]：(.+?)(?:\s|$)', line)
                    if match:
                        current_item['budget_amount'] = match.group(1).strip()
                
                # 解析采购方式
                if '采购方式：' in line:
                    match = re.search(r'采购方式：(.+?)(?:\s|$)', line)
                    if match:
                        current_item['procurement_type'] = match.group(1).strip()
                
                # 解析截止时间
                if '截止时间：' in line:
                    match = re.search(r'截止时间：(.+?)(?:\s|$)', line)
                    if match:
                        deadline_str = match.group(1).strip()
                        current_item['bidding_deadline'] = self._parse_date(deadline_str)
                
                # 解析地区（单独一行的省份名）
                provinces = ['四川', '北京', '上海', '天津', '重庆', '河北', '山西', '辽宁', '吉林', 
                           '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', 
                           '湖南', '广东', '海南', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', 
                           '内蒙古', '广西', '西藏', '宁夏', '新疆']
                
                if line in provinces:
                    current_item['province'] = line
                
                # 解析日期（YYYY-MM-DD格式）
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})$', line)
                if date_match:
                    current_item['publish_date'] = self._parse_date(date_match.group(1))
        
        # 保存最后一个项目
        if current_item and current_item.get('title'):
            items.append(current_item)
        
        # 生成项目ID和来源URL
        for i, item in enumerate(items):
            if not item['id']:
                # 使用时间戳和索引生成临时ID
                item['id'] = f"temp_{int(datetime.now().timestamp())}_{i}"
            
            if not item['source_url']:
                item['source_url'] = f"{self.BASE_URL}?keywords={','.join(self.keywords)}"
        
        return items
    
    def search_full(
        self, 
        time_range: str = "近三月",
        region: str = "四川",
        info_types: List[str] = None
    ) -> List[Dict]:
        """
        全量搜索（首次执行）
        
        Args:
            time_range: 时间范围
            region: 地区筛选
            info_types: 信息类型列表
            
        Returns:
            List[Dict]: 项目列表
        """
        if info_types is None:
            info_types = ["招标公告"]
        
        logger.info("crawler.search.start", 
                   mode="full", 
                   time_range=time_range, 
                   region=region,
                   keywords=self.keywords)
        
        try:
            self._init_browser()
            
            # 构建搜索关键字
            keywords_str = ",".join(self.keywords)
            
            # 构建搜索URL
            search_url = f"{self.BASE_URL}?keywords={keywords_str}&mod=0"
            
            logger.info("crawler.navigate", url=search_url)
            
            # 创建上下文，添加反检测措施
            context = self.browser.new_context(
                user_agent=self._get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN',
            )
            
            # 添加反检测脚本
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
            """)
            
            page = context.new_page()
            
            # 访问搜索页面
            response = page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            
            logger.info("page.loaded", status=response.status)
            
            # 等待页面加载
            delay = self._get_delay()
            logger.info("waiting", seconds=delay)
            time.sleep(delay)
            
            # 尝试等待搜索结果加载
            try:
                page.wait_for_selector('input[type="checkbox"]', timeout=10000)
                logger.info("search_results.found")
            except:
                logger.warning("search_results.not_found", message="未找到搜索结果，可能触发验证")
            
            # 获取页面内容
            content = page.content()
            
            # 检查是否触发验证
            if '人机验证' in content or 'aliyunCaptcha' in content:
                logger.error("captcha.detected", message="检测到人机验证")
                # 保存HTML用于调试
                with open('/home/ubuntu/bidding-crawler/logs/captcha_page.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                page.close()
                context.close()
                return []
            
            # 使用浏览器工具提取的 Markdown 内容
            # 由于 Playwright 的 page.content() 返回的是完整HTML
            # 我们需要手动提取文本内容
            
            # 简化方案：直接从页面文本提取
            text_content = page.evaluate("""
                () => {
                    return document.body.innerText;
                }
            """)
            
            logger.info("content.extracted", length=len(text_content))
            
            # 解析内容
            items = self.parse_markdown_content(text_content)
            
            # 过滤地区
            if region:
                items = [item for item in items if item.get('province') == region]
            
            page.close()
            context.close()
            
            logger.info("crawler.search.complete", total=len(items))
            return items
            
        except Exception as e:
            logger.error("crawler.search.failed", error=str(e), error_type=type(e).__name__)
            import traceback
            logger.error("traceback", trace=traceback.format_exc())
            return []
        finally:
            self._close_browser()
    
    def search_incremental(
        self,
        region: str = "四川",
        info_types: List[str] = None
    ) -> List[Dict]:
        """
        增量搜索（每日执行）
        
        Args:
            region: 地区筛选
            info_types: 信息类型列表
            
        Returns:
            List[Dict]: 昨日新增的项目列表
        """
        if info_types is None:
            info_types = ["招标公告"]
        
        logger.info("crawler.search.start", 
                   mode="incremental", 
                   region=region,
                   keywords=self.keywords)
        
        # 使用全量搜索，然后过滤昨日数据
        all_items = self.search_full(time_range="近一天", region=region, info_types=info_types)
        
        # 过滤昨日数据
        yesterday = datetime.now() - timedelta(days=1)
        incremental_items = [
            item for item in all_items
            if item.get('publish_date') and item['publish_date'].date() >= yesterday.date()
        ]
        
        logger.info("crawler.search.complete", 
                   total=len(all_items), 
                   incremental=len(incremental_items))
        
        return incremental_items
