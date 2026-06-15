/**
 * 创作引擎模块 (Creation)
 * 处理创作项目管理、节点、边、快照等
 */

import api from '../index'

// ============ 项目 ============

/**
 * 获取创作项目列表
 * @param {object} [params] - 查询参数
 * @returns {Promise<array>} 项目列表
 */
export function getProjects(params) {
  return api.get('/creation/projects', { params })
}

/**
 * 创建创作项目
 * @param {object} data - 项目数据
 * @param {string} data.name - 项目名称
 * @param {string} [data.type] - 项目类型
 * @param {string} [data.description] - 项目描述
 * @returns {Promise<object>} 创建的项目
 */
export function createProject(data) {
  return api.post('/creation/projects', data)
}

/**
 * 获取项目详情
 * @param {number} pid - 项目ID
 * @returns {Promise<object>} 项目详情
 */
export function getProject(pid) {
  return api.get(`/creation/projects/${pid}`)
}

/**
 * 更新项目
 * @param {number} pid - 项目ID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的项目
 */
export function updateProject(pid, data) {
  return api.put(`/creation/projects/${pid}`, data)
}

/**
 * 删除项目
 * @param {number} pid - 项目ID
 * @returns {Promise<void>}
 */
export function deleteProject(pid) {
  return api.delete(`/creation/projects/${pid}`)
}

// ============ 节点 ============

/**
 * 获取项目节点
 * @param {number} pid - 项目ID
 * @param {string} [stage] - 阶段过滤
 * @returns {Promise<array>} 节点列表
 */
export function getNodes(pid, stage) {
  return api.get(`/creation/projects/${pid}/nodes`, { params: { stage } })
}

/**
 * 创建节点
 * @param {number} pid - 项目ID
 * @param {object} data - 节点数据
 * @param {string} data.type - 节点类型
 * @param {object} data.position - 位置
 * @param {object} [data.data] - 节点数据
 * @returns {Promise<object>} 创建的节点
 */
export function createNode(pid, data) {
  return api.post(`/creation/projects/${pid}/nodes`, data)
}

/**
 * 获取节点详情
 * @param {number} pid - 项目ID
 * @param {string} nuuid - 节点UUID
 * @returns {Promise<object>} 节点详情
 */
export function getNode(pid, nuuid) {
  return api.get(`/creation/projects/${pid}/nodes/${nuuid}`)
}

/**
 * 更新节点
 * @param {number} pid - 项目ID
 * @param {string} nuuid - 节点UUID
 * @param {object} data - 更新的数据
 * @returns {Promise<object>} 更新后的节点
 */
export function updateNode(pid, nuuid, data) {
  return api.put(`/creation/projects/${pid}/nodes/${nuuid}`, data)
}

/**
 * 删除节点
 * @param {number} pid - 项目ID
 * @param {string} nuuid - 节点UUID
 * @returns {Promise<void>}
 */
export function deleteNode(pid, nuuid) {
  return api.delete(`/creation/projects/${pid}/nodes/${nuuid}`)
}

// ============ 边 ============

/**
 * 获取项目边列表
 * @param {number} pid - 项目ID
 * @returns {Promise<array>} 边列表
 */
export function getEdges(pid) {
  return api.get(`/creation/projects/${pid}/edges`)
}

/**
 * 创建边
 * @param {number} pid - 项目ID
 * @param {object} data - 边数据
 * @param {string} data.source - 源节点ID
 * @param {string} data.target - 目标节点ID
 * @param {string} [data.type] - 边类型
 * @param {object} [data.data] - 边数据
 * @returns {Promise<object>} 创建的边
 */
export function createEdge(pid, data) {
  return api.post(`/creation/projects/${pid}/edges`, data)
}

/**
 * 删除边
 * @param {number} pid - 项目ID
 * @param {string} eid - 边ID
 * @returns {Promise<void>}
 */
export function deleteEdge(pid, eid) {
  return api.delete(`/creation/projects/${pid}/edges/${eid}`)
}

// ============ 快照 ============

/**
 * 保存项目快照
 * @param {number} pid - 项目ID
 * @param {object} data - 快照数据
 * @param {string} [data.description] - 快照描述
 * @returns {Promise<object>} 保存的快照
 */
export function saveSnapshot(pid, data) {
  return api.post(`/creation/projects/${pid}/snapshots`, data)
}

// ============ AI 生成 ============

/**
 * 从设置生成内容
 * @param {object} data - 生成参数
 * @param {number} data.projectId - 项目ID
 * @param {object} data.settings - 生成设置
 * @returns {Promise<object>} 生成结果
 */
export function aiGenerateFromSettings(data) {
  return api.post('/creation/ai/generate-from-settings', data)
}

/**
 * AI 生成事件
 * @param {object} data - 生成参数
 * @param {number} data.projectId - 项目ID
 * @param {object} [data.context] - 上下文
 * @returns {Promise<array>} 生成的事件列表
 */
export function aiGenerateEvents(data) {
  return api.post('/creation/ai/generate-events', data)
}

/**
 * AI 生成大纲
 * @param {object} data - 生成参数
 * @param {number} data.projectId - 项目ID
 * @param {string} [data.prompt] - 提示词
 * @returns {Promise<object>} 生成的大纲
 */
export function aiGenerateOutline(data) {
  return api.post('/creation/ai/generate-outline', data)
}
