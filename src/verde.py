# Site "A Nova Profissao" (verde): evento ao vivo de 20 a 22 de janeiro de 2027 (webinario pago de R$ 97).
# Copy: "LP A Nova Profissao copy revisada" (aprovacao do Daniel em 19/11).
# Gera: index.html (headline padrao), versao-1..4.html (uma por headline), inscricao.html (formulario), obrigado.html.
# Fluxo: botao da LP -> inscricao.html (nome, e-mail, WhatsApp) -> checkout (plataforma de pagamento) -> obrigado.html
import html
from dados import WHATS
import componentes

def logo_svg(d):
    return '<img src="logo.png" alt="A Nova Profissão" height="52">'

# favicon: as tres barras verdes da logo
ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#000"/>'
        '<rect x="14" y="12" width="9" height="40" fill="#22e06b"/><rect x="28" y="12" width="9" height="40" fill="#22e06b"/>'
        '<rect x="42" y="12" width="9" height="40" fill="#22e06b"/></svg>')

E = html.escape

# ---- Pendencias (preencha e rode: python3 src/gerar.py) ----
HORARIO = "20h"            # horario de Brasilia (cada noite tem cerca de 2 horas)
INSCRICAO_URL = "inscricao.html"   # todos os botoes de compra levam ao formulario curto
CHECKOUT_URL = "#"         # link do checkout na plataforma de pagamento (o formulario leva para ele)
LEAD_WEBHOOK = None        # opcional: endereco que recebe nome/e-mail/WhatsApp (CRM, planilha, automacao)
GRUPO_URL = "#"            # link do grupo (ou Comunidade) de WhatsApp dos participantes
PRECO = "R$ 97"
POLITICA_URL, TERMOS_URL = "#", "#"
DATAS = "20 a 22 de janeiro"

# Headlines do roteiro revisado. Troque HEADLINE (1 a 5) e rode: python3 src/gerar.py
HEADLINES = {
 1: 'As empresas da sua cidade precisam de quem as ajude a vender. <em>Essa pessoa pode ser você.</em>',
 2: 'Em 3 noites ao vivo, descubra como se tornar o <em>Estrategista Comercial</em> que as empresas da sua cidade procuram.',
 3: 'Construa uma nova profissão ajudando empresas a vender mais, <em>com renda e autonomia</em> na sua própria cidade.',
 4: 'Empresas pagam por quem treina a equipe, organiza o processo e faz o faturamento crescer. <em>Conheça a profissão de Estrategista Comercial.</em>',
 # 5 = junta as ideias das quatro: Seja (1) + Estrategista Comercial (2 e 4) + empresas da sua cidade procuram (1, 2 e 3) + nova profissao com autonomia (3)
 5: 'Seja o <em>Estrategista Comercial</em> que as empresas da sua cidade procuram: uma nova profissão, com autonomia.',
}
HEADLINE = 5   # 5 = frase unica que junta as quatro (1 era a recomendada no roteiro)

SUBHEADLINE = ('Em 3 noites ao vivo, Daniel Pereira, que em 10 anos já ajudou mais de 22 mil empresas, mostra o passo a passo para você se tornar '
               'um Estrategista Comercial, vender seu serviço para empresas e chegar ao seu primeiro contrato.')

NAV = [("oportunidade", "Oportunidade"), ("dias", "As 3 noites"), ("mentor", "Quem ensina"), ("faq", "Dúvidas")]

def lis(x): return ''.join(f'<li>{E(i)}</li>' for i in x)
def paras(x): return ''.join(f'<p>{E(i)}</p>' for i in x)
def hd(label, titulo, lead=''):
    l = f'<p class="lead">{E(lead)}</p>' if lead else ''
    lb = f'<span class="label">{E(label)}</span>' if label else ''
    return f'<div class="hd">{lb}<h2>{E(titulo)}</h2>{l}</div>'

