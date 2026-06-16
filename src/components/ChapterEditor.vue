<template>
  <div class="chapter-editor-container" :class="[`editor-theme-${currentTheme}`]">
    <!-- 精简格式工具栏 -->
    <div class="editor-toolbar">
      <div class="toolbar-left">
        <button-group>
          <toolbar-btn icon="B" title="加粗 Ctrl+B" :active="editor?.isActive('bold')" @click="editor?.chain().focus().toggleBold().run()" />
          <toolbar-btn icon="I" title="斜体 Ctrl+I" :active="editor?.isActive('italic')" @click="editor?.chain().focus().toggleItalic().run()" />
          <toolbar-btn icon="U" title="下划线" :active="editor?.isActive('underline')" @click="editor?.chain().focus().toggleUnderline().run()" />
          <toolbar-btn icon="S" title="删除线" :active="editor?.isActive('strike')" @click="editor?.chain().focus().toggleStrike().run()" />
        </button-group>

        <button-group>
          <toolbar-btn icon="H2" title="标题2" :active="editor?.isActive('heading', { level: 2 })" @click="editor?.chain().focus().toggleHeading({ level: 2 }).run()" />
          <toolbar-btn icon="H3" title="标题3" :active="editor?.isActive('heading', { level: 3 })" @click="editor?.chain().focus().toggleHeading({ level: 3 }).run()" />
        </button-group>

        <button-group>
          <toolbar-btn icon="❝" title="引用" :active="editor?.isActive('blockquote')" @click="editor?.chain().focus().toggleBlockquote().run()" />
          <toolbar-btn icon="—" title="分割线" @click="editor?.chain().focus().setHorizontalRule().run()" />
          <toolbar-btn icon="•" title="无序列表" :active="editor?.isActive('bulletList')" @click="editor?.chain().focus().toggleBulletList().run()" />
          <toolbar-btn icon="1." title="有序列表" :active="editor?.isActive('orderedList')" @click="editor?.chain().focus().toggleOrderedList().run()" />
        </button-group>

        <button-group>
          <toolbar-btn icon="↩" title="撤销 Ctrl+Z" :disabled="!editor?.can().undo()" @click="editor?.chain().focus().undo().run()" />
          <toolbar-btn icon="↪" title="重做 Ctrl+Y" :disabled="!editor?.can().redo()" @click="editor?.chain().focus().redo().run()" />
        </button-group>
      </div>

      <div class="toolbar-right">
        <!-- AI色码图例 -->
        <div class="ai-legend" v-if="showAiLegend">
          <span class="legend-item"><span class="legend-dot" style="background:var(--ai-text-generated)"></span>生成</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--ai-text-edited)"></span>编辑</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--ai-text-input)"></span>输入</span>
        </div>
      </div>
    </div>

    <!-- 编辑器主体 -->
    <editor-content :editor="editor" class="editor-body" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import Underline from '@tiptap/extension-underline'
import { TextStyle } from '@tiptap/extension-text-style'
import Highlight from '@tiptap/extension-highlight'
import { AiSourceGenerated, AiSourceEdited, AiSourceInput, AiSourcePrompt, AiTextSourceExtension } from '@/extensions/aiTextSource'

const ButtonGroup = { template: '<div class="btn-group"><slot/></div>' }
const ToolbarBtn = {
  props: ['icon', 'title', 'active', 'disabled'],
  template: `<button class="tb-btn" :class="{ active }" :disabled="disabled" :title="title">{{ icon }}</button>`
}

