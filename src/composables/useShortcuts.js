/**
 * 快捷键Composable
 * 提供统一的快捷键绑定能力
 */
import { ref, onMounted, onUnmounted } from "vue"

/**
 * 快捷键帮助面板内容
 */
export const SHORTCUT_HELP = [
  { key: "Ctrl + S", desc: "保存当前内容" },
  { key: "Ctrl + Enter", desc: "触发AI建议/生成" },
  { key: "Ctrl + L", desc: "锁定/解锁大纲节点（仅大纲页面）" },
  { key: "Ctrl + /", desc: "打开快捷键帮助面板" }
]

/**
 * useShortcuts hook
 */
export function useShortcuts(options = {}) {
  const showHelpPanel = ref(false)
  
  const handleKeydown = (event) => {
    if (event.ctrlKey && event.key === "s") {
      event.preventDefault()
      if (options.onSave) options.onSave()
      return
    }
    if (event.ctrlKey && event.key === "Enter") {
      event.preventDefault()
      if (options.onAiGenerate) options.onAiGenerate()
      return
    }
    if (event.ctrlKey && event.key === "l") {
      event.preventDefault()
      if (options.onToggleLock) options.onToggleLock()
      return
    }
    if (event.ctrlKey && event.key === "/") {
      event.preventDefault()
      showHelpPanel.value = !showHelpPanel.value
      if (options.onShowHelp) options.onShowHelp(showHelpPanel.value)
      return
    }
  }
  
  onMounted(() => {
    if (options.enabled !== false) {
      document.addEventListener("keydown", handleKeydown)
    }
  })
  
  onUnmounted(() => {
    document.removeEventListener("keydown", handleKeydown)
  })
  
  return {
    showHelpPanel,
    openHelp: () => { showHelpPanel.value = true },
    closeHelp: () => { showHelpPanel.value = false },
    toggleHelp: () => { showHelpPanel.value = !showHelpPanel.value }
  }
}

export default useShortcuts
