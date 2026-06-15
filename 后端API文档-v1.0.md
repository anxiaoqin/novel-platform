# 十方书社 · 后端API完整文档

基于现有代码自动生成 | 2026-06-15

- 服务地址：http://103.217.187.186:8001
- 所有API前缀：/api/v1
- 认证方式：Bearer Token（Authorization: Bearer \<token\>）

---

## 目录

1. 认证模块
2. 用户模块
3. 积分模块
4. 作品模块
5. 章节模块
6. 世界观设定模块
7. 角色设定模块 🆕扩展
8. 时间线模块
9. AI写作模块
10. AI纠错模块 🆕6维增强
11. AI事件分析模块 🆕增强
12. 大纲管理模块 🆕多级+版本
13. 正文填充模块 🆕增强
14. 续写模块 🆕增强
15. 去AI味模块 🆕增强
16. 流式输出模块 🆕
17. 知识库模块 🆕
18. 写作DNA模块 🆕
19. 章节版本管理模块 🆕
20. 创作引擎模块 🆕
21. 发布模块
22. 封面模块
23. 其他模块

---

## 1. 认证模块

### POST /api/v1/auth/register
注册新用户。
```json
// Request
{ "username": "xxx", "password": "xxx", "email": "xxx" }
// Response
{ "message": "注册成功", "token": "jwt..." }
```

### POST /api/v1/auth/login
登录获取Token。
```json
// Request
{ "username": "xxx", "password": "xxx" }
// Response
{ "message": "Login successful", "token": "jwt...", "user": {...} }
```

---

## 2. 用户模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/users/settings | 获取用户设置 🔒 |
| PUT | /api/v1/users/settings | 更新用户设置 🔒 |
| GET | /api/v1/users/credits | 获取用户积分余额（兼容路径）🔒 |
| GET | /api/v1/users/me/writing-stats | 获取用户写作统计 🔒 |

---

## 3. 积分模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/credits/balance | 获取积分余额 🔒 |
| GET | /api/v1/credits/history | 获取积分历史记录 🔒 |
| POST | /api/v1/credits/signin | 每日签到领积分 🔒 |
| POST | /api/v1/credits/add | 管理员加积分 |
| POST | /api/v1/credits/set-vip | 设置VIP状态 |
| GET | /api/v1/credits/usage/daily | 获取每日使用统计 🔒 |

---

## 4. 作品模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/novels | 获取用户作品列表 🔒 |
| POST | /api/v1/novels | 创建新作品 🔒 |
| GET | /api/v1/novels/:id | 获取作品详情 🔒 |
| PUT | /api/v1/novels/:id | 更新作品信息 🔒 |
| DELETE | /api/v1/novels/:id | 删除作品 🔒 |
| GET | /api/v1/novels/:id/stats | 获取作品统计 🔒 |

创建作品请求：
```json
{ "title": "小说名", "genre": "玄幻", "description": "简介", "writing_style": "风格", "core_idea": "核心创意" }
```

---

## 5. 章节模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/novels/:novel_id/chapters | 获取章节列表 🔒 |
| POST | /api/v1/novels/:novel_id/chapters | 创建新章节 🔒 |
| GET | /api/v1/chapters/:id | 获取章节详情 🔒 |
| PUT | /api/v1/chapters/:id | 更新章节 🔒 |
| DELETE | /api/v1/chapters/:id | 删除章节 🔒 |

创建章节请求：
```json
{ "title": "第一章", "content": "正文...", "order": 1 }
```

---

## 6. 世界观设定模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/novels/:novel_id/worlds | 获取世界观列表 🔒 |
| POST | /api/v1/novels/:novel_id/worlds | 创建世界观设定 🔒 |
| GET | /api/v1/novels/:novel_id/worlds/:world_id | 获取世界观详情 🔒 |
| PUT | /api/v1/novels/:novel_id/worlds/:world_id | 更新世界观设定 🔒 |
| DELETE | /api/v1/novels/:novel_id/worlds/:world_id | 删除世界观设定 🔒 |

创建世界观请求：
```json
{ "name": "修仙界", "description": "以灵气为根基的世界", "category": "rules" }
// category可选: rules(规则)/geography(地理)/history(历史)/culture(文化)
```

---

