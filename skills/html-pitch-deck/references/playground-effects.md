# Playground Effects

Use this reference only after the markdown copy is confirmed and the deck has entered component-selection or implementation stage.

This file is a curated effect library adapted from the user's older `animation-playground.html` workflow. Treat it as an optional layer on top of the baseline system in [visual-system.md](visual-system.md).

## Selection Rules

- Choose effects because they strengthen the slide's communication, not because empty space feels boring.
- Prefer at most one hero effect or one supporting effect per slide.
- Cover, closing, metric, and technical-explainer slides benefit most from playground effects.
- If the slide already has strong copy and layout, stop at baseline motion.

## Palette Prep

Some recipes use extended tokens such as `--accent3`, `--accent4`, or `--accent5`.

When using them:

- derive them from the active palette
- keep the same hue family
- avoid introducing unrelated highlight colors

Example mapping for a blue deck:

```css
--accent: #3b82f6;
--accent2: #22d3ee;
--accent3: #60a5fa;
--accent4: #93c5fd;
--accent5: #1d4ed8;
```

## Quick Lookup

| Slide type | Recommended effects |
|---|---|
| Cover or closing | `Particle Field`, `Glitch`, `Gradient Flow` |
| Data or KPI | `Count-up`, `Spectrum Bars`, `Stagger Bars` |
| Loading or transition state | `Skeleton Shimmer`, `Dot Loader`, `Pulse Indicator` |
| CTA or button-heavy ending | `Magnetic Button`, `Ripple Button` |
| Tech explainer | `Neon Flicker`, `Terminal-style blocks`, `Orbit System` |

## CAT 1 — Loaders And State

### Skeleton Shimmer

```css
.sk {
  height: 9px;
  border-radius: 5px;
  background: linear-gradient(90deg, #18182a 25%, #252540 50%, #18182a 75%);
  background-size: 200% 100%;
  animation: shimmer 1.6s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Dot Loader

```css
.spinner-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent3);
  animation: dotBounce 1.2s ease-in-out infinite;
}

.spinner-dots span:nth-child(2) { animation-delay: .2s; }
.spinner-dots span:nth-child(3) { animation-delay: .4s; }

@keyframes dotBounce {
  0%, 80%, 100% { transform: scale(.6); opacity: .4; }
  40% { transform: scale(1); opacity: 1; }
}
```

### Pulse Indicator

```css
.pulse-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #22c55e;
  position: relative;
}

.pulse-dot::after {
  content: '';
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  border: 2px solid #22c55e;
  animation: pulseOut 1.5s ease-out infinite;
}

@keyframes pulseOut {
  0% { opacity: .8; transform: scale(1); }
  100% { opacity: 0; transform: scale(2); }
}
```

## CAT 2 — Text Effects

### Glitch

```css
.glitch {
  color: var(--text);
  position: relative;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
}

.glitch::before {
  color: var(--accent3);
  clip-path: polygon(0 0,100% 0,100% 40%,0 40%);
  animation: glitch1 3s infinite;
}

.glitch::after {
  color: var(--accent2);
  clip-path: polygon(0 60%,100% 60%,100% 100%,0 100%);
  animation: glitch2 3s infinite;
}

@keyframes glitch1 {
  0%, 94%, 100% { transform: none; opacity: 0; }
  95% { transform: translateX(-4px); opacity: 1; }
  97% { transform: translateX(4px); opacity: 1; }
}

@keyframes glitch2 {
  0%, 94%, 100% { transform: none; opacity: 0; }
  96% { transform: translateX(4px); opacity: 1; }
  98% { transform: translateX(-4px); opacity: 1; }
}
```

```html
<div class="glitch" data-text="GLITCH">GLITCH</div>
```

### Text Scramble

```js
function scramble(el, target) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%';
  let iter = 0;
  let frame = 0;
  const iv = setInterval(() => {
    el.textContent = target.split('').map((c, i) =>
      i < iter ? c : chars[Math.floor(Math.random() * chars.length)]
    ).join('');
    if (++frame % 3 === 0) iter++;
    if (iter >= target.length) clearInterval(iv);
  }, 38);
}
```

### Gradient Flow

```css
.grad-text {
  background: linear-gradient(135deg, var(--accent), var(--accent3), var(--accent4));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200%;
  animation: gradShift 4s linear infinite;
}

@keyframes gradShift {
  0% { background-position: 0%; }
  100% { background-position: 200%; }
}
```

## CAT 3 — Micro-Interactions

### Magnetic Button

```js
btn.addEventListener('mousemove', (e) => {
  const r = btn.getBoundingClientRect();
  const dx = e.clientX - r.left - r.width / 2;
  const dy = e.clientY - r.top - r.height / 2;
  btn.style.transform = `translate(${dx * .3}px, ${dy * .3}px) scale(1.05)`;
});

btn.addEventListener('mouseleave', () => {
  btn.style.transform = '';
});
```

### Ripple Button

```js
btn.addEventListener('click', (e) => {
  const r = btn.getBoundingClientRect();
  const span = document.createElement('span');
  const size = Math.max(r.width, r.height) * 2;
  Object.assign(span.style, {
    position: 'absolute',
    width: `${size}px`,
    height: `${size}px`,
    left: `${e.clientX - r.left - size / 2}px`,
    top: `${e.clientY - r.top - size / 2}px`,
    background: 'rgba(255,255,255,.3)',
    borderRadius: '50%',
    transform: 'scale(0)',
    animation: 'rippleAnim .6s linear',
    pointerEvents: 'none',
  });
  btn.appendChild(span);
  setTimeout(() => span.remove(), 620);
});
```

```css
@keyframes rippleAnim {
  to { transform: scale(1); opacity: 0; }
}
```

### Hover Lift

```css
.lift-card {
  transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s, border-color .3s;
}

