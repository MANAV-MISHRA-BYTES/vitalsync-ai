<template>
  <div class="app-shell">
    <div class="bg-grid" aria-hidden="true"></div>
    <div class="bg-orb orb-1" aria-hidden="true"></div>
    <div class="bg-orb orb-2" aria-hidden="true"></div>
    <div class="bg-orb orb-3" aria-hidden="true"></div>

    <header class="header" role="banner">
      <div class="header-inner">
        <div class="brand">
          <div class="brand-icon" aria-hidden="true">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <path d="M14 2L3 8v12l11 6 11-6V8L14 2z" stroke="url(#g1)" stroke-width="1.5" fill="rgba(0,212,255,0.05)"/>
              <path d="M14 2v24M3 8l11 6 11-6" stroke="url(#g1)" stroke-width="1" opacity="0.4"/>
              <circle cx="14" cy="14" r="3.5" fill="url(#g2)"/>
              <defs>
                <linearGradient id="g1" x1="3" y1="2" x2="25" y2="26" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#00d4ff"/>
                  <stop offset="1" stop-color="#8b5cf6"/>
                </linearGradient>
                <radialGradient id="g2" cx="50%" cy="50%" r="50%">
                  <stop stop-color="#00d4ff"/>
                  <stop offset="1" stop-color="#3b82f6"/>
                </radialGradient>
              </defs>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">VitalSync <span class="brand-ai">AI</span></span>
            <span class="brand-sub">Healthcare Resource Intelligence</span>
          </div>
        </div>
        <div class="header-meta" aria-live="polite">
          <div class="status-badge" :class="loading ? 'status-loading' : 'status-live'">
            <span class="status-dot" aria-hidden="true"></span>
            <span>{{ loading ? 'Computing…' : 'Live' }}</span>
          </div>
          <div class="header-stats" v-if="riskScores.length">
            <span class="stat-chip critical-chip">
              <span class="chip-dot" aria-hidden="true"></span>
              {{ criticalCount }} Critical
            </span>
            <span class="stat-chip high-chip">
              <span class="chip-dot" aria-hidden="true"></span>
              {{ highCount }} High
            </span>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content" role="main">
      <section class="hero-section" aria-label="Overview metrics">
        <div class="hero-title-row">
          <div>
            <h1 class="hero-title">Bottleneck Risk Dashboard</h1>
            <p class="hero-subtitle">Real-time analysis across {{ riskScores.length }} hospital regions — powered by NVIDIA RAPIDS cuDF &amp; Gemini</p>
          </div>
          <button class="refresh-btn" id="refresh-btn" @click="loadRiskScores" :disabled="loading" aria-label="Refresh data">
            <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M13.65 2.35A8 8 0 1 0 15 8h-2a6 6 0 1 1-1.76-4.24L9 6h6V0l-1.35 2.35z" fill="currentColor"/>
            </svg>
            Refresh
          </button>
        </div>

        <div class="kpi-grid" role="list" aria-label="Key performance indicators">
          <div class="kpi-card kpi-critical" role="listitem">
            <div class="kpi-icon" aria-hidden="true">🚨</div>
            <div class="kpi-value">{{ criticalCount }}</div>
            <div class="kpi-label">Critical Wards</div>
            <div class="kpi-bar"><div class="kpi-fill" :style="{ width: kpiPct(criticalCount) }" style="background: var(--critical)"></div></div>
          </div>
          <div class="kpi-card kpi-high" role="listitem">
            <div class="kpi-icon" aria-hidden="true">⚠️</div>
            <div class="kpi-value">{{ highCount }}</div>
            <div class="kpi-label">High Risk Wards</div>
            <div class="kpi-bar"><div class="kpi-fill" :style="{ width: kpiPct(highCount) }" style="background: var(--high)"></div></div>
          </div>
          <div class="kpi-card kpi-avg" role="listitem">
            <div class="kpi-icon" aria-hidden="true">📊</div>
            <div class="kpi-value">{{ avgRiskScore }}</div>
            <div class="kpi-label">Avg Risk Score</div>
            <div class="kpi-bar"><div class="kpi-fill" :style="{ width: avgRiskScore + '%' }" style="background: var(--accent-blue)"></div></div>
          </div>
          <div class="kpi-card kpi-admissions" role="listitem">
            <div class="kpi-icon" aria-hidden="true">🏥</div>
            <div class="kpi-value">{{ totalAdmissions }}</div>
            <div class="kpi-label">Total Admissions</div>
            <div class="kpi-bar"><div class="kpi-fill" style="width: 100%; background: var(--accent-emerald)"></div></div>
          </div>
        </div>
      </section>

      <div class="content-grid">
        <section class="table-section" aria-label="Risk scores table">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon" aria-hidden="true">📋</span>
              Regional Risk Matrix
            </h2>
            <div class="table-controls">
              <label class="sr-only" for="search-input">Search regions</label>
              <div class="search-wrap">
                <svg class="search-icon" width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                  <circle cx="6" cy="6" r="4.5" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M9.5 9.5L13 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <input id="search-input" class="search-input" type="search" v-model="searchQuery" placeholder="Search region…" aria-label="Search regions" />
              </div>
              <div class="filter-pills" role="group" aria-label="Filter by status">
                <button class="filter-pill" :class="{ active: activeFilter === 'ALL' }" @click="activeFilter = 'ALL'" id="filter-all">All</button>
                <button class="filter-pill critical-pill" :class="{ active: activeFilter === 'CRITICAL' }" @click="activeFilter = 'CRITICAL'" id="filter-critical">Critical</button>
                <button class="filter-pill high-pill" :class="{ active: activeFilter === 'HIGH' }" @click="activeFilter = 'HIGH'" id="filter-high">High</button>
                <button class="filter-pill moderate-pill" :class="{ active: activeFilter === 'MODERATE' }" @click="activeFilter = 'MODERATE'" id="filter-moderate">Moderate</button>
                <button class="filter-pill low-pill" :class="{ active: activeFilter === 'LOW' }" @click="activeFilter = 'LOW'" id="filter-low">Low</button>
              </div>
            </div>
          </div>

          <div class="table-wrap" role="region" aria-label="Risk data table">
            <div v-if="loading" class="table-loading" aria-live="polite" aria-busy="true">
              <div class="spinner-ring" aria-hidden="true"></div>
              <p>Processing 1,000,000 patient admissions via cuDF…</p>
            </div>
            <div v-else-if="error" class="table-error" role="alert">
              <span aria-hidden="true">⚠️</span> {{ error }}
            </div>
            <table v-else class="risk-table" aria-label="Regional bottleneck risk scores">
              <thead>
                <tr>
                  <th scope="col" class="th-rank">#</th>
                  <th scope="col" @click="sortBy('region')" class="th-sort" :aria-sort="sortCol === 'region' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Region <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'region' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                  <th scope="col" @click="sortBy('bottleneck_risk_score')" class="th-sort" :aria-sort="sortCol === 'bottleneck_risk_score' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Risk Score <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'bottleneck_risk_score' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                  <th scope="col">Status</th>
                  <th scope="col" @click="sortBy('avg_occupancy')" class="th-sort" :aria-sort="sortCol === 'avg_occupancy' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Occupancy % <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'avg_occupancy' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                  <th scope="col" @click="sortBy('avg_wait')" class="th-sort" :aria-sort="sortCol === 'avg_wait' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Avg Wait (min) <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'avg_wait' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                  <th scope="col" @click="sortBy('avg_severity')" class="th-sort" :aria-sort="sortCol === 'avg_severity' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Severity <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'avg_severity' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                  <th scope="col" @click="sortBy('total_admissions')" class="th-sort" :aria-sort="sortCol === 'total_admissions' ? (sortDir === 1 ? 'ascending' : 'descending') : 'none'">
                    Admissions <span class="sort-arrow" aria-hidden="true">{{ sortCol === 'total_admissions' ? (sortDir === 1 ? '▲' : '▼') : '⇅' }}</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, idx) in filteredScores"
                  :key="row.region"
                  class="table-row"
                  :class="'row-' + row.status.toLowerCase()"
                  :id="'row-' + row.region.replace(/\s+/g, '-').toLowerCase()"
                >
                  <td class="td-rank">{{ idx + 1 }}</td>
                  <td class="td-region">
                    <span class="region-name">{{ row.region }}</span>
                  </td>
                  <td class="td-score">
                    <div class="score-wrap">
                      <span class="score-val" :style="{ color: scoreColor(row.bottleneck_risk_score) }">{{ row.bottleneck_risk_score }}</span>
                      <div class="score-bar-track" aria-hidden="true">
                        <div class="score-bar-fill" :style="{ width: row.bottleneck_risk_score + '%', background: scoreColor(row.bottleneck_risk_score) }"></div>
                      </div>
                    </div>
                  </td>
                  <td class="td-status">
                    <span class="status-tag" :class="'tag-' + row.status.toLowerCase()" :aria-label="'Status: ' + row.status">{{ row.status }}</span>
                  </td>
                  <td class="td-num">
                    <span :class="{ 'val-danger': row.avg_occupancy >= 90 }">{{ row.avg_occupancy }}%</span>
                  </td>
                  <td class="td-num">
                    <span :class="{ 'val-danger': row.avg_wait >= 60 }">{{ row.avg_wait }}</span>
                  </td>
                  <td class="td-num">{{ row.avg_severity }}</td>
                  <td class="td-num">{{ row.total_admissions.toLocaleString() }}</td>
                </tr>
                <tr v-if="filteredScores.length === 0">
                  <td colspan="8" class="td-empty">No regions match the current filter.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="chat-section" aria-label="Gemini AI assistant">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon" aria-hidden="true">✨</span>
              Gemini Clinical AI
            </h2>
            <div class="gemini-badge" aria-label="Powered by Google Gemini">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 2L9.5 9.5 2 12l7.5 2.5L12 22l2.5-7.5L22 12l-7.5-2.5L12 2z" fill="url(#gemini-g)"/>
                <defs>
                  <linearGradient id="gemini-g" x1="2" y1="2" x2="22" y2="22">
                    <stop stop-color="#00d4ff"/>
                    <stop offset="1" stop-color="#8b5cf6"/>
                  </linearGradient>
                </defs>
              </svg>
              Gemini 2.0 Flash
            </div>
          </div>

          <div class="chat-window" ref="chatWindow" role="log" aria-label="Conversation with Gemini AI" aria-live="polite">
            <div v-if="chatMessages.length === 0" class="chat-empty">
              <div class="chat-empty-icon" aria-hidden="true">🤖</div>
              <p>Ask me anything about the current risk data.</p>
              <div class="suggestion-chips" role="list" aria-label="Suggested queries">
                <button
                  v-for="s in suggestions"
                  :key="s"
                  class="suggestion-chip"
                  @click="sendSuggestion(s)"
                  role="listitem"
                >{{ s }}</button>
              </div>
            </div>
            <template v-else>
              <div
                v-for="(msg, i) in chatMessages"
                :key="i"
                class="chat-bubble-wrap"
                :class="msg.role === 'user' ? 'bubble-user-wrap' : 'bubble-ai-wrap'"
              >
                <div class="bubble-avatar" :aria-label="msg.role === 'user' ? 'You' : 'Gemini AI'" aria-hidden="true">
                  {{ msg.role === 'user' ? '👤' : '✨' }}
                </div>
                <div
                  class="chat-bubble"
                  :class="msg.role === 'user' ? 'bubble-user' : 'bubble-ai'"
                  :id="'msg-' + i"
                >
                  <p>{{ msg.text }}</p>
                  <span class="bubble-time" aria-label="Sent at">{{ msg.time }}</span>
                </div>
              </div>
              <div v-if="geminiLoading" class="chat-bubble-wrap bubble-ai-wrap" aria-live="polite" aria-busy="true">
                <div class="bubble-avatar" aria-hidden="true">✨</div>
                <div class="chat-bubble bubble-ai bubble-thinking">
                  <div class="thinking-dots" aria-label="Gemini is thinking">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <div class="chat-input-area" role="form" aria-label="Send a message">
            <label class="sr-only" for="chat-input">Your question</label>
            <textarea
              id="chat-input"
              class="chat-textarea"
              v-model="chatInput"
              @keydown.enter.exact.prevent="sendChat"
              placeholder="Ask about ward risk levels, resource bottlenecks, or suggested interventions…"
              :disabled="geminiLoading || !riskScores.length"
              rows="2"
              aria-label="Type your clinical query"
            ></textarea>
            <button
              class="send-btn"
              id="send-btn"
              @click="sendChat"
              :disabled="geminiLoading || !chatInput.trim() || !riskScores.length"
              aria-label="Send message"
            >
              <svg v-if="!geminiLoading" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
                <path d="M1.5 9L16.5 1.5 9 16.5l-1.5-7.5L1.5 9z" fill="currentColor"/>
              </svg>
              <div v-else class="btn-spinner" aria-hidden="true"></div>
            </button>
          </div>
        </section>
      </div>
    </main>

    <footer class="footer" role="contentinfo">
      <p>VitalSync AI &mdash; Built with NVIDIA RAPIDS cuDF · Flask · Vue 3 · Google Gemini</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'

const riskScores = ref([])
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const activeFilter = ref('ALL')
const sortCol = ref('bottleneck_risk_score')
const sortDir = ref(-1)

const chatMessages = ref([])
const chatInput = ref('')
const geminiLoading = ref(false)
const chatWindow = ref(null)

const suggestions = [
  'Which ward is at highest risk?',
  'Summarize all CRITICAL regions.',
  'What resource interventions do you recommend?',
  'Which ICU has the worst bed occupancy?',
]

const criticalCount = computed(() => riskScores.value.filter(r => r.status === 'CRITICAL').length)
const highCount = computed(() => riskScores.value.filter(r => r.status === 'HIGH').length)
const avgRiskScore = computed(() => {
  if (!riskScores.value.length) return 0
  return (riskScores.value.reduce((s, r) => s + r.bottleneck_risk_score, 0) / riskScores.value.length).toFixed(1)
})
const totalAdmissions = computed(() => {
  const total = riskScores.value.reduce((s, r) => s + r.total_admissions, 0)
  return total >= 1_000_000 ? (total / 1_000_000).toFixed(2) + 'M' : total.toLocaleString()
})

const filteredScores = computed(() => {
  let data = [...riskScores.value]
  if (activeFilter.value !== 'ALL') {
    data = data.filter(r => r.status === activeFilter.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(r => r.region.toLowerCase().includes(q))
  }
  data.sort((a, b) => {
    const va = a[sortCol.value]
    const vb = b[sortCol.value]
    if (typeof va === 'string') return sortDir.value * va.localeCompare(vb)
    return sortDir.value * (vb - va)
  })
  return data
})

function kpiPct(count) {
  if (!riskScores.value.length) return '0%'
  return Math.min(100, (count / riskScores.value.length) * 100 * 4) + '%'
}

function scoreColor(score) {
  if (score >= 75) return 'var(--critical)'
  if (score >= 55) return 'var(--high)'
  if (score >= 35) return 'var(--moderate)'
  return 'var(--low)'
}

function sortBy(col) {
  if (sortCol.value === col) {
    sortDir.value = -sortDir.value
  } else {
    sortCol.value = col
    sortDir.value = -1
  }
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

async function loadRiskScores() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_BASE}/api/risk-scores`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const json = await res.json()
    if (!json.success) throw new Error(json.error)
    riskScores.value = json.data
  } catch (e) {
    error.value = e.message || 'Failed to load risk scores.'
  } finally {
    loading.value = false
  }
}

async function sendChat() {
  const query = chatInput.value.trim()
  if (!query || geminiLoading.value) return

  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  chatMessages.value.push({ role: 'user', text: query, time: now })
  chatInput.value = ''
  geminiLoading.value = true
  await scrollChat()

  try {
    const res = await fetch(`${API_BASE}/api/ask-gemini`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    })
    const json = await res.json()
    if (!json.success) throw new Error(json.error)
    const replyTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    chatMessages.value.push({ role: 'ai', text: json.insight, time: replyTime })
  } catch (e) {
    chatMessages.value.push({ role: 'ai', text: `Error: ${e.message}`, time: '' })
  } finally {
    geminiLoading.value = false
    await scrollChat()
  }
}

function sendSuggestion(text) {
  chatInput.value = text
  sendChat()
}

async function scrollChat() {
  await nextTick()
  if (chatWindow.value) {
    chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  }
}

onMounted(() => {
  loadRiskScores()
})
</script>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

.bg-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.35;
}
.orb-1 { width: 500px; height: 500px; background: radial-gradient(circle, rgba(0,212,255,0.18), transparent); top: -100px; left: -100px; animation: orb-float 12s ease-in-out infinite; }
.orb-2 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(139,92,246,0.18), transparent); bottom: -80px; right: -80px; animation: orb-float 15s ease-in-out infinite reverse; }
.orb-3 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(59,130,246,0.12), transparent); top: 40%; left: 40%; animation: orb-float 18s ease-in-out infinite 3s; }

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.05); }
  66% { transform: translate(-20px, 30px) scale(0.97); }
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(5, 11, 20, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
}

.header-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(0, 212, 255, 0.06);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: var(--radius-md);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}

.brand-text { display: flex; flex-direction: column; gap: 1px; }
.brand-name { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text-primary); }
.brand-ai { background: linear-gradient(135deg, #00d4ff, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.brand-sub { font-size: 0.7rem; color: var(--text-muted); font-weight: 400; letter-spacing: 0.05em; text-transform: uppercase; }

.header-meta { display: flex; align-items: center; gap: 16px; }

.status-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}
.status-live { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: var(--accent-emerald); }
.status-loading { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); color: var(--high); }

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
}
.status-live .status-dot { animation: pulse-dot 2s ease-in-out infinite; }

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.7; }
}

.header-stats { display: flex; gap: 8px; }
.stat-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 0.72rem;
  font-weight: 600;
}
.critical-chip { background: var(--critical-bg); color: var(--critical); border: 1px solid rgba(244,63,94,0.25); }
.high-chip { background: var(--high-bg); color: var(--high); border: 1px solid rgba(245,158,11,0.25); }
.chip-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

.main-content {
  flex: 1;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 32px 0;
  position: relative;
  z-index: 1;
}

.hero-section { margin-bottom: 32px; }
.hero-title-row { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 24px; gap: 16px; }
.hero-title { font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; background: linear-gradient(135deg, #e2e8f0 30%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.2; }
.hero-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 6px; }

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(0, 212, 255, 0.08);
  border: 1px solid rgba(0, 212, 255, 0.25);
  border-radius: var(--radius-md);
  color: var(--accent-cyan);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-smooth);
  white-space: nowrap;
}
.refresh-btn:hover:not(:disabled) { background: rgba(0, 212, 255, 0.15); box-shadow: 0 0 20px rgba(0,212,255,0.15); }
.refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.refresh-icon { transition: transform 0.5s ease; }
.refresh-icon.spinning { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all var(--transition-smooth);
  position: relative;
  overflow: hidden;
}
.kpi-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.03), transparent);
  pointer-events: none;
}
.kpi-card:hover { border-color: var(--border-glow); transform: translateY(-2px); box-shadow: var(--shadow-card); }

.kpi-icon { font-size: 1.25rem; margin-bottom: 6px; }
.kpi-value { font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: var(--text-primary); }
.kpi-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px; }
.kpi-bar { height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.kpi-fill { height: 100%; border-radius: 2px; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }

.content-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
  align-items: start;
  padding-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.section-icon { font-size: 1rem; }

.table-controls { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon { position: absolute; left: 10px; color: var(--text-muted); pointer-events: none; }
.search-input {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.8rem;
  padding: 7px 12px 7px 32px;
  width: 180px;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
}
.search-input:focus { outline: none; border-color: rgba(0,212,255,0.4); box-shadow: 0 0 0 3px rgba(0,212,255,0.08); }
.search-input::placeholder { color: var(--text-muted); }

.filter-pills { display: flex; gap: 6px; }
.filter-pill {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.filter-pill:hover { border-color: var(--border-glow); color: var(--text-primary); }
.filter-pill.active { background: rgba(0,212,255,0.1); border-color: rgba(0,212,255,0.4); color: var(--accent-cyan); }
.critical-pill.active { background: var(--critical-bg); border-color: rgba(244,63,94,0.4); color: var(--critical); }
.high-pill.active { background: var(--high-bg); border-color: rgba(245,158,11,0.4); color: var(--high); }
.moderate-pill.active { background: var(--moderate-bg); border-color: rgba(59,130,246,0.4); color: var(--moderate); }
.low-pill.active { background: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.4); color: var(--low); }

.table-wrap {
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.table-loading, .table-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 60px 24px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}
.table-error { color: var(--critical); }

.spinner-ring {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(0,212,255,0.1);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.risk-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}
.risk-table thead tr {
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0,0,0,0.2);
}
.risk-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  white-space: nowrap;
}
.th-sort { cursor: pointer; user-select: none; }
.th-sort:hover { color: var(--accent-cyan); }
.sort-arrow { margin-left: 4px; opacity: 0.7; }
.th-rank { width: 40px; }

.table-row {
  border-bottom: 1px solid rgba(255,255,255,0.03);
  transition: background var(--transition-fast);
}
.table-row:hover { background: rgba(0, 212, 255, 0.04); }
.row-critical { border-left: 2px solid var(--critical); }
.row-high { border-left: 2px solid var(--high); }
.row-moderate { border-left: 2px solid var(--moderate); }
.row-low { border-left: 2px solid var(--low); }

.risk-table td { padding: 12px 16px; vertical-align: middle; }
.td-rank { color: var(--text-muted); font-weight: 600; font-size: 0.75rem; }
.td-region .region-name { font-weight: 600; color: var(--text-primary); }
.td-num { font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary); }
.val-danger { color: var(--critical); font-weight: 600; }
.td-empty { text-align: center; padding: 40px; color: var(--text-muted); }

.score-wrap { display: flex; flex-direction: column; gap: 4px; }
.score-val { font-family: var(--font-mono); font-size: 0.9rem; font-weight: 700; }
.score-bar-track { height: 3px; background: rgba(255,255,255,0.05); border-radius: 2px; width: 80px; }
.score-bar-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }

.status-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 9px;
  border-radius: 20px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
}
.tag-critical { background: var(--critical-bg); color: var(--critical); border: 1px solid rgba(244,63,94,0.3); }
.tag-high { background: var(--high-bg); color: var(--high); border: 1px solid rgba(245,158,11,0.3); }
.tag-moderate { background: var(--moderate-bg); color: var(--moderate); border: 1px solid rgba(59,130,246,0.3); }
.tag-low { background: rgba(16,185,129,0.1); color: var(--low); border: 1px solid rgba(16,185,129,0.3); }

.chat-section {
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  height: 680px;
  position: sticky;
  top: 88px;
}

.chat-section .section-header {
  padding: 16px 20px 0;
  margin-bottom: 0;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 14px;
}

.gemini-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--accent-cyan);
  background: rgba(0,212,255,0.06);
  border: 1px solid rgba(0,212,255,0.2);
  padding: 4px 10px;
  border-radius: 20px;
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  scroll-behavior: smooth;
}

.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
}
.chat-empty-icon { font-size: 2rem; opacity: 0.6; }

.suggestion-chips { display: flex; flex-direction: column; gap: 8px; width: 100%; margin-top: 8px; }
.suggestion-chip {
  background: rgba(0,212,255,0.04);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 9px 14px;
  color: var(--text-secondary);
  font-size: 0.78rem;
  text-align: left;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
}
.suggestion-chip:hover { background: rgba(0,212,255,0.1); border-color: rgba(0,212,255,0.3); color: var(--accent-cyan); }

.chat-bubble-wrap { display: flex; align-items: flex-start; gap: 8px; }
.bubble-user-wrap { flex-direction: row-reverse; }

.bubble-avatar { font-size: 1.1rem; flex-shrink: 0; margin-top: 2px; }

.chat-bubble {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: var(--radius-md);
  font-size: 0.83rem;
  line-height: 1.55;
  position: relative;
}
.bubble-user {
  background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(59,130,246,0.1));
  border: 1px solid rgba(0,212,255,0.2);
  color: var(--text-primary);
  border-top-right-radius: 2px;
}
.bubble-ai {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-top-left-radius: 2px;
}
.bubble-thinking { padding: 14px 18px; }

.bubble-time {
  display: block;
  font-size: 0.65rem;
  color: var(--text-muted);
  margin-top: 5px;
}

.thinking-dots {
  display: flex;
  gap: 5px;
  align-items: center;
}
.thinking-dots span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent-cyan);
  animation: thinking-bounce 1.2s ease-in-out infinite;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; background: var(--accent-blue); }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; background: var(--accent-purple); }

@keyframes thinking-bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-6px); opacity: 1; }
}

.chat-input-area {
  padding: 12px 16px 16px;
  display: flex;
  gap: 10px;
  align-items: flex-end;
  border-top: 1px solid var(--border-subtle);
}

.chat-textarea {
  flex: 1;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 0.82rem;
  padding: 10px 14px;
  resize: none;
  font-family: var(--font-sans);
  line-height: 1.5;
  transition: border-color var(--transition-fast);
}
.chat-textarea:focus { outline: none; border-color: rgba(0,212,255,0.4); }
.chat-textarea::placeholder { color: var(--text-muted); }
.chat-textarea:disabled { opacity: 0.4; cursor: not-allowed; }

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition-smooth);
  color: #fff;
}
.send-btn:hover:not(:disabled) { transform: scale(1.05); box-shadow: 0 4px 20px rgba(0,212,255,0.35); }
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.footer {
  text-align: center;
  padding: 24px;
  font-size: 0.72rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-subtle);
  margin-top: 8px;
  position: relative;
  z-index: 1;
}

@media (max-width: 1200px) {
  .content-grid { grid-template-columns: 1fr; }
  .chat-section { position: static; height: 520px; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .main-content { padding: 20px 16px 0; }
  .header-inner { padding: 12px 16px; }
  .kpi-grid { grid-template-columns: 1fr 1fr; }
  .hero-title { font-size: 1.4rem; }
  .hero-title-row { flex-direction: column; }
  .table-controls { flex-direction: column; align-items: flex-start; }
  .filter-pills { flex-wrap: wrap; }
}
</style>
