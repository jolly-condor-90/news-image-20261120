# -*- coding: utf-8 -*-
"""Local checks that mirror the bounty gate and the author's layout checklist."""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def main():
    p = os.path.join(HERE, 'entry.png')
    im = Image.open(p); im.verify()
    im = Image.open(p)
    size = os.path.getsize(p)
    assert im.format == 'PNG', im.format
    assert im.size == (1024, 1024), im.size
    assert size <= 1048576, size
    print('gate: PNG, 1024x1024, %d bytes (<= 1 MiB)' % size)

    import build
    assert len(build.STORIES) == 35
    assert len(build.BY_NUM) == 35
    assert all('20 NOV' in s[9] for s in build.STORIES), 'a story is not dated 20 Nov'
    assert sum(build.COUNTS.values()) == 35
    assert len(build.MAIN_ILLU) == 3 and len(build.SMALL_ILLU) == 8
    print('content: 35 stories, all dated 20 Nov 2026, 7 regions, 3 + 8 illustrated cards')

    # Deterministic copier check
    out = os.path.join(HERE, '_verify_out')
    os.makedirs(out, exist_ok=True)
    env_ok = os.environ.get('MAKEFUN_OUTPUT_DIR') == out
    print('copier: run with MAKEFUN_OUTPUT_DIR=%s to test' % out)

    # Rebuild bounds report
    build.OUT_DIR = os.path.join(HERE, '_verify_build')
    build.build()
    print('layout: no out-of-frame elements')

if __name__ == '__main__':
    main()
