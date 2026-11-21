import os, html
from dados import SITES, WHATS
from logos import logo_svg, icon_svg, make_logo, ANIM_CSS
from urllib.parse import quote
import componentes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = open(os.path.join(ROOT, 'src', 'style.css')).read()
E = html.escape

def lis(x): return ''.join(f'<li>{E(i)}</li>' for i in x)


def sec_mercado(m):
    st = ''.join(f'<div class="st"><strong>{E(a)}</strong><span>{E(b)}</span></div>' for a, b in m['stats'])
    pt = ''.join(f'<div class="pt"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in m['pontos'])
    return (f'<section id="mercado"><div class="wrap"><span class="label">Mercado</span><h2>{E(m["h"])}</h2><p class="lead">{E(m["p"])}</p>'
            f'<div class="stats3">{st}</div><div class="pts">{pt}</div><p class="disc">{E(m["fonte"])}</p></div></section>')

def sec_fases(f):
    out = ''
    for lab, tit, dias in f['itens']:
        d = ''.join(f'<div class="dia"><small>{E(dn)}</small><h4>{E(dt)}</h4><ul>{lis(b)}</ul></div>' for dn, dt, b in dias)
        out += f'<div class="fase"><div class="fh"><span>{E(lab)}</span><h3>{E(tit)}</h3></div><div class="dias">{d}</div></div>'
    return f'<section id="conteudo"><div class="wrap"><span class="label">Programa</span><h2>{E(f["h"])}</h2><p class="lead">{E(f["p"])}</p>{out}</div></section>'

def sec_formas(f):
    c = ''.join(f'<div class="box"><span class="label">{E(a)}</span><h3>{E(b)}</h3><p class="mt">{E(t)}</p></div>' for a, b, t in f['itens'])
    return f'<section id="formas"><div class="wrap"><span class="label">Aplicação</span><h2>{E(f["h"])}</h2><p class="lead">{E(f["p"])}</p><div class="split">{c}</div></div></section>'

def sec_plano(p):
    ps = ''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in p['passos'])
    rows = ''.join(f'<tr class="{"hl" if h else ""}"><td>{E(a)}</td><td>{E(b)}</td></tr>' for a, b, h in p['conta'])
    return (f'<section id="plano"><div class="wrap"><span class="label">Plano de faturamento</span><h2>{E(p["h"])}</h2><p class="lead">{E(p["p"])}</p>'
            f'<div class="split"><div class="box"><h3>O que cada contrato entrega</h3><ol class="pl">{ps}</ol></div>'
            f'<div class="box"><h3>A conta</h3><table class="conta">{rows}</table></div></div><p class="disc">{E(p["nota"])}</p></div></section>')

