#!/usr/bin/env python3
"""
小说评分审核脚本
基于评分审核体系v2.0，对小说文本进行多维度评分审核

用法：
  python score_novel.py --text <文本文件路径> --type <小说类型> --length <篇幅类型>

参数：
  --text     待评分文本文件路径（必填）
  --type     小说类型：scifi/urban/fantasy/xuanhuan/mystery/literary/children/webnovel（默认scifi）
  --length   篇幅类型：short/medium/long（默认short）
  --output   输出报告路径（可选，默认stdout）
  --ai-check 是否执行AI痕迹检测（需要ai-text-detector技能，默认false）

示例：
  python score_novel.py --text my_novel.txt --type scifi --length short
  python score_novel.py --text my_novel.txt --type scifi --length short --ai-check --output report.md
"""

import argparse
import json
import os
import sys

# ============================================================
# 权重配置
# ============================================================

# 按篇幅权重
LENGTH_WEIGHTS = {
    "short": {  # ≤2万字
        "基础表达": 0.20,
        "世界观与设定": 0.15,
        "剧情与结构": 0.30,
        "节奏与氛围": 0.20,
        "角色与人物": 0.15,
    },
    "medium": {  # 2-8万字
        "基础表达": 0.15,
        "世界观与设定": 0.20,
        "剧情与结构": 0.25,
        "节奏与氛围": 0.15,
        "角色与人物": 0.25,
    },
    "long": {  # >8万字
        "基础表达": 0.10,
        "世界观与设定": 0.20,
        "剧情与结构": 0.25,
        "节奏与氛围": 0.15,
        "角色与人物": 0.30,
    },
}

# 按类型权重覆盖
TYPE_WEIGHTS = {
    "scifi": {
        "基础表达": 0.10,
        "世界观与设定": 0.40,
        "剧情与结构": 0.20,
        "节奏与氛围": 0.10,
        "角色与人物": 0.20,
    },
    "urban": {
        "基础表达": 0.15,
        "世界观与设定": 0.10,
        "剧情与结构": 0.25,
        "节奏与氛围": 0.15,
        "角色与人物": 0.35,
    },
    "fantasy": {
        "基础表达": 0.10,
        "世界观与设定": 0.35,
        "剧情与结构": 0.20,
        "节奏与氛围": 0.10,
        "角色与人物": 0.25,
    },
    "xuanhuan": {
        "基础表达": 0.10,
        "世界观与设定": 0.30,
        "剧情与结构": 0.30,
        "节奏与氛围": 0.15,
        "角色与人物": 0.15,
    },
    "mystery": {
        "基础表达": 0.10,
        "世界观与设定": 0.05,
        "剧情与结构": 0.40,
        "节奏与氛围": 0.20,
        "角色与人物": 0.25,
    },
    "literary": {
        "基础表达": 0.30,
        "世界观与设定": 0.10,
        "剧情与结构": 0.15,
        "节奏与氛围": 0.15,
        "角色与人物": 0.30,
    },
    "children": {
        "基础表达": 0.15,
        "世界观与设定": 0.10,
        "剧情与结构": 0.25,
        "节奏与氛围": 0.10,
        "角色与人物": 0.40,
    },
    "webnovel": {
        "基础表达": 0.08,
        "世界观与设定": 0.18,
        "剧情与结构": 0.25,
        "节奏与氛围": 0.12,
        "角色与人物": 0.15,
        "读者体验": 0.12,
        "商业化适配": 0.10,
    },
}

# AI率修正系数
AI_CORRECTION = {
    (0, 15): (0, 2),     # +0~2分
    (15, 25): (0, 0),    # 不修正
    (25, 40): (-5, -2),  # -2~5分
    (40, 60): (-10, -5), # -5~10分
    (60, 101): (-15, -10), # -10~15分
}

# AI率容忍度
AI_TOLERANCE = {
    "scifi": 20,
    "literary": 10,
    "urban": 20,
    "mystery": 15,
    "xuanhuan": 30,
    "fantasy": 25,
    "children": 15,
    "webnovel": 30,
}

