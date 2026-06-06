import re

# Read the HTML content
html_path = 'GolCerto2026_FINAL6 (2).html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's define the new premium stacked card layout for page-profile
new_profile_content = """<!-- PAGE: PROFILE -->
<div class="page" id="page-profile">
  <div class="rank-hero" style="background: linear-gradient(135deg, #0d0d0d 0%, #151515 100%); border-bottom: 1px solid rgba(197, 168, 92, 0.2); padding: 30px 20px; text-align: center;">
    <div class="rank-hero-label" style="color: var(--gold); font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">Planos & Assinatura</div>
    <div class="rank-hero-title" style="font-family: 'Oswald', sans-serif; font-size: 26px; font-weight: bold; color: #fff; margin-bottom: 8px;">ESCOLHA SEU PLANO DE IA</div>
    <div class="rank-hero-sub" style="color: var(--text3); font-size: 12px; line-height: 1.4; max-width: 320px; margin: 0 auto;">Eleve o nível dos seus palpites na Copa do Mundo 2026 com previsões matemáticas avançadas.</div>
  </div>

  <div style="padding: 20px; display: flex; flex-direction: column; gap: 20px;">
    
    <!-- 1. PLANO STANDARD (R$ 19,90) -->
    <div class="premium-card" style="background: var(--card-bg); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 15px; position: relative;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 12px;">
        <div>
          <div style="font-family: 'Oswald', sans-serif; font-size: 18px; font-weight: bold; color: #fff;">PLANO STANDARD</div>
          <div style="font-size: 11px; color: var(--text3);">Previsões completas da Copa</div>
        </div>
        <div style="text-align: right;">
          <div style="font-family: 'Oswald', sans-serif; font-size: 24px; font-weight: bold; color: #fff;">R$ 19,90</div>
          <div style="font-size: 9px; color: var(--text3);">pagamento único</div>
        </div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px; color: var(--text2);">
        <div style="display: flex; gap: 8px;"><span style="color:#aaa;">✓</span><span>3 placares sugeridos pela IA por jogo</span></div>
        <div style="display: flex; gap: 8px;"><span style="color:#aaa;">✓</span><span>Modelo Dixon-Coles + Poisson bivariado</span></div>
        <div style="display: flex; gap: 8px;"><span style="color:#aaa;">✓</span><span>Calibração em tempo real com odds de mercado</span></div>
        <div style="display: flex; gap: 8px;"><span style="color:#aaa;">✓</span><span>Feed de notícias e histórico real integrados</span></div>
        <div style="display: flex; gap: 8px;"><span style="color:#aaa;">✓</span><span>Instalação PWA no celular</span></div>
      </div>
      
      <button onclick="handleSubscribe('Standard', 19.90)" style="width: 100%; background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 10px; font-weight: bold; font-size: 13px; cursor: pointer; transition: all 0.2s;">
        Assinar Standard — R$ 19,90
      </button>
    </div>

    <!-- 2. PLANO VIP GOLD (R$ 29,90) - HIGHLIGHTED -->
    <div class="premium-card" style="background: var(--card-bg); border: 2px solid var(--gold); border-radius: 16px; padding: 24px; box-shadow: 0 12px 40px rgba(197, 168, 92, 0.15); display: flex; flex-direction: column; gap: 18px; position: relative; overflow: hidden;">
      
      <!-- Recommended Badge -->
      <div style="position: absolute; top: 12px; right: -35px; background: var(--gold); color: #000; font-size: 9px; font-weight: bold; padding: 4px 40px; transform: rotate(45deg); text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
        VIP
      </div>
      
      <!-- Glow effect -->
      <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(197, 168, 92, 0.2) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
      
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(197, 168, 92, 0.2); padding-bottom: 12px;">
        <div>
          <div style="font-family: 'Oswald', sans-serif; font-size: 22px; font-weight: bold; color: var(--gold);">PLANO VIP GOLD</div>
          <div style="font-size: 11px; color: var(--gold); font-weight: bold;">🥇 MÁXIMO VALOR PERCEBIDO</div>
        </div>
        <div style="text-align: right; margin-right: 20px;">
          <div style="font-family: 'Oswald', sans-serif; font-size: 28px; font-weight: bold; color: var(--gold);">R$ 29,90</div>
          <div style="font-size: 9px; color: var(--text3);">pagamento único</div>
        </div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px; color: var(--text);">
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
      </div>
      
      <button onclick="handleSubscribe('VIP Gold', 29.90)" style="width: 100%; background: var(--gold); color: #000; border: none; border-radius: 8px; padding: 14px; font-weight: bold; font-size: 14px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 15px rgba(197, 168, 92, 0.4);">
        Assinar VIP — R$ 29,90 🔥
      </button>
    </div>

    <!-- VALUE PROPOSITION / FAQ -->
    <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 16px;">
      <div style="font-size: 14px; font-weight: bold; color: #fff; border-left: 3px solid var(--gold); padding-left: 8px;">Por que o VIP é a melhor escolha?</div>
      
      <div style="background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.04); border-radius: 8px; padding: 14px; font-size: 12px; line-height: 1.5; color: var(--text2);">
        <strong style="color:var(--gold); display:block; margin-bottom:4px;">📈 Ferramentas de Análise Profissional</strong>
        Acesso a mercados alternativos (gols e cantos) e o inovador simulador "What-If" colocam você no mesmo nível de analistas profissionais de futebol.
      </div>
    </div>
  </div>
</div>

<!-- BEAUTIFUL CHECKOUT MODAL -->
<div id="checkout-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); backdrop-filter:blur(8px); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:#0d0d0d; border: 1px solid var(--gold); border-radius: 16px; padding: 24px; width: 90%; max-width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align:center; position:relative;">
    <button onclick="closeCheckout()" style="position:absolute; top:12px; right:12px; background:none; border:none; color:var(--text3); font-size:18px; cursor:pointer;">&times;</button>
    
    <div style="color:var(--gold); font-size:11px; font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px;">Pagamento Seguro</div>
    <div id="modal-plan-title" style="font-family:'Oswald', sans-serif; font-size:20px; color:#fff; margin-bottom:15px;">ASSINATURA VIP GOLD</div>
    
    <!-- QR Code Mockup -->
    <div style="background:#fff; padding:15px; border-radius:12px; width:160px; height:160px; margin:0 auto 15px; display:flex; align-items:center; justify-content:center; box-shadow: 0 4px 15px rgba(255,255,255,0.1);">
      <!-- Simple CSS drawn QR code pattern representation -->
      <div style="width:130px; height:130px; background: repeating-conic-gradient(#000 0% 25%, transparent 0% 50%) 0 0/15px 15px, repeating-conic-gradient(#000 0% 25%, transparent 0% 50%) 7.5px 7.5px/15px 15px; opacity: 0.85;"></div>
    </div>
    
    <div style="font-size:12px; color:var(--text2); margin-bottom:15px; line-height:1.4;">
      Escaneie o QR Code acima no app do seu banco ou use a chave abaixo para pagar via <strong>PIX</strong>.
    </div>
    
    <div style="background:#151515; border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <code id="pix-key" style="font-size:10px; color:var(--text3); word-break:break-all; text-align:left; max-width:80%;">golcerto2026.pix.vip.gateway.br/checkout/payment-key</code>
      <button onclick="copyPixKey()" style="background:var(--gold); border:none; border-radius:4px; color:#000; padding:6px 10px; font-size:10px; font-weight:bold; cursor:pointer;">Copiar</button>
    </div>
    
    <div id="checkout-status" style="font-size:12px; color:var(--gold); font-weight:bold; display:flex; align-items:center; justify-content:center; gap:8px;">
      <div class="loading-spinner" style="width:14px; height:14px; border-width:2px; margin:0;"></div>
      Aguardando confirmação do PIX...
    </div>
    
    <!-- Simulation payment trigger -->
    <button onclick="simulatePayment()" style="margin-top:15px; background:none; border:1px dashed rgba(255,255,255,0.15); color:var(--text3); border-radius:6px; padding:6px 12px; font-size:10px; cursor:pointer; width:100%;">
      [Simular confirmação automática do banco]
    </button>
  </div>
</div>
"""

