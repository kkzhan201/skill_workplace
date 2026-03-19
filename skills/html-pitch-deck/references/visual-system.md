# Visual System

Use this reference when implementing or revising the HTML deck itself.

## Stage And Scaling

Every deck should use a fixed `16:9` stage and scale to the viewport.

```css
:root {
  --W: 1280px;
  --H: 720px;
}

#stage {
  position: absolute;
  width: var(--W);
  height: var(--H);
  top: 50%;
  left: 50%;
  transform-origin: center center;
  transform: translate(-50%, -50%) scale(var(--scale));
  overflow: hidden;
}
```

```js
function scaleStage() {
  const s = Math.min(innerWidth / 1280, innerHeight / 720);
  stage.style.transform = `translate(-50%,-50%) scale(${s})`;
}

addEventListener('resize', scaleStage);
scaleStage();
```

## Default Palettes

Start from one of these and keep all dependent effects aligned with the chosen palette.

### Deep blue tech

```css
--bg: #06080f;
--accent: #3b82f6;
--accent2: #22d3ee;
--text: #f1f5f9;
--muted: #475569;
```

### Deep purple luxe

```css
--bg: #0c0a14;
--accent: #a78bfa;
--accent2: #e879f9;
--text: #f5f3ff;
--muted: #4a4360;
```

### Monochrome business

```css
--bg: #0a0a0a;
--accent: #e5e5e5;
--accent2: #a3a3a3;
--text: #fafafa;
--muted: #525252;
```

### Warm paper

```css
--bg: #faf4e8;
--accent: #c0392b;
--accent2: #d48c20;
--text: #1a0e08;
--muted: #9a5a28;
```

If the user provides a reference image:

1. Extract background, primary, and accent colors.
2. Determine whether the overall system is dark or light.
3. Update CSS variables first.
4. Update hover, glow, border, and particle colors to match.

## Motion Baseline

Every deck should include an entry animation system.

```css
[data-a] { opacity: 0; will-change: opacity, transform; }
[data-a="up"]    { transform: translateY(22px); }
[data-a="left"]  { transform: translateX(-22px); }
[data-a="right"] { transform: translateX(22px); }
[data-a="scale"] { transform: scale(.9); }
[data-a].show {
  opacity: 1;
  transform: none;
  transition: opacity .62s cubic-bezier(.2,.8,.2,1),
              transform .62s cubic-bezier(.2,.8,.2,1);
}
```

```js
function animIn(slideIdx) {
  const els = slides[slideIdx].querySelectorAll('[data-a]');
  els.forEach((el) => {
    el.classList.remove('show');
    const d = parseFloat(el.style.getPropertyValue('--delay') || '0');
    setTimeout(() => el.classList.add('show'), d * 1000 + 55);
  });
}
```

## Card Polish

Apply all three treatments to primary cards:

1. Glassmorphism base
2. Top-edge light streak
3. Sweep shimmer

```css
.card {
  background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.015));
  border: 1px solid var(--b1);
  border-radius: 14px;
  position: relative;
  overflow: hidden;
  transition: border-color .3s, transform .3s cubic-bezier(.34,1.2,.64,1), box-shadow .3s;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  opacity: 0;
  transition: opacity .3s;
}

.card:hover::before { opacity: .8; }

.card::after {
  content: '';
  position: absolute;
  top: 0;
  left: -120%;
  width: 60%;
  height: 100%;
  background: linear-gradient(105deg, transparent, rgba(255,255,255,.04), transparent);
  transition: left .55s ease;
  pointer-events: none;
}

.card:hover::after { left: 140%; }
```

Use a glow layer inside each card:

```css
.cglow {
  position: absolute;
  inset: 0;
  border-radius: 14px;
  pointer-events: none;
  opacity: 0;
  transition: opacity .3s;
  background: radial-gradient(circle 110px at var(--mx,50%) var(--my,50%),
    rgba(var(--accent-rgb), .1), transparent 70%);
}

.card:hover .cglow { opacity: 1; }
```

```js
document.querySelectorAll('.card').forEach((card) => {
  const glow = card.querySelector('.cglow');
  if (!glow) return;
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    glow.style.setProperty('--mx', `${e.clientX - rect.left}px`);
    glow.style.setProperty('--my', `${e.clientY - rect.top}px`);
  });
});
```

## Cursor And Ambient Effects

