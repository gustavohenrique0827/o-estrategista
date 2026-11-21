// Interacoes do site verde: barra de progresso, surgir ao rolar, contagem de numeros,
// logo 3D que inclina com o mouse, seletor dos 3 dias e menu que marca a secao atual.
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  /* ---- barra de progresso + parallax da palavra de fundo ---- */
  var bar = document.createElement('div'); bar.className = 'prog'; document.body.appendChild(bar);
  var stage = $('#stage');
  function onScroll() {
    var h = document.documentElement;
    var p = h.scrollTop / ((h.scrollHeight - h.clientHeight) || 1);
    bar.style.transform = 'scaleX(' + Math.min(1, Math.max(0, p)) + ')';
    if (stage && !reduce) stage.style.setProperty('--py', (h.scrollTop * 0.12).toFixed(1) + 'px');
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---- surgir ao rolar (com atraso escalonado) ---- */
  var alvo = $$('.hd,.card,.dscene,.dchips,.box,.st,.offer,.guar,.faq details,.final h2,.final .lead,.callout,.prose p,.tk');
  alvo.forEach(function (el) {
    el.classList.add('rv');
    var irmaos = [].filter.call(el.parentNode.children, function (c) { return c.classList.contains('rv'); });
    el.style.transitionDelay = (irmaos.indexOf(el) * 90) + 'ms';
  });
  if (reduce || !('IntersectionObserver' in window)) {
    alvo.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    alvo.forEach(function (el) { io.observe(el); });
  }

  /* ---- contagem dos numeros ---- */
  var nums = $$('[data-to]');
  function conta(el) {
    var to = parseFloat(el.getAttribute('data-to')), t0 = null, dur = 1400;
    function f(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(to * e);
      if (p < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  }
  if (!reduce && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { conta(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { n.textContent = '0'; co.observe(n); });
  }

  /* ---- logo 3D que inclina com o mouse ---- */
  if (stage && !reduce) {
    stage.addEventListener('mousemove', function (e) {
      var r = stage.getBoundingClientRect();
      var dx = (e.clientX - r.left) / r.width - 0.5, dy = (e.clientY - r.top) / r.height - 0.5;
      stage.style.setProperty('--ry', (dx * 16).toFixed(2) + 'deg');
      stage.style.setProperty('--rx', (-dy * 12).toFixed(2) + 'deg');
    });
    stage.addEventListener('mouseleave', function () {
      stage.style.setProperty('--ry', '0deg'); stage.style.setProperty('--rx', '0deg');
    });
  }

  /* ---- seletor dos 3 dias ---- */
  var cena = $('#dscene'), chips = $$('.dchips button');
  if (cena && chips.length) {
    var atual = 0, mexeu = false, timer = null;
    var big = $('#dbig'), peq = $('#dsmall'), tit = $('#dtitle'), txt = $('#dtext');
    function vai(i, manual) {
      if (manual) { mexeu = true; clearInterval(timer); }
      if (i === atual && !manual) return;
      atual = i;
      chips.forEach(function (c, k) { c.classList.toggle('on', k === i); c.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      var b = chips[i];
      cena.classList.add('sw');
      setTimeout(function () {
        big.innerHTML = b.getAttribute('data-n') + '<em>/01</em>';
        peq.innerHTML = '<i class="live-pill">Ao vivo</i> ' + b.getAttribute('data-w');
        tit.textContent = b.getAttribute('data-t');
        txt.textContent = b.getAttribute('data-x');
        cena.classList.remove('sw');
      }, reduce ? 0 : 220);
    }
    chips.forEach(function (c, k) { c.addEventListener('click', function () { vai(k, true); }); });
    if (!reduce && 'IntersectionObserver' in window) {
      var visivel = false;
      new IntersectionObserver(function (es) { visivel = es[0].isIntersecting; }, { threshold: 0.4 }).observe(cena);
      timer = setInterval(function () { if (visivel && !mexeu) vai((atual + 1) % chips.length, false); }, 5500);
    }
  }

  /* ---- menu marca a secao atual ---- */
  var links = $$('#links a[href^="#"]').filter(function (a) { return a.getAttribute('href').length > 1; });
  var secoes = links.map(function (a) { return $(a.getAttribute('href')); });
  if ('IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    secoes.forEach(function (s) { if (s) so.observe(s); });
  }
})();
