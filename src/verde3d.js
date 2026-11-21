// Cena 3D em tela cheia (Three.js r128): a logo oficial com espessura, aneis de luz, chao em grade e particulas.
// Tudo centralizado e simetrico. Cenas conforme a rolagem:
//   1) abertura: logo grande no centro   2) logo sobe e o texto aparece   3) "20 . 21 . 22"
(function () {
  var sec = document.getElementById('cena'), cv = document.getElementById('gl');
  if (!sec || !cv) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var forcado = new URLSearchParams(location.search).get('p'); // ?p=0.5 fixa o progresso (para testes)
  var LOGO = '__LOGO_DATA__'; // logo embutida: funciona ate abrindo o arquivo direto do computador
  // Melhoria progressiva: a pagina ja funciona sem 3D (logo + texto). So ligamos o 3D quando tudo carregou.
  if (!window.THREE || reduce) return;

  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return; }
  var pequeno = window.innerWidth < 900;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, pequeno ? 1.5 : 2));
  renderer.outputEncoding = THREE.sRGBEncoding;

  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x000000, 0.05);
  var camera = new THREE.PerspectiveCamera(38, 1, 0.1, 120);
  camera.position.set(0, 0, 9);

  var VERDE = 0x22e06b;
  var root = new THREE.Group(); scene.add(root);
  var anelA, anelB, pontos, reflMat;
  var W = 6.4, H = 2.05, N = pequeno ? 10 : 16, STEP = pequeno ? 0.048 : 0.03;

  // ---------- chao: grade + brilho ----------
  var grade = new THREE.GridHelper(70, 70, VERDE, 0x0c4a26);
  grade.position.y = -2.15; grade.material.transparent = true; grade.material.opacity = 0.38;
  scene.add(grade);
  var cc = document.createElement('canvas'); cc.width = cc.height = 256;
  var g = cc.getContext('2d'), gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, 'rgba(34,224,107,.9)'); gr.addColorStop(0.4, 'rgba(34,224,107,.25)'); gr.addColorStop(1, 'rgba(34,224,107,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  var brilho = new THREE.Mesh(new THREE.PlaneGeometry(14, 14),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cc), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  brilho.rotation.x = -Math.PI / 2; brilho.position.y = -2.12; scene.add(brilho);

  // ---------- particulas ----------
  var NP = pequeno ? 260 : 700, pontosPos = new Float32Array(NP * 3), vel = new Float32Array(NP);
  for (var i = 0; i < NP; i++) {
    pontosPos[i * 3] = (Math.random() - 0.5) * 30; pontosPos[i * 3 + 1] = Math.random() * 9 - 2.2; pontosPos[i * 3 + 2] = (Math.random() - 0.5) * 22 - 3;
    vel[i] = 0.15 + Math.random() * 0.45;
  }
  var pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.BufferAttribute(pontosPos, 3));
  pontos = new THREE.Points(pg, new THREE.PointsMaterial({ color: VERDE, size: 0.07, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false }));
  scene.add(pontos);

  // ---------- logo com espessura ----------
  new THREE.TextureLoader().load(LOGO, function (tex) {
    tex.encoding = THREE.sRGBEncoding; tex.anisotropy = 8;
    H = W / (tex.image.width / tex.image.height);
    var geo = new THREE.PlaneGeometry(W, H);
    var logo = new THREE.Group();
    for (var i = 0; i < N; i++) {
      var t = i / (N - 1);
      var cor = i === 0 ? new THREE.Color(0xffffff) : new THREE.Color().setHSL(0.39, 0.9, 0.12 + 0.2 * (1 - t));
      var mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, transparent: true, color: cor, depthWrite: false, fog: false }));
      mesh.position.z = -i * STEP; mesh.renderOrder = N - i; logo.add(mesh);
    }
    [[1.06, 0.55], [1.22, 0.18]].forEach(function (c) { // halo
      var hm = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, transparent: true, color: VERDE, opacity: c[1], blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
      hm.scale.set(c[0], c[0], 1); hm.position.z = -N * STEP - 0.05; hm.renderOrder = 0; logo.add(hm);
    });
    logo.position.z = (N * STEP) / 2;
    root.add(logo);
    reflMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0.16, depthWrite: false, fog: false });
    var refl = new THREE.Mesh(geo, reflMat); // reflexo no chao
    refl.scale.y = -1; refl.position.y = -H - 0.35; refl.renderOrder = 0; root.add(refl);
    sec.classList.add('live'); tam(); pedeFrame();
  }, undefined, function () { /* sem textura: mantem a versao simples */ });

  // ---------- aneis de luz ----------
  anelA = new THREE.Mesh(new THREE.TorusGeometry(3.6, 0.014, 8, 220), new THREE.MeshBasicMaterial({ color: VERDE, transparent: true, opacity: 0.7, fog: false }));
  anelB = new THREE.Mesh(new THREE.TorusGeometry(4.5, 0.01, 8, 220), new THREE.MeshBasicMaterial({ color: VERDE, transparent: true, opacity: 0.35, fog: false }));
  anelA.position.z = anelB.position.z = -0.9; /* aneis removidos da cena a pedido */

  // ---------- estado ----------
  // se o aparelho perder o contexto 3D, volta para a versao simples (logo + texto)
  cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); sec.classList.remove('live'); }, false);
  var mx = 0, my = 0, sx = 0, sy = 0, p = 0, ps = 0, t0 = performance.now(), visivel = true, rodando = false;
  var ov0 = document.getElementById('ov0'), ov1 = document.getElementById('ov1'), ov2 = document.getElementById('ov2'), dica = document.getElementById('hint');
  window.addEventListener('touchmove', function (e) { var t = e.touches[0]; mx = t.clientX / window.innerWidth - 0.5; my = t.clientY / window.innerHeight - 0.5; }, { passive: true });
  window.addEventListener('mousemove', function (e) { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; }, { passive: true });
  function clamp(x) { return Math.min(1, Math.max(0, x)); }
  function suave(x) { x = clamp(x); return x * x * (3 - 2 * x); }
  function lerp(a, b, k) { return a + (b - a) * k; }

  // posicoes/tamanhos da logo (centralizada) calculados em pixels da tela
  var P = { s0: 0.8, y0: 0.2, s1: 0.5, y1: 1.6, s2: 0.7, y2: 1.2 };
  function calc() {
    var cw = cv.clientWidth || 1, ch = cv.clientHeight || 1, larga = cw / ch > 1.1;
    var vh = 2 * Math.tan(camera.fov * Math.PI / 360) * 9, ppu = ch / vh; // pixels por unidade do mundo
    function esc(px) { return px / (W * ppu); }
    function yw(py) { return (0.5 - py / ch) * vh; }
    P.s0 = esc(Math.min(cw * (larga ? 0.5 : 0.88), 780));  P.y0 = yw(ch * (larga ? 0.46 : 0.42));
    P.s1 = esc(Math.min(cw * (larga ? 0.28 : 0.6), 420));   P.y1 = yw(ch * (larga ? 0.2 : 0.17));
    P.s2 = esc(Math.min(cw * (larga ? 0.42 : 0.76), 600));  P.y2 = yw(ch * (larga ? 0.26 : 0.2));
  }
  function tam() {
    var box = cv.parentNode, w = box.clientWidth, h = box.clientHeight;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    calc();
  }
  window.addEventListener('resize', function () { tam(); pedeFrame(); });
  window.addEventListener('load', function () { tam(); pedeFrame(); });
  tam();

  function progresso() {
    if (forcado !== null) return parseFloat(forcado);
    var r = sec.getBoundingClientRect(), total = sec.offsetHeight - cv.parentNode.clientHeight;
    return clamp(-r.top / (total || 1));
  }

  function quadro(now) {
    var t = (now - t0) / 1000;
    p = progresso(); ps += (p - ps) * 0.12; if (forcado !== null) ps = p;
    sx += (mx - sx) * 0.06; sy += (my - sy) * 0.06;
    var a = suave(ps / 0.3), b = suave((ps - 0.62) / 0.3); // a: abertura -> cabecalho | b: cabecalho -> final
    var s = lerp(lerp(P.s0, P.s1, a), P.s2, b);
    root.scale.set(s, s, s);
    root.position.x = 0;
    root.position.y = lerp(lerp(P.y0, P.y1, a), P.y2, b) + Math.sin(t * 0.9) * 0.05;
    root.position.z = b * 0.8;
    root.rotation.y = Math.sin(a * Math.PI) * -0.9 + Math.sin(b * Math.PI) * 0.7 + sx * 0.55 + Math.sin(t * 0.5) * 0.14 * (1 - a);
    root.rotation.x = -sy * 0.3 + Math.sin(t * 0.6) * 0.03;
    if (reflMat) reflMat.opacity = 0.16 * (1 - a) * (1 - b) + 0.04;
    if (anelA) { anelA.rotation.x = 1.2 + Math.sin(t * 0.5) * 0.15; anelA.rotation.z = t * 0.35; anelB.rotation.x = 1.9; anelB.rotation.y = 0.5 + Math.sin(t * 0.4) * 0.2; anelB.rotation.z = -t * 0.22; }
    for (var i = 0; i < NP; i++) { pontosPos[i * 3 + 1] += vel[i] * 0.012; if (pontosPos[i * 3 + 1] > 7) pontosPos[i * 3 + 1] = -2.2; }
    pontos.geometry.attributes.position.needsUpdate = true;
    pontos.rotation.y = t * 0.02 + sx * 0.2;
    camera.position.x = sx * 0.5; camera.position.y = -sy * 0.25; camera.lookAt(0, 0, 0);
    brilho.material.opacity = 0.7 + Math.sin(t * 1.6) * 0.15;
    // textos (cada cena entra e sai)
    var o0 = 1 - suave(ps / 0.08);
    var o1 = suave((ps - 0.16) / 0.1) * (1 - suave((ps - 0.64) / 0.1));
    var o2 = suave((ps - 0.76) / 0.12);
    if (ov0) { ov0.style.opacity = o0.toFixed(3); }
    if (ov1) { ov1.style.opacity = o1.toFixed(3); ov1.style.transform = 'translateY(' + ((1 - o1) * 24).toFixed(1) + 'px)'; ov1.style.pointerEvents = o1 > 0.5 ? 'auto' : 'none'; }
    if (ov2) { ov2.style.opacity = o2.toFixed(3); ov2.style.transform = 'translateY(' + ((1 - o2) * 30).toFixed(1) + 'px)'; ov2.style.pointerEvents = o2 > 0.5 ? 'auto' : 'none'; }
    if (dica) dica.style.opacity = (1 - clamp(ps * 10)).toFixed(3);
    renderer.render(scene, camera);
  }

  function loop(now) { if (!visivel) { rodando = false; return; } quadro(now); requestAnimationFrame(loop); }
  function pedeFrame() {
    if (forcado !== null) { quadro(performance.now()); setTimeout(function () { quadro(performance.now()); }, 300); return; }
    if (!rodando) { rodando = true; requestAnimationFrame(loop); }
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visivel = es[0].isIntersecting; if (visivel) pedeFrame(); }, { threshold: 0 }).observe(sec);
  }
  pedeFrame();
})();