Use a custom cursor on presentation-style decks unless the user asks for a conventional UI.

```css
body { cursor: none; }

#cur {
  position: fixed;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent2);
  pointer-events: none;
  z-index: 9999;
  transform: translate(-50%,-50%);
  mix-blend-mode: difference;
}

#cur-ring {
  position: fixed;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 1px solid rgba(var(--accent-rgb), .5);
  pointer-events: none;
  z-index: 9998;
  transform: translate(-50%,-50%);
  transition: transform .16s cubic-bezier(.2,.8,.2,1);
}
```

```js
let mx = innerWidth / 2;
let my = innerHeight / 2;
let rx = mx;
let ry = my;

document.addEventListener('mousemove', (e) => {
  mx = e.clientX;
  my = e.clientY;
  cur.style.left = `${mx}px`;
  cur.style.top = `${my}px`;
});

(function raf() {
  rx += (mx - rx) * 0.1;
  ry += (my - ry) * 0.1;
  ring.style.left = `${Math.round(rx)}px`;
  ring.style.top = `${Math.round(ry)}px`;
  requestAnimationFrame(raf);
})();
```

For hero or closing slides, add rotating rings or particles if the composition needs more atmosphere.

## Navigation Contract

Every deck must support click, keyboard, and touch navigation.

```html
<div id="nav">
  <button class="na" id="pv">←</button>
  <button class="nd on" data-i="0"></button>
  <button class="na" id="nx">→</button>
  <span class="nc" id="nc">01 / 04</span>
</div>

<div id="pb"></div>
<div id="kh">← → · Space</div>
```

```js
const SL = document.querySelectorAll('.slide');
const ND = document.querySelectorAll('.nd');
let cur = 0;
let busy = false;

function go(n) {
  if (busy || n < 0 || n >= SL.length || n === cur) return;
  busy = true;
  SL[cur].classList.remove('active');
  ND[cur].classList.remove('on');
  cur = n;
  SL[cur].classList.add('active');
  ND[cur].classList.add('on');
  document.getElementById('pb').style.width = `${((cur + 1) / SL.length) * 100}%`;
  document.getElementById('nc').textContent =
    `${String(cur + 1).padStart(2, '0')} / ${String(SL.length).padStart(2, '0')}`;
  animIn(cur);
  setTimeout(() => { busy = false; }, 520);
}

document.getElementById('nx').onclick = () => go(cur + 1);
document.getElementById('pv').onclick = () => go(cur - 1);
ND.forEach((dot) => dot.addEventListener('click', () => go(+dot.dataset.i)));

document.addEventListener('keydown', (e) => {
  if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) {
    e.preventDefault();
    go(cur + 1);
  }
  if (['ArrowLeft', 'ArrowUp'].includes(e.key)) {
    e.preventDefault();
    go(cur - 1);
  }
});

let tx = 0;
addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, { passive: true });
addEventListener('touchend', (e) => {
  const d = e.changedTouches[0].clientX - tx;
  if (Math.abs(d) > 50) go(d < 0 ? cur + 1 : cur - 1);
}, { passive: true });
```

## Recommended Components

- Status badges instead of emoji markers
- SVG icons instead of emoji
- Terminal mockup for technical solution slides
- Alternating roadmap timeline for milestones
- Progress bars on roadmap or version slides
- Count-up numbers on metrics slides

## Playground Effects

When the baseline system is not enough, read [playground-effects.md](playground-effects.md).

Use it with restraint:

- choose one effect family that matches the slide goal
- do not combine multiple hero effects on the same slide unless the composition is intentionally built around them
- cover, closing, metric, and technical explainer slides are the best candidates
- if a recipe depends on `--accent3` or later tokens, derive them from the active palette before use

## Recolor Workflow

When the user asks to change colors, do not rebuild the deck. Update the system in this order:

1. Root variables
2. Page background and decorative gradients
3. Cursor colors
4. Card borders and glow effects
5. Rings, orbs, particles, and badges
6. Progress bar and active navigation states
7. Any hard-coded residual colors

After recoloring, search for stale color values and remove them.

## Output Checklist

- `1280x720` stage with auto-scale
- entry animations on all slides
- `.cglow` layer in cards that need hover depth
- custom cursor if presentation style fits
- top progress bar and bottom navigation
- SVG icons only
- coherent palette with no stale legacy colors