## 7. 角色设定模块 🆕扩展

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/novels/:novel_id/characters | 获取角色列表 🔒 |
| POST | /api/v1/novels/:novel_id/characters | 创建角色 🔒 |
| GET | /api/v1/novels/:novel_id/characters/:character_id | 获取角色详情 🔒 |
| PUT | /api/v1/novels/:novel_id/characters/:character_id | 更新角色 🔒 |
| DELETE | /api/v1/novels/:novel_id/characters/:character_id | 删除角色 🔒 |
| GET | /api/v1/novels/:novel_id/character-relationships 🆕 | 获取角色关系图谱 🔒 |
| PUT | /api/v1/characters/:character_id/relationships 🆕 | 更新角色关系 🔒 |
| PUT | /api/v1/characters/:character_id/growth-line 🆕 | 更新角色成长线 🔒 |
| POST | /api/v1/novels/:novel_id/characters/batch-query 🆕 | 批量查询角色 🔒 |

创建角色请求：
```json
{
  "name": "赵无极", "description": "外门弟子", "role_type": "protagonist",
  "appearance": "身材修长", "abilities": "御剑术",
  "background": "宗门覆灭的幸存者",
  "relationships": [{"target_id": 2, "relation": "师妹", "target_name": "苏晴"}],
  "growth_line": [{"chapter": 1, "event": "觉醒", "description": "..."}],
  "classic_quotes": ["我命由我不由天"],
  "tags": ["傲娇", "天才"]
}
```

角色关系图谱响应：
```json
{
  "success": true,
  "data": {
    "relationships": [
      { "source_id": 1, "source_name": "赵无极", "target_id": 2, "target_name": "苏晴", "relation": "师妹" }
    ],
    "character_count": 5
  }
}
```

批量查询请求：
```json
{ "character_ids": [1, 2, 3] }
// 不传则返回全部
```

---

## 8. 时间线模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/novels/:novel_id/timelines | 获取时间线列表 🔒 |
| POST | /api/v1/novels/:novel_id/timelines | 创建时间线条目 🔒 |
| PUT | /api/v1/novels/:novel_id/timelines/:timeline_id | 更新时间线 🔒 |
| DELETE | /api/v1/novels/:novel_id/timelines/:timeline_id | 删除时间线 🔒 |

---

## 9. AI写作模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/ai/modes | 获取AI写作模式列表 |
| POST | /api/v1/ai/generate | 通用AI生成 🔒 |
| POST | /api/v1/ai/write | AI写作（指定模式）🔒 |
| POST | /api/v1/ai/write/apply | 应用AI写作结果 🔒 |
| POST | /api/v1/ai/chat | AI对话 🔒 |
| POST | /api/v1/ai/chat/stream | AI对话（流式）🔒 |
| GET | /api/v1/ai/config | 获取AI配置 🔒 |
| GET | /api/v1/ai/models/pricing | 获取模型定价 |
| GET | /api/v1/ai/models/current | 获取当前使用模型 🔒 |
| POST | /api/v1/ai/models/refresh-pricing | 刷新模型定价 🔒 |
| POST | /api/v1/ai/models/override | 覆盖模型选择 🔒 |
| POST | /api/v1/ai/models/init | 初始化模型配置 |

---

## 10. AI纠错模块 🆕6维增强

### POST /api/v1/ai/proofread
基础AI纠错（语法/逻辑/风格）🔒

### POST /api/v1/ai/novel-check 🆕
网文专属6维纠错 🔒
```json
// Request
{
  "content": "待检查文本...",
  "novel_id": 1,       // 可选：传入后自动加载角色/世界观上下文
  "chapter_id": 1,     // 可选：传入后加载前文用于时间线/名词对照
  "dimensions": ["character", "redundancy", "basic"]  // 可选：指定维度，不传则全部6维
}
// Response
{
  "success": true,
  "data": {
    "dimensions": {
      "character": { "issues": [...], "score": 80 },
      "terminology": { "issues": [...], "score": 90 },
      "timeline": { "issues": [...], "score": 100 },
      "power_level": { "issues": [...], "score": 60 },
      "redundancy": { "issues": [...], "score": 85 },
      "basic": { "issues": [...], "score": 100 }
    },
    "overall_score": 75,
    "summary": "整体评价"
  }
}
```

### GET /api/v1/ai/novel-check/dimensions 🆕
获取6维检查维度说明
```json
{
  "success": true,
  "data": {
    "character": { "name": "人设一致性", "desc": "...", "icon": "👤" },
    "terminology": { "name": "名词一致性", "desc": "...", "icon": "📖" },
    "timeline": { "name": "时间线一致性", "desc": "...", "icon": "⏰" },
    "power_level": { "name": "战力体系一致性", "desc": "...", "icon": "⚔️" },
    "redundancy": { "name": "冗余检测", "desc": "...", "icon": "✂️" },
    "basic": { "name": "基础纠错", "desc": "...", "icon": "✏️" }
  }
}
```