const props = defineProps({
  modelValue: { type: String, default: '' },
  showAiLegend: { type: Boolean, default: true },
  currentTheme: { type: String, default: 'typora' },
  chapterTitle: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue', 'save', 'selection-change', 'content-change'])

const saveStatus = ref('saved')
let autoSaveTimer = null

function convertToHtml(content) {
  if (!content) return ''
  if (content.includes('<') && content.includes('>')) return content
  if (content.trim()) return content.split('\n').map(l => `<p>${l || ''}</p>`).join('')
  return ''
}

const editor = useEditor({
  content: convertToHtml(props.modelValue),
  extensions: [
    StarterKit.configure({ heading: { levels: [2, 3] } }),
    Placeholder.configure({ placeholder: '落笔生花，开始创作你的故事...' }),
    Underline,
    TextStyle,
    Highlight.configure({ multicolor: true }),
    AiSourceGenerated,
    AiSourceEdited,
    AiSourceInput,
    AiSourcePrompt,
    AiTextSourceExtension,
  ],
  editorProps: {
    attributes: { class: 'prose-mirror' },
  },
  onUpdate: ({ editor }) => {
    saveStatus.value = 'unsaved'
    emit('update:modelValue', editor.getHTML())
    emit('content-change', editor.getHTML())
    clearTimeout(autoSaveTimer)
    autoSaveTimer = setTimeout(() => {
      saveStatus.value = 'saving'
      emit('save', editor.getHTML())
      setTimeout(() => { saveStatus.value = 'saved' }, 600)
    }, 2000)
  },
  onSelectionUpdate: ({ editor }) => {
    const { from, to } = editor.state.selection
    const text = editor.state.doc.textBetween(from, to, '')
    emit('selection-change', text)
  }
})

watch(() => props.modelValue, (newVal) => {
  if (editor.value && editor.value.getHTML() !== convertToHtml(newVal)) {
    editor.value.commands.setContent(convertToHtml(newVal), false)
  }
})

const handleKeydown = (e) => {
  if (!editor.value) return
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    saveStatus.value = 'saving'
    emit('save', editor.value.getHTML())
    setTimeout(() => { saveStatus.value = 'saved' }, 600)
  }
}

onMounted(() => { window.addEventListener('keydown', handleKeydown) })
onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
  clearTimeout(autoSaveTimer)
  editor.value?.destroy()
})

defineExpose({
  getHTML: () => editor.value?.getHTML() || '',
  getText: () => editor.value?.getText() || '',
  getEditor: () => editor.value,
  markAiText: (source) => editor.value?.chain().focus().setAiSource(source).run(),
  clearAiMarks: () => editor.value?.chain().focus().clearAllAiSources().run(),
  getSelectedText: () => {
    if (!editor.value) return ''
    const { from, to } = editor.value.state.selection
    return editor.value.state.doc.textBetween(from, to, '')
  },
  insertContent: (content) => editor.value?.chain().focus().insertContent(content).run(),
  replaceSelection: (content) => {
    if (!editor.value) return
    const { from, to } = editor.value.state.selection
    if (from === to) {
      editor.value.chain().focus().insertContent(content).run()
    } else {
      editor.value.chain().focus().deleteSelection().insertContent(content).run()
    }
  }
})
</script>

<style scoped>
.chapter-editor-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  background: var(--editor-bg, var(--bg-primary));
  transition: background 0.3s;
}

/* 工具栏 */
.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  flex-wrap: wrap;
  gap: 6px;
  flex-shrink: 0;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

