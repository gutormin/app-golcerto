async function loadMatches() {
  const container = document.getElementById('matches-container');
  container.innerHTML = `<div class="loading-card"><div class="loading-spinner"></div><div class="loading-text">Calculando predições com IA...</div></div>`;

  const apiOk = await checkAPIStatus();

  if (!apiOk) {
    document.getElementById('matches-container').innerHTML = `<div class="error-card">
      <div class="error-icon">⚠️</div>
      <div class="error-text">Backend offline.<br>Rode o servidor com:<br><code style="color:var(--accent);font-size:12px">python -m uvicorn app.main:app --port 8002</code></div>
      <button class="btn-retry" onclick="loadMatches()">Tentar novamente</button>
    </div>`;
    return;
  }

  try {
    await fetchLiveResults();
    const r = await fetch(API + '/matches', {signal: AbortSignal.timeout(12000)});
    if (!r.ok) throw new Error('API matches error');
    const data = await r.json();
    
    allMatchesData = (data.matches || []).map((m, i) => {
      // Popular o cache de predições
      const key = `${m.home}_${m.away}`;
      predictionsCache[key] = m.prediction;
      
      // Armazenar placar ao vivo/final se houver
      const st = m.status || '';
      if (['FINISHED','IN_PLAY','PAUSED'].includes(st)) {
        liveResults[key] = {
          homeScore: (m.score||{}).home ?? null,
          awayScore: (m.score||{}).away ?? null,
          status: (st==='IN_PLAY'||st==='PAUSED') ? 'LIVE' : 'FINISHED',
        };
      }
      
      return {
        match: m,
        html: renderMatchCard(m, m.prediction, i)
      };
    });
    
    renderFilteredMatches();
    updateAIGamification(data.matches);
    startAutoRefresh();
    
    const now = new Date();
    const luel = document.getElementById('last-update');
    if(luel) luel.textContent = 'Atualizado ' + now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');
  } catch(e) {
    console.error(e);
    document.getElementById('matches-container').innerHTML = `<div class="error-card">
      <div class="error-icon">⚠️</div>
      <div class="error-text">Erro ao buscar partidas da API.<br>Tente novamente.</div>
      <button class="btn-retry" onclick="loadMatches()">Tentar novamente</button>
    </div>`;
  }
}