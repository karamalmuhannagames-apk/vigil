// The world outside the match: home, finding a game, choosing a country, settings and help.
// The live world map stays behind every screen; choosing a country flies the map to it.
(() => {
  const P = (k, d) => { try { const v = localStorage.getItem('cmd.' + k); return v === null ? d : v; } catch (e) { return d; } };
  const S = (k, v) => { try { localStorage.setItem('cmd.' + k, v); } catch (e) {} };
  const AR = document.documentElement.lang === 'ar';
  const t = (ar, en) => (AR ? ar : en);
  const VERSION = 'v0.' + (document.querySelector('meta[name=build]')?.content || '1');

  // ---------- sounds ----------
  const mk = (f) => { const a = new Audio('audio/' + f); a.preload = 'auto'; return a; };
  const sClick = mk('ui_click.ogg'), sOrder = mk('order_radio.ogg');
  const vol = () => Number(P('sfx', '80')) / 100;
  const play = (a, v = 1) => { try { a.currentTime = 0; a.volume = Math.min(1, Math.max(0, v * vol())); const p = a.play(); if (p && p.catch) p.catch(() => {}); } catch (e) {} };
  const click = () => play(sClick, 0.7);

  // ---------- icons (drawn here: rough stencil shapes, no rounded cartoon icons) ----------
  const I = {
    back: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M15 4 7 12l8 8"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 3v18l15-9z"/></svg>',
    servers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/></svg>',
    alliance: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="M8 12l3 3 5-6"/></svg>',
    friends: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21v-1a7 7 0 0 1 14 0v1M16 3.5a4 4 0 0 1 0 7.5M22 21v-1a7 7 0 0 0-4-6.3"/></svg>',
    shop: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h18l-2 13H5zM8 7V5a4 4 0 0 1 8 0v2"/></svg>',
    settings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><path d="M14 4v4M8 10v4M16 16v4"/></svg>',
    help: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 3h16v18H4z"/><path d="M9 9a3 3 0 1 1 4 2.8c-.7.3-1 .9-1 1.7V14M12 17.5v.5"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
    crest: '<svg viewBox="0 0 200 200"><path d="M28 4 H172 L196 28 V172 L172 196 H28 L4 172 V28 Z" fill="#1d2219" stroke="url(#brass)" stroke-width="5"/><use href="#chevrons" x="10" y="12" width="180" height="180" fill="url(#steel)"/></svg>',
  };
  const soon = t('قريبًا', 'SOON');

  // ---------- frame (the map) ----------
  let frame = null, world = null;
  const W = () => { try { return frame.contentWindow; } catch (e) { return null; } };

  // ---------- build the screens ----------
  const root = document.createElement('div'); root.id = 'menu';
  root.innerHTML = `
  <section class="scr" id="m-home"><div class="veil"></div><div class="scan"></div>
    <div class="home-wrap">
      <div class="crest">${I.crest}<div class="ar">القائد</div><div class="en">COMMANDER</div><div class="tag"><i></i>MODERN WAR<i></i></div></div>
      <div class="homebtns">
        <button class="btn-play" data-go="servers">${I.play}<span>${t('العب', 'PLAY')}</span></button>
        <div class="grid">
          <button class="tile" data-go="servers">${I.servers}<span>${t('الخوادم', 'Servers')}</span></button>
          <button class="tile dim" data-soon="1">${I.alliance}<span>${t('التحالفات', 'Alliances')}</span><b class="soon">${soon}</b></button>
          <button class="tile dim" data-soon="1">${I.friends}<span>${t('الأصدقاء', 'Friends')}</span><b class="soon">${soon}</b></button>
          <button class="tile dim" data-soon="1">${I.shop}<span>${t('المتجر', 'Shop')}</span><b class="soon">${soon}</b></button>
          <button class="tile" data-go="settings">${I.settings}<span>${t('الإعدادات', 'Settings')}</span></button>
          <button class="tile" data-go="help">${I.help}<span>${t('المساعدة', 'Help')}</span></button>
        </div>
        <div class="foot"><span>HALBERD STUDIO</span><span>${VERSION}</span></div>
      </div>
    </div>
  </section>

  <section class="scr" id="m-servers"><div class="veil" style="background:rgba(4,6,5,.9)"></div>
    <div class="mtop"><button class="back" data-back="1">${I.back}</button><h1>${t('اختر معركة', 'Choose a battle')}</h1></div>
    <div class="body"><div class="wrapc">
      <div class="search">${I.search}<input id="srvq" placeholder="${t('ابحث عن خادم', 'Search servers')}" enterkeyhint="search"></div>
      <div class="sec">${t('متاح الآن', 'Available now')}</div>
      <div id="srvlist"></div>
      <div class="sec">${t('المعارك عبر الإنترنت', 'Online battles')}</div>
      <div class="plate card2"><h3>${t('حرب عالمية · حتى 60 لاعبًا', 'World war · up to 60 players')}</h3>
        <p>${t('خوادم اللعب عبر الإنترنت مع لاعبين حقيقيين تصل في التحديث القادم.', 'Online servers with real players arrive in the next update.')}</p>
        <div class="meta"><span class="chip">${t('60 يومًا', '60 days')}</span><span class="chip">${t('خريطة العالم', 'World map')}</span><span class="chip gold">${t('التحديث القادم', 'Next update')}</span></div></div>
    </div></div>
  </section>

  <section class="scr see-map" id="m-pick">
    <div class="pick-top"><div class="mtop"><button class="back" data-back="1">${I.back}</button><h1>${t('اختر دولتك', 'Choose your country')}</h1></div></div>
    <div class="sheet">
      <div class="body" style="padding-top:12px"><div class="wrapc">
        <div class="search" style="margin-top:0">${I.search}<input id="cq" placeholder="${t('ابحث عن دولة', 'Search countries')}" enterkeyhint="search"></div>
        <div class="chips" id="regions"></div>
        <div id="clist"></div>
        <div class="empty" id="cnote" style="padding-top:8px;font-size:12.5px">${t('الدول الصغيرة تديرها اللعبة ولا يمكن اختيارها.', 'Small countries are run by the game and cannot be chosen.')}</div>
      </div></div>
      <div class="confirm" id="cgo"><button class="btn-wide" id="cgoBtn"></button></div>
    </div>
  </section>

  <section class="scr" id="m-settings"><div class="veil" style="background:rgba(4,6,5,.92)"></div>
    <div class="mtop"><button class="back" data-back="1">${I.back}</button><h1>${t('الإعدادات', 'Settings')}</h1></div>
    <div class="body"><div class="wrapc" id="setlist"></div></div>
  </section>

  <section class="scr" id="m-help"><div class="veil" style="background:rgba(4,6,5,.92)"></div>
    <div class="mtop"><button class="back" data-back="1">${I.back}</button><h1>${t('المساعدة', 'Help')}</h1></div>
    <div class="body"><div class="wrapc" id="helplist"></div></div>
  </section>`;
  const hud = document.createElement('div'); hud.id = 'hudbar';
  hud.innerHTML = `<button class="back" id="hudMenu" aria-label="menu">${I.menu}</button><div class="nation"><i></i><span id="hudName"></span></div><div class="day">${t('ميدان التدريب', 'TRAINING')}</div>`;
  const toast = document.createElement('div'); toast.id = 'toast';
  const $ = (id) => document.getElementById(id);
  let toastT = 0;
  const say = (msg) => { toast.textContent = msg; toast.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove('on'), 2200); };

  // ---------- navigation ----------
  const stack = [];
  const show = (name) => {
    root.querySelectorAll('.scr').forEach((s) => s.classList.toggle('on', s.id === 'm-' + name));
    if (name === 'pick') fillCountries(); if (name === 'servers') fillServers(); if (name === 'settings') fillSettings(); if (name === 'help') fillHelp();
  };
  const go = (name) => { stack.push(name); show(name); };
  const back = () => {
    if (stack.length <= 1) return false;
    stack.pop(); show(stack[stack.length - 1]);
    if (stack[stack.length - 1] !== 'pick') W()?.flyTo && W().flyTo(P('country', 'JOR'), 0.5);
    return true;
  };
  root.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.go) { click(); go(b.dataset.go); }
    else if (b.dataset.back) { click(); back(); }
    else if (b.dataset.soon) { click(); say(t('في التحديث القادم', 'Coming in the next update')); }
  });

  // ---------- servers ----------
  function fillServers() {
    const q = ($('srvq').value || '').trim().toLowerCase();
    const items = [{ id: 'training', name: t('ميدان التدريب', 'Training ground'), info: t('العالم كله، بلا وقت محدد، دون إنترنت. اختر أي دولة واستكشف الخريطة.', 'The whole world, no time limit, no internet needed. Pick any country and explore the map.'), chips: [t('دون إنترنت', 'Offline'), t('لاعب واحد', '1 player'), t('خريطة العالم', 'World map')] }]
      .filter((s) => !q || s.name.toLowerCase().includes(q) || s.info.toLowerCase().includes(q));
    $('srvlist').innerHTML = items.length ? items.map((s) => `<div class="plate card2"><h3>${s.name}</h3><p>${s.info}</p><div class="meta">${s.chips.map((c) => `<span class="chip">${c}</span>`).join('')}</div><button class="btn-wide" data-join="${s.id}">${t('ادخل', 'Join')}</button></div>`).join('')
      : `<div class="empty">${t('لا يوجد خادم بهذا الاسم.', 'No server matches that name.')}</div>`;
  }
  root.addEventListener('input', (e) => { if (e.target.id === 'srvq') fillServers(); if (e.target.id === 'cq') fillCountries(); });
  root.addEventListener('click', (e) => { const b = e.target.closest('[data-join]'); if (b) { click(); go('pick'); } });

  // ---------- countries ----------
  const REG = [['all', 'الكل', 'All'], ['mena', 'الشرق الأوسط', 'Middle East'], ['europe', 'أوروبا', 'Europe'], ['africa', 'أفريقيا', 'Africa'], ['asia', 'آسيا', 'Asia'], ['americas', 'الأمريكتان', 'Americas'], ['oceania', 'أوقيانوسيا', 'Oceania']];
  const regionOf = (c) => (['Western Asia', 'Northern Africa'].includes(c.subregion) ? 'mena' : c.region_un === 'Europe' ? 'europe' : c.region_un === 'Africa' ? 'africa' : c.region_un === 'Asia' ? 'asia' : c.region_un === 'Americas' ? 'americas' : 'oceania');
  const tier = (a) => (a < 120000 ? t('صغيرة', 'SMALL') : a < 450000 ? t('متوسطة', 'MEDIUM') : a < 1200000 ? t('كبيرة', 'LARGE') : a < 3000000 ? t('ضخمة', 'HUGE') : t('عملاقة', 'GIANT'));
  let region = 'all', picked = null;
  const SHORT = {CHN: 'China', USA: 'United States', COD: 'DR Congo', CAF: 'Central African Republic'};
  const nm = (c) => (AR ? c.name_ar : SHORT[c.iso] || c.name_en) || c.name_en;
  const fmtArea = (a) => (AR ? Math.round(a).toLocaleString('ar-EG') : Math.round(a).toLocaleString('en-US')) + t(' كم²', ' km²');
  function fillCountries() {
    if (!world) world = W()?.world_ && W().world_();
    if (!world) { $('clist').innerHTML = `<div class="empty">${t('الخريطة ما زالت تُحمّل…', 'The map is still loading…')}</div>`; return; }
    $('regions').innerHTML = REG.map(([k, a, e]) => `<button data-reg="${k}" class="${k === region ? 'on' : ''}">${t(a, e)}</button>`).join('');
    const q = ($('cq').value || '').trim().toLowerCase();
    const list = world.countries.filter((c) => c.class === 'playable' && (region === 'all' || regionOf(c) === region) && (!q || (c.name_ar || '').includes(q) || (c.name_en || '').toLowerCase().includes(q)))
      .sort((a, b) => nm(a).localeCompare(nm(b), AR ? 'ar' : 'en'));
    $('clist').innerHTML = list.length ? list.map((c) => `<button class="row${picked === c.iso ? ' sel' : ''}" data-iso="${c.iso}"><span class="mk"></span><span class="nm"><b>${nm(c)}</b><small>${(c.cities || []).length} ${t('مدن', 'cities')} · ${fmtArea(c.area_km2 || 0)}</small></span><span class="tier">${tier(c.area_km2 || 0)}</span></button>`).join('')
      : `<div class="empty">${t('لا توجد دولة بهذا الاسم.', 'No country matches that name.')}</div>`;
    updateGo();
  }
  function updateGo() {
    const c = picked && world && world.countries.find((x) => x.iso === picked);
    $('cgo').classList.toggle('on', !!c);
    if (c) $('cgoBtn').textContent = t(`قُد ${nm(c)}`, `Command ${nm(c)}`);
  }
  root.addEventListener('click', (e) => {
    const r = e.target.closest('[data-reg]'); if (r) { click(); region = r.dataset.reg; fillCountries(); return; }
    const row = e.target.closest('[data-iso]'); if (row) {
      click(); picked = row.dataset.iso;
      root.querySelectorAll('#clist .row').forEach((x) => x.classList.toggle('sel', x === row));
      updateGo(); W()?.flyTo && W().flyTo(picked);
    }
  });
  $('cgoBtn') || null;
  root.addEventListener('click', (e) => { if (e.target.closest('#cgoBtn')) startMatch(picked); });

  // ---------- match ----------
  function startMatch(iso) {
    if (!iso) return;
    play(sOrder, 0.8); S('country', iso);
    const w = W(); if (w?.setRelations) w.setRelations(iso, {});
    if (w?.flyTo) w.flyTo(iso);
    const c = world.countries.find((x) => x.iso === iso);
    $('hudName').textContent = c ? nm(c) : iso;
    root.classList.remove('on'); setTimeout(() => { if (!root.classList.contains('on')) root.style.display = 'none'; }, 450);
    hud.classList.add('on'); stack.length = 0;
    window.dispatchEvent(new Event('menuClosed'));
  }
  function openHome() {
    root.style.display = ''; void root.offsetWidth; root.classList.add('on');   // reflow first so the fade still plays
    hud.classList.remove('on'); stack.length = 0; go('home');
    window.dispatchEvent(new Event('menuOpened'));
  }
  hud.addEventListener('click', (e) => { if (e.target.closest('#hudMenu')) { click(); openHome(); } });

  // ---------- settings ----------
  const seg = (key, def, opts, onSet) => `<div class="seg" data-key="${key}">${opts.map(([v, a, e]) => `<button data-val="${v}" class="${P(key, def) === v ? 'on' : ''}">${t(a, e)}</button>`).join('')}</div>`;
  const onSet = {
    lang: (v) => { location.href = location.pathname + '?menu=1'; },
    quality: (v) => W()?.setQuality && W().setQuality(v),
    glide: (v) => W()?.setGlide && W().setGlide(v),
  };
  function fillSettings() {
    const lang = P('lang', AR ? 'ar' : 'en');
    $('setlist').innerHTML = `
      <div class="sec">${t('عام', 'General')}</div>
      <div class="plate set"><label>${t('اللغة', 'Language')}</label><div class="hint">${t('أسماء الدول والمدن على الخريطة تتبع اللغة.', 'Country and city names on the map follow the language.')}</div>
        <div class="seg" data-key="lang"><button data-val="ar" class="${lang === 'ar' ? 'on' : ''}">العربية</button><button data-val="en" class="${lang === 'en' ? 'on' : ''}">English</button></div></div>
      <div class="sec">${t('الخريطة', 'Map')}</div>
      <div class="plate set"><label>${t('جودة الخريطة', 'Map quality')}</label><div class="hint">${t('"سلسة" أخف على الهواتف القديمة وتوفّر البطارية؛ "حادة" أوضح على الشاشات الكبيرة.', '"Smooth" is lighter on older phones and saves battery; "Sharp" is crisper on big screens.')}</div>
        ${seg('quality', 'balanced', [['smooth', 'سلسة', 'Smooth'], ['balanced', 'متوازنة', 'Balanced'], ['sharp', 'حادة', 'Sharp']])}</div>
      <div class="plate set"><label>${t('حركة الخريطة', 'Map movement')}</label><div class="hint">${t('مدى سرعة لحاق الخريطة بإصبعك.', 'How quickly the map follows your finger.')}</div>
        ${seg('glide', 'normal', [['calm', 'هادئة', 'Calm'], ['normal', 'عادية', 'Normal'], ['quick', 'سريعة', 'Quick']])}</div>
      <div class="sec">${t('الصوت', 'Sound')}</div>
      <div class="plate set"><label>${t('المؤثرات', 'Effects')}</label><input class="rng" type="range" min="0" max="100" step="5" data-key="sfx" value="${P('sfx', '80')}"></div>
      <div class="plate set"><label>${t('الموسيقى', 'Music')}</label><input class="rng" type="range" min="0" max="100" step="5" data-key="music" value="${P('music', '60')}"></div>
      <div class="sec">${t('حول', 'About')}</div>
      <div class="plate card2"><h3>${t('القائد', 'Commander')} · ${VERSION}</h3><p>Halberd Studio</p></div>`;
    $('setlist').querySelectorAll('.rng').forEach((r) => r.style.setProperty('--v', r.value + '%'));
  }
  root.addEventListener('click', (e) => {
    const b = e.target.closest('.seg button'); if (!b) return;
    const key = b.parentElement.dataset.key, v = b.dataset.val; if (P(key, '') === v && key !== 'lang') return;
    click(); b.parentElement.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    const was = P(key, key === 'lang' ? (AR ? 'ar' : 'en') : ''); S(key, v);
    if (key === 'lang' && was === v) return;
    onSet[key] && onSet[key](v);
  });
  root.addEventListener('input', (e) => {
    const r = e.target.closest('.rng'); if (!r) return;
    r.style.setProperty('--v', r.value + '%'); S(r.dataset.key, r.value);
    if (r.dataset.key === 'music') window.dispatchEvent(new Event('musicVolume'));
  });
  root.addEventListener('change', (e) => { if (e.target.closest('.rng[data-key=sfx]')) click(); });

  // ---------- help ----------
  const HELP = [
    [t('تحريك الخريطة', 'Moving the map'), t('اسحب بإصبع واحد لتحريك الخريطة، وباعد إصبعين أو قرّبهما للتكبير والتصغير. العالم يدور: إذا واصلت السحب شرقًا تعود إلى الغرب.', 'Drag with one finger to move. Spread or pinch two fingers to zoom. The world goes round: keep dragging east and you come back from the west.')],
    [t('هدف المعركة', 'Your goal'), t('تستمر المعركة 60 يومًا من أيام اللعب. وسّع أرضك، احمِ مدنك، وكوّن تحالفات قوية.', 'A battle lasts 60 game days. Grow your land, defend your cities and build strong coalitions.')],
    [t('المدن والأقاليم', 'Cities and provinces'), t('كل مدينة وإقليم ينتج موارد. المدينة الخالية تصبح لك لحظة دخول أي وحدة برية إليها، وإن كان فيها جنود فالقتال يستمر حتى ينسحبوا أو يُهزموا.', 'Every city and province produces resources. An empty city is yours the moment a ground unit enters. If troops are inside, the fight goes on until they retreat or fall.')],
    [t('الوحدات والقتال', 'Units and combat'), t('لكل وحدة قوة هجوم ودفاع ضد كل نوع من الوحدات. الطرادات أفضل صيادي الغواصات، والمقاتلات تُسقط المروحيات، ولا تعبر أي وحدة برية نهرًا بلا جسر.', 'Every unit has attack and defence against each kind of unit. Cruisers hunt submarines best, fighters shoot down helicopters, and no ground unit crosses a river without a bridge.')],
    [t('التحالفات', 'Coalitions'), t('تحالف مع لاعبين آخرين لتتشاركوا الرؤية والموانئ. التحالفات تصل مع المعارك عبر الإنترنت في التحديث القادم.', 'Team up with other players to share vision and ports. Coalitions arrive with online battles in the next update.')],
    [t('ميدان التدريب', 'Training ground'), t('اختر أي دولة واستكشف العالم بلا وقت محدد ودون إنترنت. يمكنك العودة إلى القائمة في أي وقت من الزر أعلى الشاشة.', 'Pick any country and explore the world with no time limit and no internet. Go back to the menu any time with the button at the top.')],
  ];
  function fillHelp() {
    $('helplist').innerHTML = HELP.map(([h, b], i) => `<div class="plate acc${i === 0 ? ' open' : ''}"><button><i></i><span>${h}</span></button><div class="txt">${b}</div></div>`).join('');
  }
  root.addEventListener('click', (e) => { const b = e.target.closest('.acc > button'); if (b) { click(); b.parentElement.classList.toggle('open'); } });

  // ---------- public ----------
  window.Menu = {
    attach(f) { frame = f; document.body.append(root, hud, toast); },
    open: openHome,
    back() {                                     // Android back button: one screen back; in the match it opens the menu
      if (root.classList.contains('on')) return back();
      openHome(); return true;
    },
    isOpen: () => root.classList.contains('on'),
  };
})();
