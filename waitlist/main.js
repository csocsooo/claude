/**
 * AURA Waitlist — main.js
 *
 * Responsibilities:
 *   1. Three.js 3D scene: iridescent, slowly morphing TorusKnot with
 *      MeshPhysicalMaterial (transmission + iridescence), rim lighting,
 *      emissive glow, mouse-parallax, and proper resize handling.
 *   2. WebGL availability check + graceful fallback.
 *   3. Waitlist form: client-side validation, mock submit with spinner,
 *      animated success state. No network calls.
 */

/*
 * THREE is loaded as a global from the local UMD build (three.min.js),
 * so this file runs as a classic script and works straight from file://
 * (double-click) — no bundler, import map, or local server required.
 * Postprocessing addons (bloom) are not part of the UMD build, so the
 * glow is achieved purely via emissive material + tone-mapping exposure.
 */

/* ================================================================
   Utility: detect WebGL support
================================================================ */
function isWebGLAvailable() {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!window.WebGLRenderingContext || !ctx) return false;
    // Release the temporary context immediately to free GPU resources
    ctx.getExtension('WEBGL_lose_context')?.loseContext();
    return true;
  } catch {
    return false;
  }
}

/* ================================================================
   Utility: detect low-power / mobile device
================================================================ */
function isLowPowerDevice() {
  // Treat small screens or coarse-pointer devices (touch) as low-power
  return (
    window.matchMedia('(max-width: 768px)').matches ||
    window.matchMedia('(pointer: coarse)').matches
  );
}