.btn-group {
  display: flex;
  gap: 1px;
  background: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.tb-btn {
  padding: 4px 8px;
  border: none;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  font-family: var(--font-mono), monospace;
  transition: all 0.15s;
  white-space: nowrap;
}
.tb-btn:hover:not(:disabled) { background: var(--bg-hover); color: var(--text-primary); }
.tb-btn.active { background: var(--brand-primary-bg); color: var(--brand-primary); }
.tb-btn:disabled { opacity: 0.3; cursor: not-allowed; }

/* AI图例 */
.ai-legend { display: flex; gap: 8px; font-size: 10px; color: var(--text-secondary); }
.legend-item { display: flex; align-items: center; gap: 2px; }
.legend-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

/* 编辑器主体 */
.editor-body {
  flex: 1;
  overflow-y: auto;
}

.editor-body :deep(.prose-mirror) {
  min-height: 100%;
  padding: 24px 32px;
  outline: none;
  font-size: 15px;
  line-height: 1.9;
  font-family: var(--font-content), serif;
  color: var(--text-primary);
  caret-color: var(--editor-cursor, var(--brand-primary));
  transition: font-family 0.2s, color 0.2s;
}

.editor-body :deep(.prose-mirror p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  color: var(--text-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
  font-style: italic;
}

.editor-body :deep(.prose-mirror h2) {
  font-size: 20px; font-weight: 700; margin: 24px 0 12px; line-height: 1.4;
  color: var(--text-primary); border-bottom: 1px solid var(--border-color); padding-bottom: 6px;
}
.editor-body :deep(.prose-mirror h3) {
  font-size: 17px; font-weight: 600; margin: 18px 0 10px; line-height: 1.4; color: var(--text-primary);
}
.editor-body :deep(.prose-mirror blockquote) {
  margin: 12px 0; padding: 10px 16px;
  border-left: 3px solid var(--brand-primary);
  background: var(--bg-secondary); color: var(--text-secondary);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.editor-body :deep(.prose-mirror ul),
.editor-body :deep(.prose-mirror ol) { padding-left: 24px; margin: 8px 0; }
.editor-body :deep(.prose-mirror li) { margin: 4px 0; }
.editor-body :deep(.prose-mirror hr) { border: none; border-top: 1px solid var(--border-color); margin: 24px 0; }
.editor-body :deep(.prose-mirror p) { margin: 6px 0; }

/* AI文本色码 */
.editor-body :deep(mark[data-ai-source="generated"]) {
  background: var(--ai-text-generated-bg); color: var(--ai-text-generated);
  border-bottom: 1px dashed var(--ai-text-generated); padding: 0 2px; border-radius: 2px;
}
.editor-body :deep(mark[data-ai-source="edited"]) {
  background: var(--ai-text-edited-bg); color: var(--ai-text-edited);
  border-bottom: 1px dashed var(--ai-text-edited); padding: 0 2px; border-radius: 2px;
}
.editor-body :deep(mark[data-ai-source="input"]) {
  background: var(--ai-text-input-bg); color: var(--ai-text-input);
  border-bottom: 1px dashed var(--ai-text-input); padding: 0 2px; border-radius: 2px;
}
.editor-body :deep(mark[data-ai-source="prompt"]) {
  background: var(--ai-text-prompt-bg); color: var(--ai-text-prompt);
  border-bottom: 1px dashed var(--ai-text-prompt); padding: 0 2px; border-radius: 2px;
}

.editor-body :deep(mark.ai-highlight) {
  background: var(--ai-text-generated-bg); border-radius: 2px;
  animation: aiFadeIn 0.6s ease-out;
}
@keyframes aiFadeIn { from { background: rgba(196,181,253,0.25); } to { background: var(--ai-text-generated-bg); } }

/* 5套编辑器主题 */
.editor-theme-default .editor-body :deep(.prose-mirror) {
  font-family: var(--font-body), sans-serif; line-height: 1.7;
}
.editor-theme-notion .editor-body :deep(.prose-mirror) {
  font-family: var(--font-body), sans-serif; font-size: 15px; line-height: 1.8;
  padding: 24px 48px; max-width: 720px; margin: 0 auto;
}
.editor-theme-notion .editor-body :deep(.prose-mirror h2) { border-bottom: none; font-size: 22px; margin-top: 28px; }
.editor-theme-notion .editor-body :deep(.prose-mirror h3) { font-size: 18px; }

.editor-theme-typora .editor-body :deep(.prose-mirror) {
  font-family: var(--font-content), serif; font-size: 16px; line-height: 1.9;
  padding: 28px 40px; max-width: 780px; margin: 0 auto;
}
.editor-theme-typora .editor-body :deep(.prose-mirror h2) {
  font-size: 22px; font-weight: 700; border-bottom: 2px solid var(--brand-primary); padding-bottom: 8px;
}
.editor-theme-typora .editor-body :deep(.prose-mirror h3) { font-size: 18px; }
.editor-theme-typora .editor-body :deep(.prose-mirror blockquote) { border-left-width: 4px; font-style: italic; }

.editor-theme-word .editor-body { background: var(--bg-secondary); padding: 24px; }
.editor-theme-word .editor-body :deep(.prose-mirror) {
  font-family: var(--font-body), sans-serif; font-size: 14px; line-height: 1.8;
  padding: 40px 56px; background: var(--bg-card); max-width: 680px; margin: 0 auto;
  border: 1px solid var(--border-color); border-radius: var(--radius-md); min-height: 600px;
  box-shadow: var(--shadow-card);
}
.editor-theme-word .editor-body :deep(.prose-mirror h2) { border-bottom: 1px solid var(--border-color); font-size: 18px; }

.editor-theme-focus .editor-body :deep(.prose-mirror) {
  font-family: var(--font-content), serif; font-size: 18px; line-height: 2.2;
  padding: 32px 60px; max-width: 640px; margin: 0 auto; letter-spacing: 0.02em;
}
.editor-theme-focus .editor-body :deep(.prose-mirror h2) { font-size: 24px; text-align: center; border-bottom: none; }
.editor-theme-focus .editor-body :deep(.prose-mirror h3) { font-size: 20px; text-align: center; }

/* 滚动条 */
.editor-body::-webkit-scrollbar { width: 6px; }
.editor-body::-webkit-scrollbar-track { background: transparent; }
.editor-body::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 3px; }
.editor-body::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-thumb-hover); }

/* 移动端 */
@media (max-width: 768px) {
  .editor-toolbar { padding: 4px 8px; gap: 4px; }
  .toolbar-left { gap: 4px; }
  .btn-group { gap: 0; }
  .tb-btn { padding: 3px 6px; font-size: 10px; }
  .ai-legend { display: none; }
  .editor-body :deep(.prose-mirror) {
    padding: 16px 18px !important; max-width: 100% !important; font-size: 14px;
  }
}
</style>
