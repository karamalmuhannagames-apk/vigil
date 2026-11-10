"""Generates art from ci/art/prompts.tsv with a free image service. Skips files that already exist."""
import os, sys, time, urllib.parse, urllib.request
out = 'art/raw'; os.makedirs(out, exist_ok=True)
ok = fail = 0
for line in open('ci/art/prompts.tsv', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line or line.startswith('#'): continue
    name, seed, w, h, prompt = line.split('\t')
    path = f'{out}/{name}.jpg'
    if os.path.exists(path): continue
    url = 'https://image.pollinations.ai/prompt/' + urllib.parse.quote(prompt) + f'?width={w}&height={h}&seed={seed}&model=flux&nologo=true&enhance=false'
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'vigil-art/1.0'})
            data = urllib.request.urlopen(req, timeout=180).read()
            if len(data) < 8000: raise RuntimeError('too small: %d bytes' % len(data))
            open(path, 'wb').write(data); print('ok', name, len(data)); ok += 1; break
        except Exception as e:
            print('retry', name, attempt, repr(e)[:200]); time.sleep(12 * (attempt + 1))
    else:
        fail += 1
    time.sleep(6)
print('done', ok, 'new,', fail, 'failed')
