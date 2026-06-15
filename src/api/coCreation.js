import api from './index'

/**
 * 人机共创 API 层
 * 后端 API 已就绪，默认对接真实接口
 */

// 是否使用 mock（调试用）
let useMock = false

export function setMockMode(mock) {
  useMock = mock
}

export function isMockMode() {
  return useMock
}

/**
 * Step 2: AI 分析段落，提取事件
 * POST /ai/analyze-paragraph
 * 
 * 真实响应格式：
 * {
 *   success: true,
 *   extracted: { characters: [{name,role}], conflicts: [], emotions: [], locations: [] },
 *   suggestions: [{ id, title, description, type, participants, reasoning, follow_ups }],
 *   paragraph_hash: "..."
 * }
 */
export async function analyzeParagraph(paragraph, novelId, chapterId) {
  if (useMock) {
    await new Promise(resolve => setTimeout(resolve, 1500))
    return {
      success: true,
      extracted: {
        characters: [
          { name: '神秘来客', role: '核心角色/悬念来源' },
          { name: '客栈老板', role: '潜在配角/观察者' }
        ],
        conflicts: ['来客与追捕者之间的对抗', '伤口背后隐藏的秘密'],
        emotions: ['恐惧与警觉', '好奇与警惕'],
        locations: ['深夜的小镇客栈']
      },
      suggestions: [
        { id: 'mock-1', title: '神秘来客', description: '一个陌生人在深夜出现在小镇客栈，身上带着奇怪的伤口', type: '主线', participants: ['神秘来客'], reasoning: '核心悬念事件', follow_ups: [] },
        { id: 'mock-2', title: '隐藏身份', description: '主角发现来客竟是失踪多年的故人', type: '支线', participants: ['神秘来客', '主角'], reasoning: '深化人物关系', follow_ups: [] },
        { id: 'mock-3', title: '午夜密谈', description: '深夜客栈传来低语，来客与一名黑衣人在角落交谈', type: '冲突', participants: ['神秘来客', '黑衣人'], reasoning: '制造冲突', follow_ups: [] },
        { id: 'mock-4', title: '旧日信物', description: '来客手中握着一枚与主角家传之物相同的玉佩', type: '主线', participants: ['神秘来客'], reasoning: '关键线索', follow_ups: [] },
        { id: 'mock-5', title: '追兵将至', description: '镇外传来马蹄声，来客神色骤变', type: '冲突', participants: ['神秘来客'], reasoning: '推动节奏', follow_ups: [] },
        { id: 'mock-6', title: '月下独白', description: '来客独自站在院中仰望月光，喃喃自语', type: '支线', participants: ['神秘来客'], reasoning: '塑造人物', follow_ups: [] },
      ],
      paragraph_hash: 'mock-hash'
    }
  }
  return api.post('/ai/analyze-paragraph', { 
    paragraph, 
    novel_id: novelId, 
    chapter_id: chapterId 
  })
}

/**
 * Step 3: 保存大纲事件
 * POST /ai/save-outline-events
 * 
 * 真实响应格式：
 * { success: true, chapter_id: N, event_count: N }
 */
export async function saveOutlineEvents(novelId, chapterId, events) {
  if (useMock) {
    await new Promise(resolve => setTimeout(resolve, 500))
    return { success: true, chapter_id: chapterId, event_count: events.length }
  }
  return api.post('/ai/save-outline-events', { 
    novel_id: novelId, 
    chapter_id: chapterId, 
    events 
  })
}

/**
 * Step 4: AI 按大纲填充正文
 * POST /ai/fill-chapter
 * 
 * 请求参数用 events（不是 outline）
 * 真实响应格式：
 * { success: true, content: "...", word_count: N, ai_parts: [{start, end}], user_parts: [], chapter_id: N }
 */
export async function fillChapter(novelId, chapterId, events, style, originalParagraph) {
  if (useMock) {
    await new Promise(resolve => setTimeout(resolve, 3000))
    const mockContent = `夜色如墨，小镇上唯一的客栈还亮着昏黄的灯。

门被推开的时候，风裹着寒意灌了进来。一个身影踉跄着踏入门槛，宽大的斗篷下看不清面容，只有一只手紧紧按着腰侧——那里有暗色的液体正在缓缓渗出。

掌柜抬头看了一眼，没多问，指了指角落的桌子。来客点了点头，坐下的瞬间，斗篷的兜帽微微滑落，露出一截白皙的脖颈和耳后一颗极小的痣。`
    return {
      success: true,
      content: mockContent,
      word_count: mockContent.replace(/\s/g, '').length,
      ai_parts: [{ start: 0, end: mockContent.length }],
      user_parts: [],
      chapter_id: chapterId
    }
  }
  return api.post('/ai/fill-chapter', { 
    novel_id: novelId, 
    chapter_id: chapterId, 
    events,
    style, 
    original_paragraph: originalParagraph 
  })
}