# 评分等级
GRADE_TABLE = [
    (90, "卓越", "可直接出版或发表"),
    (80, "优秀", "整体质量良好，局部有微调空间"),
    (70, "良好", "有明显亮点，但存在需要改进的问题"),
    (60, "合格", "基本达到发表标准，需要修改后出版"),
    (50, "需大改", "存在结构性问题，需大幅修订"),
    (0, "不合格", "建议重写或放弃当前方向"),
]


def get_weight(type_key, length_key):
    """获取混合权重（类型权重为主，短篇适度调整）"""
    type_w = TYPE_WEIGHTS.get(type_key, TYPE_WEIGHTS["scifi"])
    length_w = LENGTH_WEIGHTS.get(length_key, LENGTH_WEIGHTS["short"])
    
    # 如果是短篇科幻，取两种权重的中间值
    if type_key == "scifi" and length_key == "short":
        return {
            "基础表达": 0.15,
            "世界观与设定": 0.35,
            "剧情与结构": 0.25,
            "节奏与氛围": 0.10,
            "角色与人物": 0.15,
        }
    
    return type_w


def get_grade(score):
    """根据分数获取等级"""
    for threshold, grade, desc in GRADE_TABLE:
        if score >= threshold:
            return grade, desc
    return "不合格", "建议重写或放弃当前方向"


def get_ai_correction(ai_rate):
    """根据AI率获取修正系数"""
    for (low, high), (correction_low, correction_high) in AI_CORRECTION.items():
        if low <= ai_rate < high:
            if correction_low <= 0 <= correction_high:
                return 0
            return correction_high if correction_high > 0 else correction_low
    return 0


def calculate_score(dimension_scores, weights, ai_rate=None):
    """计算加权总分"""
    total = sum(dimension_scores.get(dim, 0) * weight for dim, weight in weights.items())
    
    correction = 0
    if ai_rate is not None:
        correction = get_ai_correction(ai_rate)
    
    final = max(0, min(100, total + correction))
    return total, correction, final