# Let's replace the page-profile section in the content
start_idx = content.find('<!-- PAGE: PROFILE -->')
end_idx = content.find('<!-- VALUE PROPOSITION / FAQ -->')
# We need to find the closing div of page-profile which starts after FAQ
faq_start = content.find('<!-- VALUE PROPOSITION / FAQ -->', start_idx)
# Let's find the closing </div> of page-profile. It would be followed by another page like <!-- PAGE: ALERTS --> or similar
next_page_idx = content.find('<!-- PAGE:', faq_start)
if next_page_idx == -1:
    next_page_idx = content.find('<div class="page"', faq_start)

# Let's locate the exact closing </div> before that next page
profile_end_idx = content.rfind('</div>', faq_start, next_page_idx) + 6

# Replace page-profile content
content_replaced = content[:start_idx] + new_profile_content + content[profile_end_idx:]

# Let's inject JavaScript helper functions at the end of the first script block
# First script block ends at </script> around line 1873
script_end_idx = content_replaced.find('</script>')

js_helpers = """
// Premium / VIP subscription simulator logic
let activePlan = 'Free';

function handleSubscribe(planName, price) {
  document.getElementById('modal-plan-title').textContent = 'ASSINATURA ' + planName.toUpperCase();
  document.getElementById('pix-key').textContent = 'golcerto2026.pix.' + planName.toLowerCase().replace(' ', '') + '.gateway.br/pay/' + Math.random().toString(36).substring(2, 12);
  document.getElementById('checkout-modal').style.display = 'flex';
  document.getElementById('checkout-status').innerHTML = '<div class="loading-spinner" style="width:14px; height:14px; border-width:2px; margin:0;"></div> Aguardando confirmação do PIX...';
}

function closeCheckout() {
  document.getElementById('checkout-modal').style.display = 'none';
}

function copyPixKey() {
  const keyText = document.getElementById('pix-key').textContent;
  navigator.clipboard.writeText(keyText).then(() => {
    alert('Chave PIX copiada para a área de transferência!');
  });
}

function simulatePayment() {
  const statusEl = document.getElementById('checkout-status');
  statusEl.innerHTML = '✅ Pagamento confirmado pelo banco!';
  statusEl.style.color = '#4caf50';
  
  setTimeout(() => {
    activePlan = 'VIP';
    document.getElementById('checkout-modal').style.display = 'none';
    
    // Update plan text throughout UI if present
    const planLabel = document.querySelector('.profile-plan');
    if (planLabel) {
      planLabel.innerHTML = '👑 Plano VIP Gold Ativo';
      planLabel.style.color = 'var(--gold)';
    }
    
    // Alert the user
    alert('Parabéns! Sua assinatura VIP Gold foi ativada com sucesso. Aproveite todos os recursos avançados!');
    
    // Enable any simulated VIP features if necessary
  }, 1500);
}
"""

# Inject before the first </script>
final_html = content_replaced[:script_end_idx] + js_helpers + content_replaced[script_end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("HTML successfully updated with VIP subscription cards and PIX checkout simulator!")