### POST /api/v1/ai/check-errors
前端兼容路径（简化纠错）🔒

### POST /api/v1/ai/analyze-chapter
AI章节分析 🔒

---

## 11. AI事件分析模块 🆕增强

### POST /api/v1/ai/analyze-paragraph
分析段落提取元素+生成事件建议 🔒
```json
// Request
{
  "paragraph": "待分析段落...",
  "novel_id": 1,           // 可选：自动加载上下文
  "context_mode": "auto",  // auto/manual
  "max_suggestions": 5,    // 3-8
  "granularity": "scene"   // chapter/scene/paragraph
}
// Response
{
  "success": true,
  "extracted": {
    "characters": [{"name": "林风", "role": "主角"}],
    "locations": ["云霄宗"],
    "conflicts": ["突破受阻"],
    "emotions": ["紧张"]
  },
  "suggestions": [
    {
      "id": "1", "title": "事件标题",
      "type": "铺垫|冲突|反转|高潮|过渡|收尾",
      "description": "...", "participants": ["林风"],
      "reasoning": "...", "follow_ups": ["..."]
    }
  ],
  "paragraph_hash": "md5..."
}
```

---

## 12. 大纲管理模块 🆕多级+版本

### POST /api/v1/ai/save-outline-events
保存章节事件大纲（支持多级结构）🔒
```json
// Request
{
  "novel_id": 1, "chapter_id": 1,
  "events": [
    {
      "order": 0,
      "source": "user_created",  // user_created/ai_suggested
      "ai_suggestion_id": null,
      "title": "事件标题", "description": "事件描述",
      "participants": ["角色1"],
      "level": "volume",  // volume/chapter/scene/paragraph
      "parent_id": null,  // 父节点ID（多级结构）
      "sort_order": 0
    }
  ]
}
```

### GET /api/v1/novels/:novel_id/outline-tree 🆕
获取大纲树结构（多级展开）🔒
```json
{
  "success": true,
  "data": {
    "outline": [
      {
        "id": 1, "title": "...", "level": "volume",
        "children": [
          { "id": 2, "title": "...", "level": "chapter", "children": [...] }
        ]
      }
    ],
    "total": 15
  }
}
```

### GET /api/v1/novels/:novel_id/outline-versions
获取大纲版本列表 🔒

### POST /api/v1/novels/:novel_id/outline-versions
保存当前大纲为版本快照 🔒
```json
{ "version_name": "版本1" }
```

### PUT /api/v1/novels/:novel_id/outline-versions/:vid/activate
激活指定大纲版本 🔒
```json
{ "confirm": true }
```

### DELETE /api/v1/novels/:novel_id/outline-versions/:vid
删除大纲版本（不可删除激活版本）🔒

---

## 13. 正文填充模块 🆕增强

### POST /api/v1/ai/fill-chapter
根据事件大纲填充章节正文 🔒
```json
{
  "novel_id": 1, "chapter_id": 1,
  "events": [{"title": "事件1", "description": "...", "participants": [...]}],
  "user_paragraph": "用户已写的段落",
  "style": "古风"  // 可选
}
```

### POST /api/v1/ai/fill-event 🆕
单事件独立填充 🔒
```json
{
  "novel_id": 1, "chapter_id": 1,  // chapter_id可选
  "event_title": "宗门覆灭",
  "event_description": "天魔宗突袭",
  "participants": ["赵无极"],
  "word_count": 800,        // 目标字数
  "rhythm": "normal",       // fast/normal/slow
  "perspective": "third",   // first/third/omniscient
  "writing_style": "古风",  // 可选
  "use_dna": false          // 是否使用写作DNA风格
}
```

### POST /api/v1/ai/fill-chapter/multi 🆕
多候选填充（2-3个版本供选择）🔒
```json
{
  "novel_id": 1, "chapter_id": 1,
  "events": [...], "user_paragraph": "", "writing_style": "",
  "num_candidates": 2,  // 1-3
  "use_dna": false
}
// Response
{
  "success": true,
  "candidates": [
    { "label": "标准版", "content": "...", "word_count": 2000 },
    { "label": "紧凑版", "content": "...", "word_count": 1800 }
  ]
}
```