def head(s, titulo, desc, noindex=False):
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titulo)}</title><meta name="description" content="{E(desc)}">{robots}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"><link rel="icon" href="icon.svg">
<style>:root{{--accent:{s['accent']};--sec:{s['sec']};--sec2:{s['sec2']};--tint:{s['tint']}}}</style>
</head><body class="ev">'''

def rodape(s):
    logo = logo_svg(s['dir'])
    return f'''<footer><div class="wrap"><div class="flogo">{logo}</div>
<p>Negócio Fora da Curva</p>
<p><a class="ac" href="{POLITICA_URL}">Política de privacidade</a> · <a class="ac" href="{TERMOS_URL}">Termos de uso</a> · <a class="ac" href="https://wa.me/{WHATS}" target="_blank" rel="noopener">Contato</a></p>
<p>Os resultados variam de pessoa para pessoa e dependem da aplicação do método. Este evento não é promessa de ganho financeiro.</p>
<p>Este site não é afiliado ao Google, à Meta ou a outra plataforma.</p></div></footer>'''

def vendas(s, hl=None, rotulo=False):
    hl = hl or HEADLINE
    logo = logo_svg(s['dir'])
    # (numero, dia da semana, rotulo, titulo, texto)
    noites = [("20", "Quarta", "Noite 1", "A oportunidade", "Por que as empresas precisam de Estrategistas Comerciais, o que elas buscam e por que 2027 é o momento de começar."),
              ("21", "Quinta", "Noite 2", "O método", "Os três entregáveis do Estrategista Comercial (treinar a equipe, estruturar o processo e usar os dados), mostrados em um caso real."),
              ("22", "Sexta", "Noite 3", "O caminho", "Como sair do zero e chegar ao primeiro contrato: onde encontrar, como abordar e como fechar a primeira empresa da sua cidade. Nesta noite, Daniel também apresenta a formação online O Estrategista Comercial, para quem quiser continuar com acompanhamento.")]
    ticket = ''.join(f'<div class="tk"><div class="dt"><i class="live-pill">Ao vivo</i><em class="nn">{n}</em><b>{d}/01</b><span>{w.upper()} · {HORARIO}</span></div><h3>{E(t)}</h3></div>' for d, w, n, t, _ in noites)
    chips = ''.join(f'<button type="button" class="{"on" if k == 0 else ""}" data-n="{n}" data-w="{d} · {w}" data-t="{E(t)}" data-x="{E(x)}" aria-pressed="{"true" if k == 0 else "false"}"><b>{d}</b><span>{n}/01</span></button>' for k, (n, w, d, t, x) in enumerate(noites))
    n0, w0, d0, t0, x0 = noites[0]
    tabs = (f'<div class="dscene" id="dscene"><div class="dbig" id="dbig">{n0}<em>/01</em></div><div class="dtxt"><small id="dsmall"><i class="live-pill">Ao vivo</i> {d0} · {w0}</small>'
            f'<h3 id="dtitle">{E(t0)}</h3><p id="dtext">{E(x0)}</p></div></div><div class="dchips">{chips}</div>')
    entreg = [("Treina a equipe de vendas", "Prepara os vendedores para atender e fechar melhor."),
              ("Estrutura o processo comercial", "Organiza como a empresa prospecta, atende e acompanha clientes."),
              ("Acompanha os dados para não perder vendas", "Usa os números para a empresa vender mais.")]
    cenario = [("A empresa vende no improviso", "A maioria das pequenas e médias empresas não tem processo comercial, a equipe não é treinada e ninguém acompanha os números. O cliente que não fechou na hora é esquecido."),
               ("O dono não tem a quem recorrer", "Ele sabe que precisa de ajuda. Mas as grandes consultorias não atendem o negócio dele, e contratar um diretor comercial custa caro demais."),
               ("Falta quem ocupe esse lugar", "Entre o improviso e a consultoria cara, existe um espaço aberto na sua cidade: o de quem ajuda a empresa a vender de forma organizada.")]
    cards_ent = ''.join(f'<div class="card"><div class="n">{i+1}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(entreg))
    faq = [("Preciso ter experiência como consultor?", "Não. O evento começa do zero e mostra o caminho completo, da primeira conversa ao primeiro contrato."),
           ("Funciona na minha cidade, mesmo sendo pequena?", "Sim. Toda cidade tem empresas que precisam vender mais, e em cidades menores há menos concorrência de consultores."),
           ("E se eu não puder assistir ao vivo?", "Você pode adicionar as gravações dos 3 dias na hora da compra. O replay da última noite fica disponível para todos os participantes até 28/01."),
           ("Onde vai acontecer?", "Online, em uma área exclusiva para participantes. O acesso chega por e-mail e WhatsApp logo após a compra."),
           ("Que horário?", f"De {DATAS}, às {HORARIO}, horário de Brasília. Cada noite tem cerca de 2 horas."),
           ("Vai ter venda de curso no evento?", "Sim. Nas noites 1 e 2 o foco é o conteúdo. Na noite 3, Daniel apresenta a formação online O Estrategista Comercial, para quem quiser continuar. A compra é opcional, e o conteúdo do evento vale por si."),
           ("Vou ganhar dinheiro depois do evento?", "O evento mostra o método e o caminho para fechar seus primeiros contratos. O resultado depende da sua dedicação e da aplicação do que você aprender."),
           ("E se eu não gostar?", "Você tem 7 dias de garantia e recebe 100% do valor de volta.")]
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    include = [f"Acesso aos 3 dias ao vivo, de {DATAS}, às {HORARIO}", "Material de apoio para acompanhar as aulas", "Grupo exclusivo de participantes", "Certificado de participação"]
    cta = lambda txt: f'<p class="cta-c"><a class="btn lg" href="{INSCRICAO_URL}">{txt}</a></p>'
    marca = f'<div class="vtag">Versão {hl} de 5 · headline {hl} (versão de teste)</div>' if rotulo else ''
    return head(s, "A Nova Profissão: evento ao vivo de 20 a 22 de janeiro",
        "Em 3 noites ao vivo, Daniel Pereira mostra o passo a passo para você se tornar um Estrategista Comercial e chegar ao seu primeiro contrato.") + f'''
{{VERSAO}}
{componentes.topo(s['dir'], logo, NAV, 'Garantir minha vaga', INSCRICAO_URL)}

