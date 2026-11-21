# Topo (aviso + menu) e rodape completos, usados pelos tres sites.
import html
import datetime
from dados import WHATS

E = html.escape
ANO = datetime.date.today().year
INSTAGRAM = "https://instagram.com/negociosforadacurva"
INSTAGRAM_NOME = "@negociosforadacurva"
POLITICA_URL = TERMOS_URL = REEMBOLSO_URL = "#"   # TODO: links reais das paginas legais

ICON_ZAP = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M4 20l1.3-4.1A8 8 0 1 1 8.2 18.8L4 20z"/><path d="M9 9.2c.3 2.4 2.5 4.6 5 5.2l1.4-1.4-1.9-1-.9.7c-.8-.4-1.6-1.2-2-2l.7-.9-1-1.9L9 9.2z"/></svg>')
ICON_IG = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
           '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>')

# conteudo especifico de cada site
INFO = {
 'site-97-verde': dict(
   aviso='Ao vivo de 20 a 22 de janeiro, às 20h · faltam <b id="dias">--</b> dias', aviso_link='',
   desc='A Nova Profissão é um evento ao vivo do Negócio Fora da Curva, a maior escola de negócios do Tocantins, para quem quer se tornar Estrategista Comercial.',
   selos=['Pagamento seguro', 'Garantia de 7 dias', 'Suporte no WhatsApp'], reembolso=True, contagem='2027-01-20T20:00:00-03:00', marca='Negócio Fora da Curva'),
 'site-2997-azul': dict(
   aviso='Vagas limitadas · formação completa com certificação de estrategista de negócios', aviso_link='Garantir minha vaga →',
   desc='Formação Estrategista Comercial da Negócios Fora da Curva, a maior escola de negócios do Tocantins. Online, ao vivo e presencial.',
   selos=['Pagamento seguro', 'Garantia de 7 dias', 'Suporte no WhatsApp'], reembolso=True, contagem=None),
 'site-licenciado-laranja': dict(
   aviso='Candidaturas abertas · vagas limitadas por região', aviso_link='Candidatar-me →',
   desc='Licença Fora da Curva: opere a marca, o método e o sistema da Negócios Fora da Curva, a maior escola de negócios do Tocantins, na sua região.',
   selos=['Candidatura avaliada pela equipe', 'Suporte da equipe central', 'Atendimento no WhatsApp'], reembolso=False, contagem=None),
}

def topo(d, logo_html, links, cta_texto, cta_href='#oferta', home='', aviso_href=None):
    """Aviso no alto + barra de menu. links = [(ancora, rotulo)]."""
    i = INFO[d]
    aviso_href = aviso_href or cta_href
    nav = ''.join(f'<a href="{home}#{a}">{b}</a>' for a, b in links)
    logo_href = home or '#'
    js = ''
    if i.get('contagem'):
        js = ("<script>(function(){var el=document.getElementById('dias');if(!el)return;var a=new Date('" + i['contagem'] + "');"
              "var n=Math.ceil((a-new Date())/864e5);el.textContent=n>0?n:0;if(n<=0){el.parentNode.innerHTML='Evento ao vivo acontecendo agora';}})();</script>")
    return (f'<div class="aviso"><div class="wrap"><span>{i["aviso"]}</span>{(f'<a href="{aviso_href}">' + E(i["aviso_link"]) + '</a>') if i["aviso_link"] else ""}</div></div>{js}\n'
            f'<nav id="topo"><div class="wrap"><a class="logo" href="{logo_href}">{logo_html}</a>'
            f'<div class="links" id="links">{nav}<a class="zapl" href="https://wa.me/{WHATS}" target="_blank" rel="noopener">Falar no WhatsApp</a>'
            f'<a class="zap" href="https://wa.me/{WHATS}" target="_blank" rel="noopener" title="Falar no WhatsApp" aria-label="Falar no WhatsApp">{ICON_ZAP}</a>'
            f'<a class="btn sm" href="{cta_href}">{E(cta_texto)}</a></div>'
            f'<button class="burger" onclick="document.getElementById(\'links\').classList.toggle(\'open\')" aria-label="Menu">☰</button></div></nav>')

def rodape(d, logo_html, links, home=''):
    i = INFO[d]
    lk = ''.join(f'<li><a href="{home}#{a}">{E(b)}</a></li>' for a, b in links)
    legal = f'<li><a href="{POLITICA_URL}">Política de privacidade</a></li><li><a href="{TERMOS_URL}">Termos de uso</a></li>'
    if i['reembolso']:
        legal += f'<li><a href="{REEMBOLSO_URL}">Garantia e reembolso</a></li>'
    selos = ''.join(f'<span>{E(x)}</span>' for x in i['selos'])
    return f'''<footer class="rod"><div class="wrap">
<div class="rg">
<div class="rc rbrand"><div class="flogo">{logo_html}</div><p>{E(i["desc"])}</p>
<div class="soc"><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{ICON_IG}<span>{INSTAGRAM_NOME}</span></a>
<a href="https://wa.me/{WHATS}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON_ZAP}<span>WhatsApp</span></a></div></div>
<div class="rc"><h5>Navegação</h5><ul>{lk}</ul></div>
<div class="rc"><h5>Ajuda</h5><ul><li><a href="{home}#faq">Perguntas frequentes</a></li>
<li><a href="https://wa.me/{WHATS}" target="_blank" rel="noopener">Falar com a equipe</a></li>
<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li></ul></div>
<div class="rc"><h5>Informações legais</h5><ul>{legal}</ul></div>
</div>
<div class="selos">{selos}</div>
<div class="rbot"><p>© {ANO} {i.get("marca", "Negócios Fora da Curva")}. Todos os direitos reservados.</p>
<p class="rdisc">Os resultados variam de pessoa para pessoa e dependem de dedicação e da aplicação do método. Este conteúdo não é promessa de ganho financeiro. Este site não é afiliado ao Google, à Meta ou a outra plataforma.</p>
<a class="up" href="#topo">Voltar ao topo ↑</a></div>
</div></footer>'''
