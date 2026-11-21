# Logos em SVG (vetor). Versoes: horizontal/vertical, tema escuro/claro, partes (icone/texto).
SANS = "Inter,'Helvetica Neue',Arial,sans-serif"

# CSS da animacao da logo laranja (seta que se desenha, ponta que "estoura", brilho que respira)
ANIM_CSS = '''
.lg-anim{overflow:visible}
.lg-shaft{stroke-dasharray:1;stroke-dashoffset:1;animation:lgdraw 1.1s cubic-bezier(.6,0,.2,1) .25s forwards}
.lg-head{transform-box:fill-box;transform-origin:50% 100%;animation:lgpop .5s cubic-bezier(.3,1.7,.5,1) 1.2s both}
.lg-glow{animation:lgglow 3.2s ease-in-out 1.9s infinite}
.lg-t1{animation:lgin .7s cubic-bezier(.2,.8,.2,1) 1s both}
.lg-t2{animation:lgin .7s cubic-bezier(.2,.8,.2,1) 1.4s both}
@keyframes lgdraw{to{stroke-dashoffset:0}}
@keyframes lgpop{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes lgin{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}
@keyframes lgglow{0%,100%{filter:drop-shadow(0 0 2px rgba(255,123,28,.30))}50%{filter:drop-shadow(0 0 9px rgba(255,123,28,.80))}}
@media (prefers-reduced-motion:reduce){.lg-shaft,.lg-head,.lg-glow,.lg-t1,.lg-t2{animation:none!important;stroke-dashoffset:0!important}}
'''

def _arrow(theme, animate):
    """Seta em V (referencia NFC): traco com borda escura e miolo claro + ponta."""
    lo, hi = ('#c2540a', '#ff8a2b') if theme == 'dark' else ('#9c4208', '#f06a0c')
    pa = ' pathLength="1" class="lg-shaft"' if animate else ''
    ha = ' class="lg-head"' if animate else ''
    p = 'M10 28L30 54L50 14'
    return (f'<g class="lg-glow">' if animate else '<g>') + (
        f'<path d="{p}" fill="none" stroke="{lo}" stroke-width="9.5" stroke-linejoin="miter"{pa}/>'
        f'<path d="{p}" fill="none" stroke="{hi}" stroke-width="5" stroke-linejoin="miter"{pa}/>'
        f'<g{ha}><polygon points="54.9,3.2 59.2,18.4 40.8,9.4" fill="{lo}" stroke="{lo}" stroke-width="1.2" stroke-linejoin="miter"/>'
        f'<polygon points="53.2,7.6 55.8,15.4 46,10.6" fill="{hi}"/></g></g>')

def _icon(d, theme, animate=False):
    dark = theme == 'dark'
    if d == 'site-97-verde':
        return ('<rect x="2" y="2" width="60" height="60" rx="14" fill="#22e06b"/>'
                '<path d="M19 47V19L41 43V26" fill="none" stroke="#000" stroke-width="6.5" stroke-linejoin="round" stroke-linecap="round"/>'
                '<path d="M41 11L50 24H32Z" fill="#000" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
    if d == 'site-2997-azul':
        return ('<path d="M32 3L58 18V46L32 61L6 46V18Z" fill="#071426" stroke="#3b95ff" stroke-width="3.5" stroke-linejoin="round"/>'
                '<path d="M17 43L28 33L38 37L47 21" fill="none" stroke="#3b95ff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                '<circle cx="17" cy="43" r="4" fill="#3b95ff"/><circle cx="28" cy="33" r="4" fill="#3b95ff"/><circle cx="38" cy="37" r="4" fill="#3b95ff"/>'
                '<circle cx="47" cy="21" r="5.5" fill="#fff"/>')
    return _arrow(theme, animate)

# linhas de texto: (texto, tamanho, peso, espacamento, cor 'm'(principal)|'a'(destaque), fonte)
BRANDS = {
 'site-97-verde': dict(slug='97-verde', nome='A Nova Profissão', accent='#22e06b', accent_light='#0e9f4b',
   hw=232, vw=210, hx=76, hy=[30, 54], vy=[100, 124],
   lines=[('A NOVA', 23, 900, .6, 'm', SANS), ('PROFISSÃO', 23, 900, .6, 'a', SANS)]),
 'site-2997-azul': dict(slug='2997-azul', nome='Estrategista Comercial', accent='#3b95ff', accent_light='#1a6fd6',
   hw=282, vw=250, hx=76, hy=[31, 53], vy=[100, 124],
   lines=[('ESTRATEGISTA', 21, 900, 1.4, 'm', SANS), ('COMERCIAL', 15, 700, 6.6, 'a', SANS)]),
 'site-licenciado-laranja': dict(slug='licenciado-laranja', nome='Licenciado Fora da Curva', accent='#ff7b1c', accent_light='#c2540a',
   hw=292, vw=232, hx=76, hy=[31, 53], vy=[100, 124],
   lines=[('FORA DA CURVA', 21, 900, 1.2, 'm', SANS), ('LICENCIADO', 12, 700, 8.2, 'a', SANS)]),
}

def _text(d, layout, theme, animate=False):
    B = BRANDS[d]
    main = '#f1f1f1' if theme == 'dark' else '#0b0b0b'
    acc = B['accent'] if theme == 'dark' else B['accent_light']
    out = ''
    for i, (t, size, w, sp, c, fam) in enumerate(B['lines']):
        fill = main if c == 'm' else acc
        cls = f' class="lg-t{i+1}"' if animate else ''
        if layout == 'h':
            x = B['hx'] + (1 if (d == 'site-2997-azul' and i == 1) else 0)
            out += f'<text{cls} x="{x}" y="{B["hy"][i]}" font-family="{fam}" font-weight="{w}" font-size="{size}" letter-spacing="{sp}" fill="{fill}">{t}</text>'
        else:
            cx = B['vw'] / 2 + sp / 2
            out += f'<text{cls} x="{cx}" y="{B["vy"][i]}" text-anchor="middle" font-family="{fam}" font-weight="{w}" font-size="{size}" letter-spacing="{sp}" fill="{fill}">{t}</text>'
    return out

def make_logo(d, layout='h', theme='dark', part='all', animate=False):  # theme: dark (fundo escuro) | light (fundo claro)
    B = BRANDS[d]; icon = _icon(d, theme, animate)
    if layout == 'h':
        W = B['hw']
        if part == 'icon':   vb, body = '0 0 64 64', icon
        elif part == 'text': vb, body = f'{B["hx"]-2} 0 {W-B["hx"]+2} 64', _text(d, 'h', theme, animate)
        else:                vb, body = f'0 0 {W} 64', icon + _text(d, 'h', theme, animate)
    else:
        W = B['vw']
        if part == 'icon':   vb, body = '0 0 64 64', icon
        elif part == 'text': vb, body = f'0 80 {W} 56', _text(d, 'v', theme, animate)
        else:
            vb = f'0 0 {W} 136'
            body = f'<g transform="translate({W/2-32} 0)">{icon}</g>' + _text(d, 'v', theme, animate)
    h = vb.split()[3]
    cls = ' class="lg-anim"' if animate else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" height="{h}" role="img" aria-label="{B["nome"]}"{cls}>{body}</svg>'

def logo_svg(d, animate=False):  return make_logo(d, 'h', 'dark', 'all', animate)
def icon_svg(d):  return make_logo(d, 'h', 'dark', 'icon')
def icon_only(d, theme='dark'): return make_logo(d, 'h', theme, 'icon')