<div class="cena" id="cena"><div class="cena-sticky">
<canvas id="gl" aria-hidden="true"></canvas>
<div class="cena-vig"></div>
<div class="ov ov0" id="ov0"><div class="wrap"><span class="strip">Evento ao vivo e online · 3 noites</span></div></div>
<div class="ov ov1" id="ov1"><div class="wrap"><div class="sidelogo"><img src="logo.png" alt="A Nova Profissão"></div><div class="hl">
<span class="strip estatico">Evento ao vivo e online · 3 noites</span>
<h1>{HEADLINES[hl]}</h1>
<p class="sub">{E(SUBHEADLINE)}</p>
<p class="cta-c"><a class="btn lg" href="{INSCRICAO_URL}">Quero garantir minha vaga</a></p>
<div class="trust"><span>Pagamento seguro</span><span>Garantia de 7 dias</span></div>
</div></div></div>
<div class="ov ov2" id="ov2"><div class="wrap"><span class="live-pill big">Ao vivo</span>
<div class="giant">20/01 · 21/01 · 22/01</div><p class="gsub">3 noites online · sempre às {HORARIO} (horário de Brasília)</p>
</div></div>
<div class="hint" id="hint"><span>Role para entrar</span><i></i></div>
</div></div>

<div class="ticket"><div class="wrap"><div class="tks">{ticket}</div></div></div>