def generate_report(dimension_scores, sub_scores, weights, ai_rate, ai_details,
                    type_key, length_key, novel_name, word_count):
    """生成评分报告"""
    total, correction, final = calculate_score(dimension_scores, weights, ai_rate)
    grade, grade_desc = get_grade(final)
    tolerance = AI_TOLERANCE.get(type_key, 20)
    
    type_names = {
        "scifi": "科幻", "urban": "都市", "fantasy": "奇幻",
        "xuanhuan": "玄幻", "mystery": "悬疑推理", "literary": "纯文学",
        "children": "儿童文学", "webnovel": "网络小说",
    }
    length_names = {"short": "短篇(≤2万字)", "medium": "中篇(2-8万字)", "long": "长篇(>8万字)"}
    
    lines = []
    lines.append(f"# 《{novel_name}》评分报告")
    lines.append("")
    lines.append(f"> 评分依据：小说评分审核体系 v2.0 · {type_names.get(type_key, type_key)}{length_names.get(length_key, length_key)}权重")
    lines.append(f"> 评分时间：{__import__('datetime').datetime.now().strftime('%Y年%m月')}")
    lines.append(f"> 正文字数：约{word_count}字")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 维度评分表
    lines.append("## 评分总览")
    lines.append("")
    lines.append("| 维度 | 权重 | 得分 | 加权分 |")
    lines.append("|------|------|------|--------|")
    for dim, weight in weights.items():
        score = dimension_scores.get(dim, 0)
        weighted = score * weight
        lines.append(f"| {dim} | {weight:.0%} | {score} | {weighted:.2f} |")
    lines.append(f"| **文学加权总分** | **100%** | **—** | **{total:.2f}** |")
    
    if ai_rate is not None:
        lines.append(f"| AI修正系数 | — | {correction:+d} | {correction} |")
        lines.append(f"| **最终得分** | — | **—** | **{final:.1f}** |")
    else:
        lines.append(f"| **最终得分** | — | **—** | **{total:.1f}** |")
    
    lines.append("")
    lines.append(f"**等级：{grade}**（{grade_desc}）")
    lines.append("")
    
    # AI痕迹检测
    if ai_rate is not None:
        lines.append("---")
        lines.append("")
        lines.append("## AI痕迹检测报告【v2.0】")
        lines.append("")
        lines.append("| 指标 | 数值 | 评价 |")
        lines.append("|------|------|------|")
        ai_grade = "极低" if ai_rate < 10 else "低" if ai_rate < 20 else "轻度" if ai_rate < 30 else "中度" if ai_rate < 45 else "较重" if ai_rate < 60 else "严重"
        lines.append(f"| 整体AI率 | {ai_rate:.1f}% | {ai_grade}AI痕迹 |")
        lines.append(f"| 硬科幻警戒线 | {tolerance}% | {'✅ 通过' if ai_rate <= tolerance else '⚠️ 超标'} |")
        lines.append(f"| 修正系数 | {correction:+d} | {'安全区间' if correction == 0 else '需修正'} |")
        
        if ai_details:
            lines.append("")
            for key, value in ai_details.items():
                lines.append(f"| {key} | {value} | — |")
        lines.append("")
    
    # 子项评分
    if sub_scores:
        lines.append("---")
        lines.append("")
        lines.append("## 分项评分明细")
        lines.append("")
        for dim, subs in sub_scores.items():
            lines.append(f"### {dim}")
            lines.append("")
            lines.append("| 子项 | 得分 | 说明 |")
            lines.append("|------|------|------|")
            for sub_name, (sub_score, sub_note) in subs.items():
                lines.append(f"| {sub_name} | {sub_score} | {sub_note} |")
            lines.append("")
    
    # 建议
    lines.append("---")
    lines.append("")
    lines.append("## 总体建议")
    lines.append("")
    lines.append(f"**最终得分**：{final:.1f}分")
    lines.append(f"**等级**：{grade}")
    lines.append("")
    
    if final >= 90:
        lines.append("**推荐动作：直接出版/发表**")
    elif final >= 80:
        lines.append("**推荐动作：轻微润色后出版**")
    elif final >= 70:
        lines.append("**推荐动作：修改后出版**")
    elif final >= 60:
        lines.append("**推荐动作：大幅修改后考虑出版**")
    else:
        lines.append("**推荐动作：建议大改或重写**")
    
    lines.append("")
    lines.append("---")
    lines.append(f"*评分体系版本：v2.0*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="小说评分审核脚本 v2.0")
    parser.add_argument("--text", required=True, help="待评分文本文件路径")
    parser.add_argument("--type", default="scifi", 
                       choices=["scifi", "urban", "fantasy", "xuanhuan", "mystery", "literary", "children", "webnovel"],
                       help="小说类型")
    parser.add_argument("--length", default="short",
                       choices=["short", "medium", "long"],
                       help="篇幅类型")
    parser.add_argument("--output", help="输出报告路径")
    parser.add_argument("--ai-check", action="store_true", help="是否执行AI痕迹检测")
    parser.add_argument("--name", default="未命名作品", help="作品名称")
    
    # 支持直接传入维度分数
    parser.add_argument("--scores", help="维度分数JSON，格式: {\"基础表达\":95,\"世界观与设定\":97,...}")
    parser.add_argument("--sub-scores", help="子项分数JSON文件路径")
    parser.add_argument("--ai-rate", type=float, help="AI率（如果已检测）")
    parser.add_argument("--ai-details", help="AI检测详情JSON")
    parser.add_argument("--word-count", type=int, default=0, help="字数")
    
    args = parser.parse_args()
    
    # 读取文本
    if not os.path.exists(args.text):
        print(f"错误：文件不存在 {args.text}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.text, "r", encoding="utf-8") as f:
        text = f.read()
    
    word_count = args.word_count or len(text)
    
    # 获取权重
    weights = get_weight(args.type, args.length)
    
    # 解析维度分数
    dimension_scores = {}
    if args.scores:
        dimension_scores = json.loads(args.scores)
    
    # 解析子项分数
    sub_scores = {}
    if args.sub_scores and os.path.exists(args.sub_scores):
        with open(args.sub_scores, "r", encoding="utf-8") as f:
            sub_scores = json.load(f)
    
    # AI检测
    ai_rate = args.ai_rate
    ai_details = {}
    if args.ai_details:
        ai_details = json.loads(args.ai_details)
    
    # 生成报告
    report = generate_report(
        dimension_scores=dimension_scores,
        sub_scores=sub_scores,
        weights=weights,
        ai_rate=ai_rate,
        ai_details=ai_details,
        type_key=args.type,
        length_key=args.length,
        novel_name=args.name,
        word_count=word_count,
    )
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已保存至：{args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
