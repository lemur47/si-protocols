<script>
  let text = $state('');
  let result = $state(null);
  let loading = $state(false);
  let error = $state('');

  // Lightweight client-side marker matching (no spaCy, no NLP)
  // Subset of markers from src/si_protocols/markers.py
  const VAGUE_ADJECTIVES = new Set([
    'amazing', 'powerful', 'incredible', 'transformative', 'divine',
    'sacred', 'cosmic', 'infinite', 'universal', 'profound',
    'miraculous', 'enlightened', 'spiritual', 'mystical', 'blessed',
  ]);

  const AUTHORITY_PHRASES = [
    'ancient wisdom', 'the universe wants', 'spirit guides',
    'higher self', 'divine plan', 'chosen ones', 'awakened souls',
    'the masters teach', 'sacred knowledge', 'cosmic truth',
  ];

  const URGENCY_PATTERNS = [
    'act now', 'limited time', 'don\'t miss', 'once in a lifetime',
    'before it\'s too late', 'urgent', 'last chance', 'now or never',
  ];

  function clientScore(input) {
    const lower = input.toLowerCase();
    const words = lower.split(/\s+/);
    const wordCount = words.length || 1;

    // Vagueness: fraction of words that are vague adjectives
    const vagueCount = words.filter(w => VAGUE_ADJECTIVES.has(w)).length;
    const vagueness = Math.min((vagueCount / wordCount) * 500, 100);

    // Authority: phrase matches
    const authorityCount = AUTHORITY_PHRASES.filter(p => lower.includes(p)).length;
    const authority = Math.min(authorityCount * 20, 100);

    // Urgency: pattern matches
    const urgencyCount = URGENCY_PATTERNS.filter(p => lower.includes(p)).length;
    const urgency = Math.min(urgencyCount * 25, 100);

    const score = Math.round(vagueness * 0.4 + authority * 0.35 + urgency * 0.25);
    return { score, dimensions: { vagueness: Math.round(vagueness), authority: Math.round(authority), urgency: Math.round(urgency) } };
  }

  async function tryApiAnalysis(input) {
    try {
      const res = await fetch('http://127.0.0.1:8000/analyse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
        signal: AbortSignal.timeout(2000),
      });
      if (!res.ok) return false;
      const data = await res.json();
      result = {
        score: data.overall_threat_score,
        dimensions: {
          vagueness: Math.round(data.tech_contribution),
          authority: data.authority_hits?.length ?? 0,
          urgency: data.urgency_hits?.length ?? 0,
        },
        source: 'api',
      };
      return true;
    } catch {
      return false;
    }
  }

  async function analyse() {
    if (!text.trim()) return;
    loading = true;
    error = '';
    result = null;

    // Try local API first, fall back to client-side
    const apiSuccess = await tryApiAnalysis(text);
    if (!apiSuccess) {
      const { score, dimensions } = clientScore(text);
      result = { score, dimensions, source: 'browser' };
    }

    loading = false;
  }

  function threatLevel(score) {
    if (score <= 33) return 'low';
    if (score <= 66) return 'medium';
    return 'high';
  }

  function threatColour(score) {
    if (score <= 33) return 'var(--colour-success, #22c55e)';
    if (score <= 66) return 'var(--colour-warning, #eab308)';
    return 'var(--colour-danger, #ef4444)';
  }
</script>

<div class="analyser">
  <textarea
    bind:value={text}
    placeholder="Paste spiritual or metaphysical text here to analyse for manipulation patterns..."
    rows="6"
  ></textarea>
  <button onclick={analyse} disabled={loading || !text.trim()}>
    {loading ? 'Analysing…' : 'Analyse'}
  </button>

  {#if result}
    <div class="result" style="border-color: {threatColour(result.score)}">
      <div class="score" style="color: {threatColour(result.score)}">
        <span class="score-number">{result.score}</span>
        <span class="score-label">/ 100 — {threatLevel(result.score)} threat</span>
      </div>
      <div class="dimensions">
        {#each Object.entries(result.dimensions) as [name, value]}
          <div class="dimension">
            <span class="dim-name">{name}</span>
            <div class="dim-bar">
              <div class="dim-fill" style="width: {value}%; background: {threatColour(value)}"></div>
            </div>
            <span class="dim-value">{value}</span>
          </div>
        {/each}
      </div>
      <p class="source">
        {result.source === 'api' ? 'Full analysis via local API (127.0.0.1:8000)' : 'Lightweight browser-only analysis (marker matching only)'}
      </p>
    </div>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

<style>
  .analyser {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 640px;
  }

  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--colour-border, #333);
    border-radius: var(--radius, 4px);
    background: var(--colour-surface, #1a1a1a);
    color: var(--colour-text, #e0e0e0);
    font-family: inherit;
    font-size: 0.9rem;
    resize: vertical;
  }

  button {
    align-self: flex-start;
    padding: 0.5rem 1.5rem;
    border: 1px solid var(--colour-primary, #4f9);
    border-radius: var(--radius, 4px);
    background: transparent;
    color: var(--colour-primary, #4f9);
    font-size: 0.9rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
  }

  button:hover:not(:disabled) {
    background: var(--colour-primary, #4f9);
    color: var(--colour-bg, #0a0a0a);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .result {
    border: 1px solid;
    border-radius: var(--radius, 4px);
    padding: 1rem;
  }

  .score {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .score-number {
    font-size: 2rem;
    font-weight: 700;
  }

  .score-label {
    font-size: 0.85rem;
    color: var(--colour-text-muted, #888);
  }

  .dimensions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .dimension {
    display: grid;
    grid-template-columns: 100px 1fr 40px;
    align-items: center;
    gap: 0.5rem;
  }

  .dim-name {
    font-size: 0.8rem;
    text-transform: capitalize;
    color: var(--colour-text-muted, #888);
  }

  .dim-bar {
    height: 6px;
    background: var(--colour-surface-alt, #222);
    border-radius: 3px;
    overflow: hidden;
  }

  .dim-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.3s;
  }

  .dim-value {
    font-size: 0.8rem;
    text-align: right;
    color: var(--colour-text-muted, #888);
  }

  .source {
    margin-top: 0.75rem;
    font-size: 0.75rem;
    color: var(--colour-text-muted, #888);
    font-style: italic;
  }

  .error {
    color: var(--colour-danger, #ef4444);
    font-size: 0.85rem;
  }
</style>
