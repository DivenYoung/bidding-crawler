"""关键字匹配器单元测试"""
import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

from data.matcher import KeywordMatcher


def test_keyword_matcher_basic():
    """测试基本关键字匹配"""
    matcher = KeywordMatcher(["广告", "标识"])
    text = "本项目需要制作户外广告牌和标识系统"
    result = matcher.match(text)
    assert set(result) == {"广告", "标识"}


def test_keyword_matcher_single():
    """测试单个关键字匹配"""
    matcher = KeywordMatcher(["广告", "标识", "宣传"])
    text = "本项目为宣传栏采购"
    result = matcher.match(text)
    assert result == ["宣传"]


def test_keyword_matcher_no_match():
    """测试无匹配情况"""
    matcher = KeywordMatcher(["广告", "标识"])
    text = "本项目为道路施工工程"
    result = matcher.match(text)
    assert result == []


def test_keyword_matcher_empty_text():
    """测试空文本"""
    matcher = KeywordMatcher(["广告", "标识"])
    result = matcher.match("")
    assert result == []


def test_is_relevant_true():
    """测试项目相关性判断（相关）"""
    matcher = KeywordMatcher(["广告", "标识"])
    item = {
        "title": "某市广告牌采购项目",
        "content": "详细内容..."
    }
    assert matcher.is_relevant(item) == True


def test_is_relevant_false():
    """测试项目相关性判断（不相关）"""
    matcher = KeywordMatcher(["广告", "标识"])
    item = {
        "title": "某市道路施工项目",
        "content": "详细内容..."
    }
    assert matcher.is_relevant(item) == False