<section id="situacao"><div class="wrap">
<div class="hd hd-big"><h2>O seu problema não é <em>talento</em></h2><p class="lead">Talvez você esteja nesta situação.</p></div>
<div class="split">
<div class="box"><h3>Você tem experiência em vendas</h3><p>É palestrante, mentor ou treinador. Tem conteúdo, tem palco e tem gente que admira o seu trabalho.</p><p><b>Mas, na hora de vender para uma empresa, falta:</b></p><ul class="lst no">{lis(["Método", "Proposta", "Uma estrutura de serviços que pague as contas todo mês"])}</ul></div>
<div class="box"><h3>Você está em transição</h3><p>É administrador, trabalha na área de RH ou está mudando de carreira.</p><p><b>E procura:</b></p><ul class="lst yes">{lis(["Uma forma de viver da sua experiência profissional"])}</ul></div>
</div>
<p class="callout col">O que falta é um projeto que faça o empresário querer te contratar.</p>
<p class="col prose" style="margin-top:22px;text-align:center">O empresário procura quem entregue muito mais que uma palestra motivacional. No fim do mês, ele quer ver o faturamento crescer.</p>
</div></section>

<section id="oportunidade"><div class="wrap">
<div class="hd hd-big"><h2>A oportunidade de ter uma <em>nova profissão</em></h2><p class="lead">Existe uma profissão que as empresas precisam e quase ninguém ocupa na sua cidade.</p></div>
<div class="grid3">{''.join(f'<div class="card"><div class="n">{i+1}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(cenario))}</div>
<p class="callout col" style="margin-top:28px">É aí que entra o <b>Estrategista Comercial</b>: o profissional que treina a equipe, organiza o processo de vendas e usa os dados para a empresa vender mais. É a nova profissão, e quase ninguém na sua cidade ocupa esse lugar ainda.</p>
<h3 class="h3c">Os três entregáveis do Estrategista Comercial</h3>
<div class="grid3">{cards_ent}</div>
</div></section>

<section id="dias"><div class="wrap">
{hd("As 3 noites", "O que você vai ver em 3 noites ao vivo")}
{tabs}
<div class="split" style="margin-top:56px">
<div class="box"><h3>Este evento é para você se…</h3><ul class="lst yes">{lis(["É vendedor e quer transformar sua experiência em um negócio próprio.", "É coach, palestrante, mentor ou treinador e quer vender para empresas.", "Já lidera ou já liderou equipes comerciais.", "Quer uma carreira com liberdade de agenda e ganhos que não dependem de salário.", "Está parado, mas sabe que tem potencial para mais."])}</ul></div>
<div class="box"><h3>Não é para você se…</h3><ul class="lst no">{lis(["Procura dinheiro rápido sem esforço.", "Não gosta de conversar com empresários.", "Não está disposto a aplicar o que aprender."])}</ul></div>
</div></div></section>

<section id="mentor"><div class="wrap">
{hd("Quem ensina", "Quem vai te guiar nesta nova profissão")}
<div class="grid3 stt"><div class="st"><strong><span data-to="10">10</span> anos</strong><span>na área comercial</span></div><div class="st"><strong>+<span data-to="22">22</span> mil</strong><span>empresas ajudadas</span></div><div class="st"><strong><span data-to="230">230</span> mil</strong><span>seguidores</span></div></div>
<div class="col prose" style="margin-top:44px">{paras([
 "Daniel Pereira é fundador do Negócio Fora da Curva. Há 10 anos, ele entra em empresas para treinar equipes, organizar processos comerciais e fazer o faturamento crescer. Nesse tempo, ajudou mais de 22 mil empresas. Agora, pela primeira vez, vai ensinar o método completo para quem quer fazer esse trabalho como profissão."])}</div>
<p class="callout col">“Passei 10 anos fazendo isso dentro das empresas. Agora quero formar pessoas que façam o mesmo na cidade delas.”</p>
<!-- PROVA SOCIAL ("O que dizem os empresarios que aplicaram o metodo"): inserir aqui apenas depoimentos reais e com autorizacao de uso de imagem assinada
     (video de empresario do varejo, empresario de servicos, prints de mensagens, fotos de palestras com plateia cheia). -->
</div></section>

<section id="oferta"><div class="wrap">
{hd("Ingresso", "Garanta seu lugar nas 3 noites ao vivo", "Menos do que um jantar fora, para conhecer uma profissão que pode mudar a sua carreira.")}
<div class="offer"><span class="tag">Evento ao vivo · {DATAS} · {HORARIO}</span>
<div class="price">{PRECO}</div><div class="pn">por apenas {PRECO}</div>
<ul>{lis(include)}</ul>
<div class="bonus1"><small>Bônus do 1º lote</small><b>Aula extra: “O roteiro da primeira reunião com o empresário”</b><span>Só para quem comprar até 20/12.</span></div>
<a class="btn lg" href="{INSCRICAO_URL}">Quero garantir minha vaga por {PRECO}</a><div class="s">O bônus do 1º lote acaba em 20/12. Pagamento seguro · Garantia de 7 dias</div></div>
<div class="guar" style="margin-top:34px"><b>7</b><div><strong>Risco zero para você</strong><p style="color:var(--muted);margin-top:6px">Você tem 7 dias de garantia. Se por qualquer motivo achar que o evento não é para você, devolvemos 100% do valor, sem perguntas.</p></div></div>
</div></section>

<section id="faq"><div class="wrap">{hd("Dúvidas", "Perguntas frequentes")}<div class="faq col">{faq_html}</div></div></section>

<section class="final"><div class="wrap"><h2>Daqui a um ano, você vai desejar ter começado hoje.</h2>
<p class="lead">As empresas da sua cidade vão continuar perdendo vendas. A pergunta é quem vai ajudá-las: você ou outra pessoa.</p>
<p class="cta-c"><a class="btn lg" href="{INSCRICAO_URL}">Sim, quero a nova profissão por {PRECO}</a></p></div></section>

{componentes.rodape(s['dir'], logo, NAV)}
<div class="fix"><b>{PRECO}</b><a class="btn sm" href="{INSCRICAO_URL}">Garantir vaga</a></div>
<script src="three.min.js" defer></script>
<script src="cena3d.js" defer></script>
<script src="interativo.js" defer></script>
<script>document.querySelectorAll('#links a').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('links').classList.remove('open')}})}});</script>
</body></html>'''.replace('{VERSAO}', marca)

FORM_JS = '''
(function () {
  var f = document.getElementById('f'), ck = '__CHECKOUT__', hook = '__HOOK__';
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(f), dados = { nome: d.get('nome'), email: d.get('email'), whatsapp: d.get('whatsapp') };
    if (hook) { try { fetch(hook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados), keepalive: true }).catch(function () {}); } catch (x) {} }
    if (ck === '#') { document.getElementById('prev').hidden = false; return; }
    var u = new URL(ck, location.href);
    u.searchParams.set('name', dados.nome); u.searchParams.set('email', dados.email); u.searchParams.set('phone', dados.whatsapp);
    new URLSearchParams(location.search).forEach(function (v, k) { if (!u.searchParams.has(k)) u.searchParams.set(k, v); }); // mantem UTMs
    location.href = u.toString();
  });
})();
'''

def inscricao(s):
    logo = logo_svg(s['dir'])
    js = FORM_JS.replace('__CHECKOUT__', CHECKOUT_URL).replace('__HOOK__', LEAD_WEBHOOK or '')
    return head(s, "Inscrição: A Nova Profissão", "Informe seus dados para receber o acesso ao evento.", noindex=True) + f'''
