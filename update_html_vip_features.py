# Load the HTML
html_path = 'GolCerto2026_FINAL6 (2).html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's locate the VIP plan features list
# Old list items to replace:
old_features_section = """      <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px; color: var(--text);">
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Tudo do Plano Standard</strong> incluso</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Previsão de Mercados de Gols</strong>: Probabilidades para Ambos Marcam (BTTS), Over/Under gols e cantos</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Value Bets Inteligentes</strong>: Gráficos comparativos IA vs Casas de Apostas com destaque de apostas de valor</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Simulador Interativo "What-If"</strong>: Edite as forças de ataque/defesa para projetar cenários personalizados</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Alertas Premium no Telegram/WhatsApp</strong>: Notificações em tempo real sobre variações de odds e desfalques</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Download de Dossiê Tático (PDF)</strong>: Relatórios estatísticos profissionais de cada jogo</span>
        </div>
      </div>"""

new_features_section = """      <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px; color: var(--text);">
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Tudo do Plano Standard</strong> incluso</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Alertas de Última Hora</strong> via Telegram/WhatsApp (lesões, clima e variações na força da seleção)</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Radar de Vulnerabilidade & Pênaltis</strong>: análise física de fadiga, índice de cartões e aproveitamento de cobranças</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Simulador de Chaves (Bracket)</strong>: preencha o mata-mata visualmente e exporte infográficos personalizados</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Dossiê H2H Histórico Profundo</strong>: retrospectiva de confrontos oficiais e tabus em Copas do Mundo</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Índice de Entrosamento de Elenco</strong>: análise de sinergia do time baseada nos clubes europeus dos atletas</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: flex-start;">
          <span style="color: var(--gold); font-weight: bold;">✓</span>
          <span><strong>Tendências da Comunidade</strong>: dados consolidados de palpites e simulações de todos os usuários</span>
        </div>
      </div>"""

if old_features_section in content:
    content = content.replace(old_features_section, new_features_section)
    print("VIP features updated in HTML successfully!")
else:
    # Let's search using a smaller keyword if formatting differed
    print("Could not find exact block, trying robust replacement...")
    # Find list after "PLANO VIP GOLD"
    pos_vip = content.find("PLANO VIP GOLD")
    pos_list_start = content.find('<div style="display: flex; flex-direction: column; gap: 10px;', pos_vip)
    pos_list_end = content.find('</div>', pos_list_start + 100)
    # count matching closing div for the inner container
    div_count = 1
    for i in range(pos_list_start + 50, len(content)):
        if content[i:i+4] == '<div':
            div_count += 1
        elif content[i:i+5] == '</div':
            div_count -= 1
            if div_count == 0:
                pos_list_end = i + 6
                break
    content = content[:pos_list_start] + new_features_section + content[pos_list_end:]
    print("Robust replacement executed!")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