def pagina(s):
    nav = ''.join(f'<a href="#{a}">{b}</a>' for a, b in s['nav'])
    trust = ''.join(f'<span>{E(t)}</span>' for t in s['trust'])
    funnel = ''.join(f'<div class="fn"><b>{E(a)}</b><small>{E(b)}</small><i style="width:{100-i*20}%"></i></div>' for i, (a, b) in enumerate(s['funnel']))
    band = ''.join(f'<div class="it"><strong>{a}</strong><span>{b}</span></div>' for a, b in s['band'])
    pillars = ''.join(f'<div class="card"><div class="n">{i+1}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(s['pillars']))
    mods = ''.join(f'<details{" open" if i==0 else ""}><summary><span><em>{i+1:02d}</em>{E(a)}</span></summary><ul>{lis(b)}</ul></details>' for i, (a, b) in enumerate(s['mods']))
    tl = ''.join(f'<div class="it"><small>{a}</small><h3>{E(b)}</h3><p>{E(c)}</p></div>' for a, b, c in s['timeline'])
    earn = ''.join(f'<div class="e"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in s['earn'])
    bonus = ''.join(f'<div class="bn"><small>Bônus {i+1}</small><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(s['bonus']))
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in s['faq'])
    form = ''
    if s.get('form'):
        form = '''<section id="candidatura"><div class="wrap center">
<span class="label">Candidatura</span><h2>Candidate-se à licença <em>NFC</em></h2>
<p class="lead">Preencha os dados. Ao enviar, abre uma conversa no WhatsApp com a equipe, já com as suas respostas.</p>
<form class="form" onsubmit="return enviar(event)">
<label>Nome completo<input name="n" required></label>
<div class="c2"><label>WhatsApp<input name="w" required inputmode="tel"></label><label>Cidade e estado<input name="c" required></label></div>
<div class="c2"><label>Experiência com vendas<select name="e"><option>Menos de 2 anos</option><option>2 a 5 anos</option><option>5 a 10 anos</option><option>Mais de 10 anos</option></select></label>
<label>Atua com consultoria ou gestão comercial?<select name="f"><option>Sim</option><option>Não</option></select></label></div>
<label>Por que você quer ser licenciado?<textarea name="m" rows="3"></textarea></label>
<button class="btn" type="submit">Enviar candidatura</button></form></div></section>'''
    mercado = sec_mercado(s['mercado']) if s.get('mercado') else ''
    formas = sec_formas(s['formas']) if s.get('formas') else ''
    plano = sec_plano(s['plano']) if s.get('plano') else ''
    if s.get('fases'):
        conteudo = sec_fases(s['fases'])
    else:
        conteudo = f'<section id="conteudo"><div class="wrap"><span class="label">Conteúdo</span><h2>{E(s["mods_h"])}</h2><p class="lead">{E(s["mods_p"])}</p><div class="acc">{mods}</div></div></section>'
    logo = logo_svg(s['dir'])
    topo = componentes.topo(s['dir'], logo_svg(s['dir'], animate=bool(s.get('animate'))), s['nav'], s.get('cta_nav', s['cta']))
    rodape = componentes.rodape(s['dir'], logo, s['nav'])
    logo_nav = logo_svg(s['dir'], animate=bool(s.get('animate')))
    hero_mark = f'<div class="bigmark">{make_logo(s["dir"], "h", "dark", "icon", True)}</div>' if s.get('hero_mark') else ''
    cabeca = f'<span class="tag">{E(s["tag"])}</span><h1>{s["h1"]}</h1>'
    corpo = (f'<p class="sub">{E(s["sub"])}</p>'
             f'<div class="ctas"><a class="btn" href="#oferta">{E(s["cta"])}</a><a class="btn ghost" href="#metodo">Ver como funciona</a></div>'
             f'<div class="trust">{trust}</div>')
    painel = f'<div class="mock sq">{hero_mark}<h4>{E(s["funnel_title"])}</h4>{funnel}</div>'
    cls = 'hero long' if s.get('long_h1') else 'hero'
    hero = f'<header class="{cls}"><div class="wrap"><div>{cabeca}{corpo}</div>{painel}</div></header>'
    fav = '<link rel="icon" href="icon.svg">'
    return f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(s['title'])}</title><meta name="description" content="{E(s['desc'])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900{'&family=Cormorant+Garamond:wght@700' if s.get('serif') else ''}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">{fav}
<style>:root{{--accent:{s['accent']};--sec:{s['sec']};--sec2:{s['sec2']};--tint:{s['tint']}}}</style>
</head><body>
{topo}

{hero}
<div class="band"><div class="wrap">{band}</div></div>

<section id="problema"><div class="wrap">
<span class="label">O problema</span><h2>{s['problem_h']}</h2><p class="lead">{E(s['problem_p'])}</p>
<div class="split"><div class="box"><h3>{E(s.get('no_h','Sem estratégia'))}</h3><ul class="lst no">{lis(s['no'])}</ul></div>
<div class="box"><h3>{E(s.get('yes_h','Com estratégia'))}</h3><ul class="lst yes">{lis(s['yes'])}</ul></div></div>
</div></section>

{mercado}

<section id="metodo"><div class="wrap">
<span class="label">Método</span><h2>{E(s['pillars_h'])}</h2><p class="lead">{E(s['pillars_p'])}</p>
<div class="grid">{pillars}</div></div></section>

{conteudo}
{formas}
{plano}

<section><div class="wrap"><span class="label">Passo a passo</span><h2>{E(s['tl_h'])}</h2><br><div class="tl">{tl}</div></div></section>

<section id="ganhos"><div class="wrap">
<span class="label">Retorno</span><h2>{E(s['earn_h'])}</h2><p class="lead">{E(s['earn_p'])}</p>
<div class="earn">{earn}</div>
<p class="disc">Os resultados dependem de dedicação, aplicação do método e condições de mercado. Não há garantia de ganhos.</p></div></section>

<section><div class="wrap"><span class="label">Bônus</span><h2>Incluso no valor</h2><br><div class="bonus">{bonus}</div></div></section>

<section><div class="wrap"><div class="split">
<div><span class="label">Perfil</span><h2>Para quem é</h2><br><ul class="lst yes">{lis(s['forwho'])}</ul></div>
<div><span class="label">Atenção</span><h2>Para quem não é</h2><br><ul class="lst no">{lis(s['notfor'])}</ul></div>
</div></div></section>

<section id="oferta"><div class="wrap center">
<span class="label">Oferta</span><h2>{s['final_h']}</h2><p class="lead">{E(s['final_p'])}</p>
<div class="offer"><span class="tag">{E(s['tag'])}</span>
<div class="price">{E(s['price'])}</div><div class="pn">{E(s['pricenote'])}</div>
<ul>{lis(s['includes'])}</ul>
<a class="btn" href="{s['link']}">{E(s['btn'])}</a><div class="s">{E(s['secure'])}</div></div>
</div></section>

<section><div class="wrap"><div class="guar"><b>{s.get('gbig','7')}</b><div><strong>{E(s['guar'])}</strong></div></div></div></section>
{form}
<section id="faq"><div class="wrap"><span class="label">Dúvidas</span><h2>Perguntas frequentes</h2><br><div class="faq">{faq}</div></div></section>

<section class="final"><div class="wrap"><h2>{s['h1']}</h2><a class="btn" href="#oferta">{E(s['cta'])}</a></div></section>

{rodape}
<div class="fix"><b>{E(s['price'])}</b><a class="btn sm" href="#oferta">{E(s['cta'])}</a></div>
<script>
document.querySelectorAll('#links a').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('links').classList.remove('open')}})}});
function enviar(ev){{ev.preventDefault();var f=new FormData(ev.target);
var t=encodeURIComponent('Candidatura de licenciado\\nNome: '+f.get('n')+'\\nWhatsApp: '+f.get('w')+'\\nCidade: '+f.get('c')+'\\nExperiência: '+f.get('e')+'\\nAtua com consultoria/gestão: '+f.get('f')+'\\nMotivo: '+f.get('m'));
window.open('https://wa.me/{WHATS}?text='+t,'_blank');return false}}
</script>
</body></html>'''

for s in SITES:
    d = os.path.join(ROOT, s['dir'])
    os.makedirs(d, exist_ok=True)
    if s['dir'] == 'site-97-verde':
        import verde
        for nome, conteudo in verde.paginas(s).items():
            open(os.path.join(d, nome), 'w').write(conteudo)
        open(os.path.join(d, 'icon.svg'), 'w').write(verde.ICON)
        open(os.path.join(d, 'interativo.js'), 'w').write(open(os.path.join(ROOT, 'src', 'verde.js')).read())
        import base64
        logo64 = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(d, 'logo.png'), 'rb').read()).decode()
        open(os.path.join(d, 'cena3d.js'), 'w').write(open(os.path.join(ROOT, 'src', 'verde3d.js')).read().replace('__LOGO_DATA__', logo64))
        open(os.path.join(d, 'three.min.js'), 'w').write(open(os.path.join(ROOT, 'src', 'vendor', 'three.min.js')).read())
    else:
        open(os.path.join(d, 'index.html'), 'w').write(pagina(s))
    open(os.path.join(d, 'style.css'), 'w').write(CSS + (ANIM_CSS if s.get('animate') else ''))
    if s['dir'] != 'site-97-verde':
        open(os.path.join(d, 'icon.svg'), 'w').write(icon_svg(s['dir']))
    print('ok', s['dir'])
