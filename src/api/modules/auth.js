/**
 * 认证模块 (Auth)
 * 处理用户注册、登录等认证相关接口
 */

import api from '../index'

/**
 * 用户注册
 * @param {object} data - 注册信息
 * @param {string} data.username - 用户名
 * @param {string} data.email - 邮箱
 * @param {string} data.password - 密码
 * @returns {Promise<{token: string, user: object}>} 返回token和用户信息
 */
export function register(data) {
  return api.post('/auth/register', data)
}

/**
 * 用户登录
 * @param {object} data - 登录信息
 * @param {string} data.username - 用户名或邮箱
 * @param {string} data.password - 密码
 * @returns {Promise<{token: string, user: object}>} 返回token和用户信息
 */
export function login(data) {
  return api.post('/auth/login', data)
}