.lift-card:hover {
  transform: translateY(-8px) rotate(-2deg);
  box-shadow: 0 20px 40px rgba(0,0,0,.6);
}
```

## CAT 4 — Visual FX

### Blob Morph

```css
.blob {
  background: linear-gradient(135deg, var(--accent4), var(--accent3));
  animation: morphBlob 6s ease-in-out infinite;
}

@keyframes morphBlob {
  0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  25% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
  50% { border-radius: 50% 60% 30% 60% / 40% 70% 60% 30%; }
  75% { border-radius: 70% 30% 60% 40% / 30% 50% 70% 60%; }
  100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
}
```

### Orbit System

```css
.orbit-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1px dashed rgba(255,255,255,.2);
  animation: spinOrbit 4s linear infinite;
}

.orbit-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
}

.orbit-ring.r2 {
  inset: 10px;
  animation-duration: 2.5s;
  animation-direction: reverse;
}

@keyframes spinOrbit {
  to { transform: rotate(360deg); }
}
```

### Stagger Bars

```css
.stagger-bar {
  height: 7px;
  border-radius: 4px;
  background: var(--accent4);
  transform-origin: left;
  animation: staggerBar 2s ease-in-out infinite;
}

.stagger-bar:nth-child(1) { width: 92%; animation-delay: 0s; }
.stagger-bar:nth-child(2) { width: 68%; animation-delay: .12s; }
.stagger-bar:nth-child(3) { width: 82%; animation-delay: .24s; }
.stagger-bar:nth-child(4) { width: 55%; animation-delay: .36s; }

@keyframes staggerBar {
  0%, 65%, 100% { transform: scaleX(0); opacity: 0; }
  20%, 50% { transform: scaleX(1); opacity: 1; }
}
```

## CAT 5 — Canvas

### Particle Field

Best for cover or closing slides. Use when the slide needs atmosphere, not when the layout is already busy.

```js
function initParticles(canvasId, colorR, colorG, colorB, lineR, lineG, lineB) {
  const cv = document.getElementById(canvasId);
  cv.width = cv.offsetWidth || 1280;
  cv.height = cv.offsetHeight || 720;
  const ctx = cv.getContext('2d');
  const pts = Array.from({ length: 55 }, () => ({
    x: Math.random() * cv.width,
    y: Math.random() * cv.height,
    vx: (Math.random() - .5) * .4,
    vy: (Math.random() - .5) * .4,
    r: Math.random() * 1.8 + .5,
    pulse: Math.random() * Math.PI * 2,
  }));
  let hx = null;
  let hy = null;

  cv.addEventListener('mousemove', (e) => {
    const r = cv.getBoundingClientRect();
    hx = e.clientX - r.left;
    hy = e.clientY - r.top;
  });

  cv.addEventListener('mouseleave', () => {
    hx = null;
    hy = null;
  });

  (function loop() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    pts.forEach((p) => {
      p.pulse += .012;
      if (hx !== null) {
        const d = Math.hypot(hx - p.x, hy - p.y);
        if (d < 90) {
          p.vx += ((hx - p.x) / d) * .04;
          p.vy += ((hy - p.y) / d) * .04;
        }
      }
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= .98;
      p.vy *= .98;
      if (p.x < 0 || p.x > cv.width) p.vx *= -1;
      if (p.y < 0 || p.y > cv.height) p.vy *= -1;
      const a = .4 + .4 * Math.sin(p.pulse);
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${colorR},${colorG},${colorB},${a})`;
      ctx.fill();
    });
    requestAnimationFrame(loop);
  })();
}
```

### Spectrum Bars

```js
function initSpectrumBars(canvasId, colors) {
  const cv = document.getElementById(canvasId);
  cv.width = cv.offsetWidth * devicePixelRatio;
  cv.height = cv.offsetHeight * devicePixelRatio;
  const ctx = cv.getContext('2d');
  const bars = 28;
  const h = Array.from({ length: bars }, () => Math.random());
  const t = Array.from({ length: bars }, () => Math.random());
  setInterval(() => t.forEach((_, i) => { t[i] = .08 + Math.random() * .92; }), 190);
  (function loop() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    const bw = cv.width / bars;
    h.forEach((v, i) => {
      h[i] += (t[i] - v) * .14;
      const bh = h[i] * cv.height * .88;
      const x = i * bw + bw * .12;
      const w = bw * .76;
      const y = cv.height - bh;
      const gr = ctx.createLinearGradient(0, y, 0, cv.height);
      gr.addColorStop(0, colors[i % colors.length]);
      gr.addColorStop(1, `${colors[i % colors.length]}18`);
      ctx.fillStyle = gr;
      ctx.beginPath();
      ctx.roundRect(x, y, w, bh, 2 * devicePixelRatio);
      ctx.fill();
    });
    requestAnimationFrame(loop);
  })();
}
```

## CAT 6 — Layout And UI

### Accordion

```js
document.querySelectorAll('.acc-header').forEach((header) => {
  header.addEventListener('click', () => {
    const item = header.parentElement;
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.acc-item').forEach((i) => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
```

### Tabs

```js
document.querySelectorAll('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach((p) => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
  });
});
```

### Count-Up

```js
function countUp(el, target, suffix = '') {
  const dur = 1600;
  const start = performance.now();
  function ease(t) { return t < .5 ? 2 * t * t : (4 - 2 * t) * t - 1; }
  (function step(now) {
    const p = Math.min((now - start) / dur, 1);
    el.textContent = Math.round(ease(p) * target) + (p >= 1 ? suffix : '');
    if (p < 1) requestAnimationFrame(step);
  })(start);
}
```