/* ================================================================
   Three.js Scene
================================================================ */
function initScene() {
  const canvas   = document.getElementById('canvas-bg');
  const fallback = document.getElementById('canvas-fallback');

  // Helper: activate the CSS fallback (WebGL unavailable or failed)
  function activateFallback() {
    canvas.style.display   = 'none';
    fallback.style.display = 'block';
  }

  // --- WebGL gate ------------------------------------------------
  if (!isWebGLAvailable()) {
    activateFallback();
    return; // bail out gracefully — CSS fallback takes over
  }

  // --- Mobile / low-power detection -----------------------------
  const lowPower = isLowPowerDevice();

  // DPR cap: 1.5 on mobile, 2 on desktop
  const DPR_CAP = lowPower ? 1.5 : 2;

  // TorusKnot segment counts: fewer on mobile for lower GPU load
  const TORUS_TUBE_SEGS   = lowPower ? 120 : 220;
  const TORUS_RADIAL_SEGS = lowPower ? 16  : 24;

  // --- Renderer (try/catch: driver blocklist, context failures) --
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha:     true,    // transparent background so CSS bg shows through
    });
  } catch (err) {
    // Context creation failed (e.g. driver blocklist, hardware limit)
    console.warn('[AURA] WebGLRenderer creation failed, using CSS fallback:', err);
    activateFallback();
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, DPR_CAP));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping        = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.25; // slightly higher to compensate for no bloom pass
  renderer.outputColorSpace   = THREE.SRGBColorSpace;

  // --- Scene & Camera --------------------------------------------
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    0.1,
    100
  );
  camera.position.set(0, 0, 6);

  // --- Lights ----------------------------------------------------
  // Key light: warm, slightly off-centre
  const keyLight = new THREE.DirectionalLight(0xd0aaff, 3.5);
  keyLight.position.set(3, 4, 5);
  scene.add(keyLight);

  // Rim light: cool cyan from the back-left — creates the iridescent edge
  const rimLight = new THREE.DirectionalLight(0x00e5ff, 2.8);
  rimLight.position.set(-4, -2, -3);
  scene.add(rimLight);

  // Ambient: very dark, just lifts the absolute shadows slightly
  const ambient = new THREE.AmbientLight(0x1a0a2e, 1.2);
  scene.add(ambient);

  // Subtle fill from below (purple cast on underside)
  const fillLight = new THREE.PointLight(0x7c3aed, 1.5, 20);
  fillLight.position.set(0, -4, 2);
  scene.add(fillLight);

  // --- Geometry --------------------------------------------------
  // TorusKnot: complex, self-intersecting loops look great with
  // iridescent / transmission material.
  // Segment counts are reduced on mobile to lower GPU load.
  const geometry = new THREE.TorusKnotGeometry(
    1.3,               // radius
    0.42,              // tube radius
    TORUS_TUBE_SEGS,   // tubular segments (higher = smoother)
    TORUS_RADIAL_SEGS, // radial segments
    2,                 // p — winding number
    3                  // q — winding number
  );

  // --- Material: MeshPhysicalMaterial ----------------------------
  // MeshPhysicalMaterial supports:
  //   • transmission  — glass-like see-through
  //   • iridescence   — colour-shifting thin-film interference
  //   • clearcoat     — extra specular layer on top
  //   • roughness/metalness — PBR inputs
  const material = new THREE.MeshPhysicalMaterial({
    color:            new THREE.Color(0x7c3aed),   // base violet tint
    emissive:         new THREE.Color(0x3b0d8a),   // self-glow
    emissiveIntensity: 0.35,

    metalness:  0.15,
    roughness:  0.08,

    // Glass-like transmission
    transmission: 0.45,
    thickness:    2.0,
    ior:          1.55,  // index of refraction (glass ≈ 1.5)

    // Iridescence: rainbow thin-film effect on grazing angles
    iridescence:           1.0,
    iridescenceIOR:        1.8,
    iridescenceThicknessRange: [200, 800],

    // Clear coat for that extra specular pop
    clearcoat:          0.8,
    clearcoatRoughness: 0.12,

    side: THREE.DoubleSide,
  });

  const mesh = new THREE.Mesh(geometry, material);

  // --- Parallax group -------------------------------------------
  // The mesh lives inside a parent Group. The Group carries parallax
  // rotation (lerped toward the cursor), while the mesh itself carries
  // the intrinsic spin/wobble. This keeps parallax as a clean offset
  // and prevents Y-axis rotation from accumulating as a velocity bias.
  const group = new THREE.Group();
  group.add(mesh);
  scene.add(group);

  // --- Rendering path -------------------------------------------
  // The UMD (global) Three.js build does not ship the postprocessing
  // addons, so there is no EffectComposer/bloom here. The "glow" comes
  // from the emissive material + raised tone-mapping exposure instead.
  // `composer` stays null and the render calls below use the plain
  // renderer — keeping a single, dependency-free rendering path.
  const composer = null;

  // --- Mouse parallax state --------------------------------------
  // We store the "target" mouse position and lerp the actual rotation
  // toward it each frame — this gives a buttery smooth follow.
  const mouse = { x: 0, y: 0 };      // normalised −1 … +1
  const target = { rx: 0, ry: 0 };   // target GROUP rotation in radians
  const current = { rx: 0, ry: 0 };  // current (lerped) GROUP rotation

  // Parallax sensitivity (radians of rotation per unit of cursor movement)
  const PARALLAX_STRENGTH = 0.35;

  window.addEventListener('mousemove', (e) => {
    mouse.x = (e.clientX / window.innerWidth)  * 2 - 1;  // −1 … +1
    mouse.y = (e.clientY / window.innerHeight) * 2 - 1;
    target.ry =  mouse.x * PARALLAX_STRENGTH;
    target.rx = -mouse.y * PARALLAX_STRENGTH * 0.6;
  });

  // Touch support for parallax
  window.addEventListener('touchmove', (e) => {
    const touch = e.touches[0];
    mouse.x = (touch.clientX / window.innerWidth)  * 2 - 1;
    mouse.y = (touch.clientY / window.innerHeight) * 2 - 1;
    target.ry =  mouse.x * PARALLAX_STRENGTH;
    target.rx = -mouse.y * PARALLAX_STRENGTH * 0.6;
  }, { passive: true });

  // --- Resize handler -------------------------------------------
  // baseScale is stored separately so the breathing animation can
  // multiply against it reliably without reading back from mesh.scale.
  let baseScale = 1;

  function onResize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, DPR_CAP));
    if (composer) composer.setSize(w, h);

    // Scale mesh down on small screens so it doesn't overpower the UI
    baseScale = Math.min(1, Math.max(0.55, w / 900));
    mesh.scale.setScalar(baseScale);
  }

  window.addEventListener('resize', onResize);
  onResize(); // run once on init to set correct scale

  // --- prefers-reduced-motion check -----------------------------
  // If the user has requested reduced motion, render a single static
  // frame and stop — no continuous animation loop.
  const prefersReducedMotion =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReducedMotion) {
    // Position the mesh at a pleasing static angle and render once
    mesh.rotation.x = 0.18;
    mesh.rotation.y = 0.4;
    if (composer) {
      composer.render();
    } else {
      renderer.render(scene, camera);
    }
    return; // do not start the animation loop
  }

  // --- Animation loop -------------------------------------------
  const LERP = 0.045; // lower = lazier follow (0 = frozen, 1 = instant)

  let t = 0; // elapsed time in seconds (driven by clock)
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    t += delta;

    // ------ Intrinsic rotation on the mesh (spin + wobble) ------
    // Y-axis spin accumulates each frame; X and Z are sinusoidal so
    // they never drift — purely oscillatory wobble.
    mesh.rotation.y += delta * 0.22;
    mesh.rotation.x  = Math.sin(t * 0.35) * 0.18;
    mesh.rotation.z  = Math.cos(t * 0.25) * 0.08;

    // ------ Parallax on the GROUP (lerped toward cursor) --------
    // Applying parallax to the parent group keeps it decoupled from
    // the mesh's intrinsic spin, so it acts as a stable angular offset
    // rather than a per-frame velocity bias.
    current.rx += (target.rx - current.rx) * LERP;
    current.ry += (target.ry - current.ry) * LERP;
    group.rotation.x = current.rx;
    group.rotation.y = current.ry;

    // ------ Breathing scale pulse: ±3 % over ~4 s ---------------
    // All three axes scale uniformly so the object swells/shrinks
    // evenly. baseScale is the value set by the resize handler.
    const breathe = 1 + Math.sin(t * 1.57) * 0.03;
    mesh.scale.x = baseScale * breathe;
    mesh.scale.y = baseScale * breathe;
    mesh.scale.z = baseScale * breathe;

    // ------ Emissive pulse (gives a "glow breathing" feel) ------
    // Pushed a bit higher than the original bloom-assisted version so the
    // object still reads as luminous without a postprocessing glow pass.
    const glow = 0.5 + Math.sin(t * 0.8) * 0.18;
    material.emissiveIntensity = glow;

    // ------ Animate fill light position (slow orbit) ------
    fillLight.position.x = Math.sin(t * 0.5) * 4;
    fillLight.position.z = Math.cos(t * 0.5) * 3;

    // Render: via composer (bloom) on desktop, plain renderer on mobile
    if (composer) {
      composer.render();
    } else {
      renderer.render(scene, camera);
    }
  }

  animate();
}