<nav><div class="wrap"><a class="logo" href="index.html">{logo}</a><span class="seg">Inscrição segura</span></div></nav>
<section style="border:0"><div class="wrap" style="max-width:560px">
<span class="label">Quase lá</span><h1 style="font-size:clamp(1.8rem,5vw,2.6rem);margin-bottom:12px">Para onde enviamos o seu acesso?</h1>
<p class="lead" style="margin-bottom:26px">Os lembretes das 3 noites ao vivo ({DATAS}, às {HORARIO}) chegam por e-mail e WhatsApp.</p>
<form class="form" id="f" style="margin:0">
<label>Nome completo<input name="nome" required autocomplete="name"></label>
<label>E-mail<input name="email" type="email" required autocomplete="email" inputmode="email"></label>
<label>WhatsApp (com DDD)<input name="whatsapp" type="tel" required autocomplete="tel" inputmode="tel" placeholder="(00) 00000-0000"></label>
<button class="btn lg" type="submit" style="width:100%">Ir para o pagamento</button>
<p class="fine" style="text-align:center;margin:0">Pagamento seguro · Garantia de 7 dias · Ao continuar, você concorda com a <a class="ac" href="{POLITICA_URL}">política de privacidade</a>.</p>
</form>
<p id="prev" hidden class="callout" style="margin-top:22px;font-size:1rem">Pré-visualização: neste ponto a pessoa segue para o pagamento. O link da plataforma de pagamento ainda não foi configurado.</p>
</div></section>
{rodape(s)}
<script>{js}</script>
</body></html>'''

def obrigado(s):
    logo = logo_svg(s['dir'])
    agenda = ("https://calendar.google.com/calendar/render?action=TEMPLATE&text=A+Nova+Profiss%C3%A3o+(evento+ao+vivo)"
              "&dates=20270120T230000Z/20270121T010000Z&recur=RRULE%3AFREQ%3DDAILY%3BCOUNT%3D3&details=Evento+ao+vivo+e+online.+20%2C+21+e+22+de+janeiro%2C+%C3%A0s+20h+(hor%C3%A1rio+de+Bras%C3%ADlia)")
    return head(s, "Parabéns! Seu lugar está garantido", "Seu ingresso para A Nova Profissão está confirmado.", noindex=True) + f'''
