# Makes the game's opening and interface sounds from scratch (no samples, no licences needed).
# usage: python3 ci/audio/make_sounds.py   -> app/audio/*.ogg
import os, subprocess, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'audio')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def t(sec): return np.arange(int(sec * SR)) / SR
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=3): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def env(n, a, d, shape=4.0):
    e = np.ones(n); ai = int(a * SR)
    if ai: e[:ai] = np.linspace(0, 1, ai) ** 2
    rest = n - ai; e[ai:] = np.exp(-np.linspace(0, shape, rest)) if d else 1
    return e
def reverb(x, sec=2.5, wet=0.35, dark=3000):
    n = int(sec * SR); ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n)); ir = lp(ir, dark)
    y = fftconvolve(x, ir)[: len(x) + n]; y = np.pad(y, (0, len(x) + n - len(y))); y /= np.max(np.abs(y)) + 1e-9
    x2 = np.pad(x, (0, n)); x2 /= np.max(np.abs(x2)) + 1e-9
    return (1 - wet) * x2 + wet * y
def boom(sec=3.0, f0=55, f1=28, noise=0.6):
    tt = t(sec); f = f1 + (f0 - f1) * np.exp(-tt * 3)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6)
    n = lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 3.5) * noise
    crack = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 40) * 0.5
    return s + n + crack
def metal_ring(sec=3.0, base=420.0):
    tt = t(sec); y = np.zeros_like(tt)
    for k, (m, a, d) in enumerate([(1, 1, 1.2), (2.76, .6, 1.8), (5.4, .4, 2.6), (8.9, .25, 3.5), (13.3, .15, 5)]):
        y += a * np.sin(2 * np.pi * base * m * tt + k) * np.exp(-tt * d)
    return y
def static(sec, density=1.0):
    n = rng.standard_normal(int(sec * SR)); n = bp(n, 900, 4200)
    gate = (lp(rng.standard_normal(len(n)), 6) > (0.2 / density)).astype(float)
    return n * (0.3 + 0.7 * lp(gate, 30))
def save(name, x, gain=0.9, phone=False):
    if phone:   # phone speakers cannot play deep bass: trim the sub, lift the 150-1200 Hz body so the hit is felt
        x = hp(x, 45, 2); mid = bp(x, 150, 1200, 2); x = x + 2.2 * mid
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    # short fades so nothing clicks
    f = int(0.01 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    wav = f'/tmp/{name}.wav'
    import wave
    with wave.open(wav, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        st = np.stack([x, np.roll(x, 90)], 1)  # slight width
        w.writeframes((st * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '5', os.path.join(OUT, name + '.ogg')], check=True)
    os.remove(wav)

# 1. Studio reveal: a low swell rising out of silence into a deep, heavy hit ("braam") with a long dark tail. No bell, no ringing.
d = 4.4; base = np.zeros(int(d * SR))
hit = 1.25
sw = t(hit); swell = lp(rng.standard_normal(len(sw)), 220) * (sw / hit) ** 3 * 0.35 + np.sin(2 * np.pi * 38 * sw) * (sw / hit) ** 2.5 * 0.5
base[: len(sw)] += swell
i0 = int(hit * SR); bt = t(d - hit)
saw = lambda f: 2 * ((f * bt) % 1) - 1
braam = (saw(55) + saw(55.6) * 0.8 + saw(82.4) * 0.6 + saw(41.2) * 0.7)
cut = 420 + 2600 * np.exp(-bt * 1.8)                       # filter opens on the hit, then closes: brass-like, dark
y = np.zeros_like(braam); state = 0.0
for k in range(len(braam)):                                 # one-pole lowpass with a moving cutoff
    a_ = 1 - np.exp(-2 * np.pi * cut[k] / SR); state += a_ * (braam[k] - state); y[k] = state
braam = np.tanh(y * 2.6) * np.exp(-bt * 0.9) * 0.7          # saturation adds the mid harmonics phone speakers can play
b = boom(2.8, 52, 26, 0.35) * 0.9
base[i0: i0 + len(braam)] += braam[: len(base) - i0]
base[i0: i0 + len(b)] += b[: len(base) - i0]
save('studio_reveal', reverb(base, 2.6, 0.32, 1600)[: int(5.0 * SR)], phone=True)

# 2. Game logo impact: a heavy artillery-like hit with a long rolling tail.
d = 4.0; x = np.zeros(int(d * SR))
b = boom(3.6, 70, 26, 0.9); x[: len(b)] += b
body = bp(rng.standard_normal(len(x)), 180, 900) * env(len(x), 0.004, True, 6) * 1.1; x += body
thump = np.tanh(np.sin(2 * np.pi * 95 * t(d)) * np.exp(-t(d) * 5) * 3) * 0.5; x += thump
roll = lp(rng.standard_normal(len(x)), 120) * env(len(x), 0.3, True, 2.5) * 0.5; x += roll
whoosh = bp(rng.standard_normal(int(0.5 * SR)), 300, 2500) * np.linspace(0, 1, int(0.5 * SR)) ** 3
pre = np.concatenate([whoosh * 0.35, x])
save('logo_impact', reverb(pre, 2.8, 0.35, 1800)[: int(5.0 * SR)], phone=True)

# 3. Loading loop (24 s, loops cleanly): low drone, distant artillery, radio static bursts, a faint signal beep.
L = 24.0; n = int(L * SR); tt = t(L)
x = (np.sin(2 * np.pi * 110 * tt) * 0.16 + np.sin(2 * np.pi * 165 * tt) * 0.1 + np.sin(2 * np.pi * 220 * tt) * 0.05) * (0.8 + 0.2 * np.sin(2 * np.pi * tt / L))
x += lp(rng.standard_normal(n), 450) * 0.1
for at in [1.2, 4.9, 6.1, 10.4, 13.8, 15.0, 19.6, 22.3]:
    b = lp(boom(2.2, 70, 40, 0.9), 900) * (0.35 + 0.25 * rng.random()); i = int(at * SR)
    x[i: i + len(b)] += b[: n - i]
for at, ln in [(3.0, 0.7), (8.2, 1.1), (12.0, 0.5), (17.4, 0.9), (21.0, 0.6)]:
    s = static(ln, 1.5) * 0.18 * np.hanning(int(ln * SR)); i = int(at * SR); x[i: i + len(s)] += s
for at in [7.0, 7.25, 7.5, 16.0, 16.25]:
    bt = t(0.09); bp_ = np.sin(2 * np.pi * 1180 * bt) * np.hanning(len(bt)) * 0.05; i = int(at * SR); x[i: i + len(bt)] += bp_
x = reverb(x, 1.5, 0.25, 2500)[:n]
xf = int(0.5 * SR); x[:xf] = x[:xf] * np.linspace(0, 1, xf) + x[-xf:] * np.linspace(1, 0, xf); x = x[: n - xf]
save('loading_loop', x, 0.7, phone=True)

# 4. Button: one dry metal click.
c = t(0.12); click = hp(rng.standard_normal(len(c)), 2500) * np.exp(-c * 120) + metal_ring(0.12, 1900) * 0.25 * np.exp(-c * 60)
save('ui_click', click, 0.6)

# 5. Order sent: radio squelch and a short crackle.
s = static(0.45, 2.0) * np.hanning(int(0.45 * SR)); sq = np.sin(2 * np.pi * 2200 * t(0.05)) * np.hanning(int(0.05 * SR)) * 0.4
save('order_radio', np.concatenate([sq, s, sq * 0.6]), 0.55)
print('sounds written to', os.path.abspath(OUT))