/* ================================================================
   Form validation & submit
================================================================ */
function initForm() {
  const form        = document.getElementById('waitlist-form');
  const formCard    = document.getElementById('form-card');
  const successEl   = document.getElementById('success-state');
  const nameInput   = document.getElementById('input-name');
  const emailInput  = document.getElementById('input-email');
  const phoneInput  = document.getElementById('input-phone');
  const submitBtn   = form.querySelector('.btn-cta');

  // --- Helpers ---------------------------------------------------
  function showError(input, errorEl, message) {
    input.classList.add('invalid');
    errorEl.textContent = message;
    errorEl.classList.add('visible');
    input.setAttribute('aria-invalid', 'true');
  }

  function clearError(input, errorEl) {
    input.classList.remove('invalid');
    errorEl.textContent = '';
    errorEl.classList.remove('visible');
    input.removeAttribute('aria-invalid');
  }

  // --- Per-field live validation (on blur) ----------------------
  nameInput.addEventListener('blur', () => validateName(true));
  emailInput.addEventListener('blur', () => validateEmail(true));
  phoneInput.addEventListener('blur', () => validatePhone(true));

  // Clear errors as the user types again
  [nameInput, emailInput, phoneInput].forEach(input => {
    const errorEl = document.getElementById(input.getAttribute('aria-describedby'));
    input.addEventListener('input', () => {
      if (input.classList.contains('invalid')) clearError(input, errorEl);
    });
  });

  // --- Validators -----------------------------------------------
  function validateName(showFeedback = false) {
    const errEl = document.getElementById('err-name');
    const val   = nameInput.value.trim();
    if (!val) {
      if (showFeedback) showError(nameInput, errEl, 'Please enter your full name.');
      return false;
    }
    clearError(nameInput, errEl);
    return true;
  }

  function validateEmail(showFeedback = false) {
    const errEl = document.getElementById('err-email');
    const val   = emailInput.value.trim();
    // RFC-ish basic pattern
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    if (!val) {
      if (showFeedback) showError(emailInput, errEl, 'Please enter your email address.');
      return false;
    }
    if (!emailRe.test(val)) {
      if (showFeedback) showError(emailInput, errEl, 'Please enter a valid email (e.g. jane@example.com).');
      return false;
    }
    clearError(emailInput, errEl);
    return true;
  }

  function validatePhone(showFeedback = false) {
    const errEl = document.getElementById('err-phone');
    const val   = phoneInput.value.trim();
    // Allowed characters: digits, spaces, +, -, (, ), dots; total length 7–20.
    // Additionally requires at least 7 actual digits so that a string of
    // only formatting characters (e.g. "   +()-   ") cannot pass.
    const phoneRe  = /^[+\-()\s\d.]{7,20}$/;
    const digitMin = 7;
    if (!val) {
      if (showFeedback) showError(phoneInput, errEl, 'Please enter your phone number.');
      return false;
    }
    if (!phoneRe.test(val) || val.replace(/\D/g, '').length < digitMin) {
      if (showFeedback) showError(phoneInput, errEl, 'Please enter a valid phone number.');
      return false;
    }
    clearError(phoneInput, errEl);
    return true;
  }

  // --- Submit handler -------------------------------------------
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validate all fields and collect results
    const nameOk  = validateName(true);
    const emailOk = validateEmail(true);
    const phoneOk = validatePhone(true);

    if (!nameOk || !emailOk || !phoneOk) {
      // Focus first invalid field for accessibility
      if (!nameOk)  { nameInput.focus();  return; }
      if (!emailOk) { emailInput.focus(); return; }
      if (!phoneOk) { phoneInput.focus(); return; }
      return;
    }

    // Collect data (log to console only — no network call)
    const data = {
      name:  nameInput.value.trim(),
      email: emailInput.value.trim(),
      phone: phoneInput.value.trim(),
    };

    console.info('[AURA Waitlist] New submission (no backend):', data);

    // Simulate brief async submit with loading spinner
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    await new Promise(resolve => setTimeout(resolve, 900));

    // --- Show success state ---
    // 1. Switch card to submitted mode (hides form, shows success div)
    formCard.classList.add('submitted');
    successEl.setAttribute('aria-hidden', 'false');
    successEl.style.display = 'flex';

    // 2. Trigger the staggered success animations via .visible class
    //    (rAF ensures the display:flex has rendered before we add .visible)
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        successEl.classList.add('visible');

        // Move focus to the success title so screen readers announce it
        const successTitle = successEl.querySelector('.success-title');
        if (successTitle) successTitle.focus();
      });
    });
  });
}

/* ================================================================
   Boot
================================================================ */
// Use DOMContentLoaded so both functions run as soon as the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initScene();
  initForm();
});