---

## 14. 续写模块 🆕增强

### POST /api/v1/ai/continue-writing
智能续写（支持方向/视角/字数自定义）🔒
```json
{
  "novel_id": 1, "chapter_id": 1,
  "direction": "auto",   // auto/conflict/emotion/transition/climax/foreshadow
  "perspective": "third", // first/third/omniscient
  "word_count": 1000,    // 200-5000
  "num_candidates": 3    // 1-5
}
// Response
{
  "success": true,
  "candidates": [
    { "style": "标准续写", "content": "..." },
    { "style": "强化转折", "content": "..." },
    { "style": "情感侧重", "content": "..." }
  ]
}
```

---

## 15. 去AI味模块 🆕增强

### POST /api/v1/ai/deai-detect
AI味检测（含改进建议）🔒
```json
// Request
{ "content": "待检测文本..." }
// Response
{
  "success": true, "score": 65,
  "issues": [
    { "type": "排比三连", "text": "...", "reason": "...", "severity": "medium", "suggestion": "改写建议" }
  ],
  "suggestions": [
    { "category": "句式多样性", "description": "减少排比结构", "priority": "high" }
  ],
  "summary": "整体评估"
}
```

### POST /api/v1/ai/deai-rewrite
去AI味改写（三档浓度+内容锁定+相似度评分）🔒
```json
// Request
{
  "content": "待改写文本...",
  "style": "modern",         // modern/classical/colloquial/literary
  "issues": [...],           // 可选：传入检测结果
  "intensity": "medium",     // light/medium/heavy
  "lock_content": false,     // 是否锁定核心内容
  "lock_ranges": [{"start": 0, "end": 50}]  // 具体锁定范围
}
// Response
{
  "success": true,
  "rewritten": "改写后文本...",
  "intensity": "medium",
  "original_length": 500, "rewritten_length": 480,
  "ai_similarity_score": 72.3,  // 与原文的相似度（越低改幅越大）
  "change_ratio": 27.7          // 改动比例
}
```

---

## 16. 流式输出模块 🆕

4个核心API的SSE流式版本，返回格式为text/event-stream。

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/ai/fill-chapter/stream | 流式填充章节 🔒 |
| POST | /api/v1/ai/continue-writing/stream | 流式续写（单候选）🔒 |
| POST | /api/v1/ai/deai-rewrite/stream | 流式去AI味改写 🔒 |
| POST | /api/v1/ai/analyze-paragraph/stream | 流式段落分析 🔒 |

SSE数据格式：
```
data: {"choices":[{"delta":{"content":"生成文本片段"}}]}
data: [DONE]
```

---

## 17. 知识库模块 🆕

### POST /api/v1/ai/knowledge-search
事实知识检索 🔒
```json
// Request
{
  "query": "唐代长安城坊市制度",
  "category": "history"  // auto/history/geography/culture/science/art/music/literature
}
// Response
{
  "success": true,
  "data": {
    "results": [
      {
        "fact": "长安城实行坊市分离制度",
        "confidence": "high",
        "source_type": "历史典籍",
        "source_detail": "《长安志》",
        "relevance": 95
      }
    ],
    "query_domain": "历史",
    "summary": "简明摘要",
    "disclaimer": "使用提醒"
  }
}
```

---

## 18. 写作DNA模块 🆕

### POST /api/v1/ai/writing-dna/analyze
分析用户写作风格生成DNA画像 🔒
```json
// Request
{
  "novel_id": 1,           // 从该作品的章节自动采样
  "sample_texts": ["..."]  // 或直接提供文本样本
}
// Response
{
  "success": true,
  "data": {
    "profile": {
      "sentence_patterns": { "avg_length": "15字", "rhythm": "短长交替" },
      "vocabulary": { "formal_level": "mixed", "fav_words": ["然而", "不禁"] },
      "narrative_style": { "perspective": "第三人称", "dialogue_ratio": "medium" },
      "emotion_tone": { "overall_tone": "热血", "humor_level": "low" },
      "unique_traits": ["习惯用短句制造节奏感", "对话中常带反问"],
      "style_fingerprint": "短句紧凑型热血叙事风格"
    },
    "dna_id": 1
  }
}
```

### GET /api/v1/novels/:novel_id/writing-dna
获取作品写作DNA画像 🔒

---

