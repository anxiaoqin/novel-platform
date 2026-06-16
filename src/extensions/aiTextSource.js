/**
 * AI文本来源标记扩展
 * 灵感来自 NovelAI 的文本来源色码系统
 * 
 * 用法：
 *   editor.chain().focus().toggleAiSource('generated').run()
 *   editor.chain().focus().toggleAiSource('edited').run()
 *   editor.chain().focus().toggleAiSource('input').run()
 *   editor.chain().focus().toggleAiSource('prompt').run()
 */
import { Mark, markInputRule, markPasteRule } from '@tiptap/core'

// AI来源类型定义
const AI_SOURCES = ['generated', 'edited', 'input', 'prompt']

// 创建AI来源Mark的工厂函数
function createAiSourceMark(source) {
  return Mark.create({
    name: `aiSource_${source}`,
    
    addOptions() {
      return {
        HTMLAttributes: {
          'data-ai-source': source,
          class: `ai-text-${source}`,
        },
      }
    },

    parseHTML() {
      return [
        {
          tag: `mark[data-ai-source="${source}"]`,
        },
      ]
    },

    renderHTML({ HTMLAttributes }) {
      return ['mark', HTMLAttributes, 0]
    },

    addCommands() {
      return {
        [`toggleAiSource_${source}`]: () => ({ commands }) => {
          return commands.toggleMark(this.name)
        },
        [`setAiSource_${source}`]: () => ({ commands }) => {
          return commands.setMark(this.name)
        },
        [`unsetAiSource_${source}`]: () => ({ commands }) => {
          return commands.unsetMark(this.name)
        },
      }
    },
  })
}

// 为每种AI来源类型创建扩展
export const AiSourceGenerated = createAiSourceMark('generated')
export const AiSourceEdited = createAiSourceMark('edited')
export const AiSourceInput = createAiSourceMark('input')
export const AiSourcePrompt = createAiSourceMark('prompt')

// 通用切换命令 — 便捷方式
export const AiTextSourceExtension = Mark.create({
  name: 'aiTextSource',

  addOptions() {
    return {
      HTMLAttributes: {},
    }
  },

  addCommands() {
    return {
      toggleAiSource: (source) => ({ commands }) => {
        const markName = `aiSource_${source}`
        return commands.toggleMark(markName)
      },
      setAiSource: (source) => ({ commands }) => {
        const markName = `aiSource_${source}`
        return commands.setMark(markName)
      },
      unsetAiSource: (source) => ({ commands }) => {
        const markName = `aiSource_${source}`
        return commands.unsetMark(markName)
      },
      // 清除所有AI来源标记
      clearAllAiSources: () => ({ commands }) => {
        AI_SOURCES.forEach(source => {
          const markName = `aiSource_${source}`
          commands.unsetMark(markName)
        })
        return true
      },
    }
  },
})

export { AI_SOURCES }
export default AiTextSourceExtension
