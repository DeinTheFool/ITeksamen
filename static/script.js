import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'



try {
  console.log('Supabase env -> URL present:', !!import.meta.env.SUPABASE_URL, 'ANON_KEY present:', !!import.meta.env.SUPABASE_ANON)
} catch (e) {
  console.log('Supabase env check failed', e)
}


const SUPABASE_URL = import.meta.env.SUPABASE_URL 
const SUPABASE_ANON = import.meta.env.SUPABASE_ANON


if (!SUPABASE_URL || !SUPABASE_ANON) {
  console.warn('Supabase URL or ANON key is missing. Client will not initialize.')
}

const supa = createClient(SUPABASE_URL, SUPABASE_ANON)
const listContainer = document.getElementById('meldinger')

console.log('SUPABASE_URL:', SUPABASE_URL)
console.log('SUPABASE_ANON present:', Boolean(SUPABASE_ANON))

async function logEnvEndpoint() {
  try {
    const res = await fetch('/env')
    const envData = await res.json()
    console.log('Browser env endpoint data:', envData)
  } catch (err) {
    console.warn('Failed to fetch /env endpoint', err)
  }
}

async function renderPostList(container) {
  if (!container) return
  container.innerHTML = '<h2>Poster</h2><p>Loading…</p>'

  try {
    const { data, error } = await supa
      .from('messages')
      .select('id, name, message, created_at')
      .order('created_at', { ascending: false })

    if (error) throw error

    if (!data || data.length === 0) {
      container.innerHTML = '<h2>Posts</h2><p>No posts yet.</p>'
      return
    }

    const list = document.createElement('div')
    list.className = 'post-list'

    data.forEach(post => {
      const el = document.createElement('article')
      el.className = 'post-card'
      el.id = post.id
      const date = post.created_at ? new Date(post.created_at).toLocaleString() : ''
      el.innerHTML = `
        <h3>${escapeHtml(post.name || 'Anonymous')}</h3>
        <p class="meta">${date}</p>
        <p>${escapeHtml(post.message || '')}</p>
      `
      list.appendChild(el)
    })

    container.innerHTML = '<h2>Posts</h2>'
    container.appendChild(list)
  } catch (err) {
    console.error('Failed to load posts', err)
    container.innerHTML = `<h2>Posts</h2><p class="error">Failed to load posts: ${escapeHtml(err.message || err)}</p>`
  }
}

function escapeHtml(str) {
  if (!str) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

// Auto-run when loaded
logEnvEndpoint()
renderPostList(listContainer)