## 19. 章节版本管理模块 🆕

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/chapters/:chapter_id/versions | 获取章节版本列表 🔒 |
| POST | /api/v1/chapters/:chapter_id/versions | 保存版本快照 🔒 |
| GET | /api/v1/chapter-versions/:version_id | 获取版本详情 🔒 |
| PUT | /api/v1/chapter-versions/:version_id/restore | 恢复到指定版本 🔒 |
| DELETE | /api/v1/chapter-versions/:version_id | 删除版本 🔒 |
| GET | /api/v1/chapter-versions/:v1_id/diff/:v2_id | 对比两个版本差异 🔒 |

保存版本请求：
```json
{ "version_label": "大改前", "source": "manual" }
// source: manual/ai_fill/ai_rewrite/ai_continue
```

版本对比响应：
```json
{
  "success": true,
  "data": {
    "diff": ["--- version-1", "+++ version-2", "-旧文本", "+新文本"],
    "added_lines": 5, "removed_lines": 3,
    "v1_word_count": 2000, "v2_word_count": 2200,
    "v1_label": "auto-save", "v2_label": "大改后"
  }
}
```

---

## 20. 创作引擎模块 🆕

节点式创作引擎，5阶段流程：世界观→角色→事件→大纲→正文

### 项目管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/creation/projects | 获取创作项目列表 🔒 |
| POST | /api/v1/creation/projects | 创建创作项目 🔒 |
| GET | /api/v1/creation/projects/:pid | 获取项目详情 🔒 |
| PUT | /api/v1/creation/projects/:pid | 更新项目 🔒 |
| DELETE | /api/v1/creation/projects/:pid | 删除项目 🔒 |

### 节点操作

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/creation/projects/:pid/nodes?stage=1 | 获取节点列表（可按stage筛选）🔒 |
| POST | /api/v1/creation/projects/:pid/nodes | 创建节点 🔒 |
| GET | /api/v1/creation/projects/:pid/nodes/:nuuid | 获取节点详情 🔒 |
| PUT | /api/v1/creation/projects/:pid/nodes/:nuuid | 更新节点 🔒 |
| DELETE | /api/v1/creation/projects/:pid/nodes/:nuuid | 删除节点 🔒 |

创建节点请求：
```json
{
  "stage": 1,
  "node_type": "world",  // stage1: world/faction/system/rule/item
                          // stage2: protagonist/supporting/antagonist/npc
                          // stage3: cause/turning_point/conflict/growth/emotion/revelation/ending
  "name": "修仙界",
  "data": { "description": "...", "type": "high_fantasy" },
  "ai_generated": false
}
```

### 连接操作

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/creation/projects/:pid/edges | 获取所有连接 🔒 |
| POST | /api/v1/creation/projects/:pid/edges | 创建连接 🔒 |
| DELETE | /api/v1/creation/projects/:pid/edges/:eid | 删除连接 🔒 |

创建连接请求：
```json
{
  "source_uuid": "xxx", "target_uuid": "yyy",
  "edge_type": "derives",  // contains/derives/conflicts/supplements/leads_to/trigger/parallel
  "edge_data": { "description": "..." }
}
```

### 快照

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/creation/projects/:pid/snapshots | 保存阶段快照 🔒 |

```json
{ "stage": 1 }
```

### AI生成

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/creation/ai/generate-from-settings | 从世界观设定自动生成角色 🔒 |
| POST | /api/v1/creation/ai/generate-events | 从角色+设定生成事件因果链 🔒 |
| POST | /api/v1/creation/ai/generate-outline | 从事件生成章节大纲 🔒 |

---

## 21. 发布模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/platforms/accounts | 获取平台账号列表 🔒 |
| POST | /api/v1/platforms/accounts | 添加平台账号 🔒 |
| DELETE | /api/v1/platforms/accounts/:account_id | 删除平台账号 🔒 |
| POST | /api/v1/platforms/accounts/:account_id/verify | 验证平台账号 🔒 |
| GET | /api/v1/publish/preview/:novel_id | 预览发布内容 🔒 |
| POST | /api/v1/publish/:novel_id | 发布小说 🔒 |
| GET | /api/v1/publish/records | 获取发布记录 🔒 |
| GET | /api/v1/publish/records/:record_id | 获取发布记录详情 🔒 |
| GET | /api/v1/publish/check-duplicate/:novel_id | 检查重复发布 🔒 |
| POST | /api/v1/publish/sync-status/:record_id | 同步发布状态 🔒 |
| POST | /api/v1/publish/detect-existing | 检测已有作品 🔒 |
| GET | /api/v1/platforms/:platform/login-url | 获取平台登录URL 🔒 |
| POST | /api/v1/platforms/:platform/save-session | 保存平台会话 🔒 |
| GET | /api/v1/platforms/:platform/check-session | 检查平台会话 🔒 |
| GET | /api/v1/platforms/:platform/load-session | 加载平台会话 🔒 |
| GET | /api/v1/publish/task-data/:novel_id | 获取发布任务数据 🔒 |
| POST | /api/v1/publish/chapter-report | 章节发布报告 🔒 |
| POST | /api/v1/publish/book-created | 书籍创建确认 🔒 |
| GET | /api/v1/publish/existing-works | 获取已有作品列表 🔒 |