<nav><div class="wrap"><a class="logo" href="index.html">{logo}</a></div></nav>
<section style="border:0"><div class="wrap" style="max-width:720px">
<span class="label">Compra confirmada</span><h1 style="font-size:clamp(2rem,5vw,3.2rem);margin-bottom:12px">Parabéns! Seu lugar está garantido.</h1>
<p class="lead">Falta só um passo para você não perder nada.</p>
<ol class="steps3">
<li><b>Entre no grupo exclusivo de participantes no WhatsApp.</b><a class="btn" href="{GRUPO_URL}" target="_blank" rel="noopener">Entrar no grupo agora</a></li>
<li><b>Coloque na agenda: 20, 21 e 22 de janeiro, às {HORARIO}.</b><a class="btn ghost" href="{agenda}" target="_blank" rel="noopener">Adicionar ao Google Agenda</a></li>
<li><b>Confira seu e-mail.</b><span>O acesso à área do evento chega por e-mail e WhatsApp logo após a confirmação da compra.</span></li></ol>
<!-- VIDEO DO DANIEL (ate 60s): agradecer, reforcar a importancia de estar ao vivo nos 3 dias e adiantar uma curiosidade da noite 3. -->
<p style="margin-top:30px"><a class="btn" href="{GRUPO_URL}" target="_blank" rel="noopener">Entrar no grupo agora</a></p>
</div></section>
{rodape(s)}</body></html>'''

def paginas(s):
    out = {'index.html': vendas(s), 'inscricao.html': inscricao(s), 'obrigado.html': obrigado(s)}
    for n in HEADLINES:
        out[f'versao-{n}.html'] = vendas(s, hl=n, rotulo=True)
    return out
