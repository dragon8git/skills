#!/usr/bin/env node

const fs = require('fs')
const path = require('path')
const { Readable } = require('stream')
const { pipeline } = require('stream/promises')
const { execFileSync } = require('child_process')
const { createRequire } = require('module')

const DEFAULT_RECIPIENT = '18692055330@163.com'
const DEFAULT_OUTPUT_DIR = '/Users/lee/Downloads'
const DEFAULT_NODE_MODULES_ROOT = '/Users/lee/project/dls-scams-ui'
const DEFAULT_SMTP_HOST = 'smtp.qq.com'
const DEFAULT_SMTP_USER = '928532756@qq.com'

function option(name, fallback = '') {
  const index = process.argv.indexOf(name)
  if (index < 0) return fallback
  const value = process.argv[index + 1]
  if (value == null || value.startsWith('--')) throw new Error(`${name} requires a value`)
  return value
}

function hasFlag(name) {
  return process.argv.includes(name)
}

function safeFileName(value) {
  const normalized = value.replace(/[\\/:*?"<>|]/g, '_').trim()
  return normalized.length > 0 ? normalized : `download-${Date.now()}`
}

function contentDispositionFileName(value) {
  if (value == null) return ''
  const match = value.match(/filename\*?=(?:UTF-8''|\")?([^;\"]+)/i)
  if (match == null) return ''
  try {
    return decodeURIComponent(match[1].replace(/\"/g, '').trim())
  } catch (_) {
    return match[1].replace(/\"/g, '').trim()
  }
}

function uniquePath(directory, fileName) {
  const extension = path.extname(fileName)
  const stem = extension.length > 0 ? fileName.slice(0, -extension.length) : fileName
  let candidate = path.join(directory, fileName)
  let suffix = 1
  while (fs.existsSync(candidate)) {
    candidate = path.join(directory, `${stem}-${suffix}${extension}`)
    suffix += 1
  }
  return candidate
}

function validateRecipients(value) {
  const recipients = value.split(',').map(item => item.trim()).filter(Boolean)
  if (recipients.length === 0 || recipients.some(item => !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(item))) {
    throw new Error('Invalid recipient address')
  }
  return recipients
}

async function download(url, outputDirectory) {
  const parsedUrl = new URL(url)
  if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') throw new Error('Only HTTP(S) download URLs are supported')
  fs.mkdirSync(outputDirectory, { recursive: true })
  const response = await fetch(parsedUrl, { redirect: 'follow' })
  if (!response.ok || response.body == null) throw new Error(`Download failed: HTTP ${response.status}`)
  const urlFileName = path.basename(new URL(response.url).pathname)
  const suggestedName = contentDispositionFileName(response.headers.get('content-disposition')) || urlFileName
  const downloadPath = uniquePath(outputDirectory, safeFileName(suggestedName))
  try {
    await pipeline(Readable.fromWeb(response.body), fs.createWriteStream(downloadPath, { flags: 'wx' }))
  } catch (error) {
    if (fs.existsSync(downloadPath)) fs.unlinkSync(downloadPath)
    throw error
  }
  return downloadPath
}

function createZip(sourcePath) {
  const zipPath = uniquePath(path.dirname(sourcePath), `${path.basename(sourcePath)}.zip`)
  execFileSync('/usr/bin/ditto', ['-c', '-k', '--sequesterRsrc', '--keepParent', sourcePath, zipPath], { stdio: 'inherit' })
  return zipPath
}

function loadNodemailer() {
  const moduleRoot = process.env.SEND_EMAIL_NODE_MODULES_ROOT || DEFAULT_NODE_MODULES_ROOT
  const packageJson = path.join(moduleRoot, 'package.json')
  if (!fs.existsSync(packageJson)) throw new Error(`Nodemailer source is unavailable: ${moduleRoot}`)
  return createRequire(packageJson)('nodemailer')
}

function keychainPassword() {
  try {
    return execFileSync('/usr/bin/security', [
      'find-generic-password', '-a', DEFAULT_SMTP_USER, '-s', 'SEND_EMAIL_SMTP_PASS', '-w'
    ], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()
  } catch (_) {
    return ''
  }
}

async function sendMail({ recipients, subject, zipPath }) {
  const host = process.env.SEND_EMAIL_SMTP_HOST || DEFAULT_SMTP_HOST
  const user = process.env.SEND_EMAIL_SMTP_USER || DEFAULT_SMTP_USER
  const pass = process.env.SEND_EMAIL_SMTP_PASS || keychainPassword()
  if (!host || !user || !pass) throw new Error('Missing SMTP configuration: SEND_EMAIL_SMTP_HOST, SEND_EMAIL_SMTP_USER, SEND_EMAIL_SMTP_PASS')
  process.env.SEND_EMAIL_SMTP_HOST = host
  process.env.SEND_EMAIL_SMTP_USER = user
  process.env.SEND_EMAIL_SMTP_PASS = pass
  const port = Number(process.env.SEND_EMAIL_SMTP_PORT || '465')
  if (!Number.isInteger(port) || port <= 0) throw new Error('SEND_EMAIL_SMTP_PORT must be a positive integer')
  const nodemailer = loadNodemailer()
  const transporter = nodemailer.createTransport({
    host,
    port,
    secure: (process.env.SEND_EMAIL_SMTP_SECURE || 'true').toLowerCase() === 'true',
    auth: { user, pass }
  })
  const info = await transporter.sendMail({
    from: process.env.SEND_EMAIL_FROM || user,
    to: recipients.join(', '),
    subject,
    text: '附件为下载文件的 ZIP 压缩包。',
    attachments: [{ filename: path.basename(zipPath), path: zipPath }]
  })
  return info.messageId
}

async function main() {
  const url = option('--url')
  if (!url) throw new Error('Usage: --url <http(s) URL> [--to <email[,email]>] [--subject <text>] [--output-dir <path>] [--confirm-send]')
  const recipients = validateRecipients(option('--to', DEFAULT_RECIPIENT))
  const outputDirectory = path.resolve(option('--output-dir', DEFAULT_OUTPUT_DIR))
  const downloadPath = await download(url, outputDirectory)
  const zipPath = createZip(downloadPath)
  const subject = option('--subject', `文件交付：${path.basename(zipPath)}`)
  const summary = { recipients, subject, downloadPath, zipPath }
  if (!hasFlag('--confirm-send')) {
    console.log(JSON.stringify({ status: 'prepared', ...summary }, null, 2))
    return
  }
  const messageId = await sendMail({ recipients, subject, zipPath })
  console.log(JSON.stringify({ status: 'sent', ...summary, messageId }, null, 2))
}

main().catch(error => {
  console.error(error.message)
  process.exitCode = 1
})