---

## 22. 封面模块

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/covers/:novel_id | 获取封面信息 🔒 |
| POST | /api/v1/covers/:novel_id/generate | AI生成封面 🔒 |
| POST | /api/v1/covers/:novel_id/upload | 上传封面 🔒 |

---

## 23. 其他模块

### 道具卡
| 方法 | 路径 |
|------|------|
| GET | /api/v1/novels/:novel_id/item-cards |
| POST | /api/v1/novels/:novel_id/item-cards |
| PUT | /api/v1/item-cards/:id |
| DELETE | /api/v1/item-cards/:id |

### 写作上下文
| 方法 | 路径 |
|------|------|
| GET | /api/v1/novels/:novel_id/writing-context/:chapter_id |

### 时间线AI
| 方法 | 路径 |
|------|------|
| POST | /api/v1/ai/timeline/generate |
| POST | /api/v1/ai/timeline/apply |

### AI创作6步流程（旧版）
| 方法 | 路径 |
|------|------|
| POST | /api/v1/ai/create-framework |
| POST | /api/v1/ai/create-outline |
| POST | /api/v1/ai/write-chapter |
| POST | /api/v1/ai/update-creation-stage |
| POST | /api/v1/ai/update-framework |
| POST | /api/v1/ai/update-outline |

### AI标签
| 方法 | 路径 |
|------|------|
| POST | /api/v1/ai/tags/generate |
| POST | /api/v1/ai/tags/save |
| GET | /api/v1/ai/tags/popular |

### 法务合规
| 方法 | 路径 |
|------|------|
| GET | /api/v1/legal/:doc_type |
| GET | /api/v1/legal/list |
| POST | /api/v1/legal/accept |
| GET | /api/v1/legal/acceptance-status |

### 草稿
| 方法 | 路径 |
|------|------|
| GET/POST | /api/v1/drafts |
| GET/PUT/DELETE | /api/v1/drafts/:id |

### 社区
| 方法 | 路径 |
|------|------|
| GET/POST | /api/v1/posts |
| GET/DELETE | /api/v1/posts/:id |
| POST | /api/v1/posts/:id/like |
| POST | /api/v1/posts/:id/comments |

### 公开
| 方法 | 路径 |
|------|------|
| GET | /api/v1/public/novels |
| GET | /api/v1/public/novels/:id |
| GET | /api/v1/public/rank |

### 统计
| 方法 | 路径 |
|------|------|
| GET | /api/v1/stats/dashboard |

### 设备
| 方法 | 路径 |
|------|------|
| POST | /api/v1/device/report |
| GET | /api/v1/device/sessions |

### 管理后台
| 方法 | 路径 |
|------|------|
| POST | /api/v1/admin/login |
| GET | /api/v1/admin/dashboard |
| GET | /api/v1/admin/users |
| DELETE | /api/v1/admin/users/:user_id |
| GET | /api/v1/admin/users/:user_id/novels |
| GET | /api/v1/admin/novels |
| DELETE | /api/v1/admin/novels/:novel_id |
| GET | /api/v1/admin/tables |
| GET | /api/v1/admin/tables/:table_name |
| POST | /api/v1/admin/init-credits-db |
| GET | /api/v1/admin/credits/users |

---

## 错误码

| HTTP状态码 | 含义 |
|-----------|------|
| 400 | 参数错误 |
| 401 | 未认证（Token缺失或过期） |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务端错误 |

通用错误格式：
```json
{ "error": "错误描述" }
```

通用成功响应：
```json
{ "success": true, "data": {...} }
```

---

文档版本：v1.0 | 生成时间：2026-06-15 | app.py: 9180行, 190个API端点
