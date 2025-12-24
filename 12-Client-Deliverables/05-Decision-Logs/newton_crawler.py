#!/usr/bin/env python3
"""
NEWTON AGENT - STEM KNOWLEDGE CRAWLER
=====================================
PhD-level STEM knowledge base from top YouTube channels.

Primary Channels: Veritasium, 3Blue1Brown, PBS Space Time,
MIT OpenCourseWare, Fermilab, NileRed, Scott Manley

Uses yt-dlp for searching (no API key needed).
Requires youtube_cookies.txt for transcript requests.
"""

import os
import subprocess
import json
import time
import re
import tempfile
from datetime import datetime

OUTPUT_DIR = "G:/My Drive/00 - Trajanus USA/01-Morning-Sessions/Research/Newton_Knowledge"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(SCRIPTS_DIR, "youtube_cookies.txt")

PRIORITY_CHANNELS = [
    "veritasium", "3blue1brown", "pbs space time", "pbsspacetime",
    "mit opencourseware", "mitocw", "fermilab", "nilered", "nile red",
    "scott manley", "minutephysics", "numberphile", "computerphile",
    "standupmaths", "mathologer", "smarter every day", "kurzgesagt",
    "two minute papers", "sabine hossenfelder", "periodic videos",
    "real engineering", "practical engineering", "sixty symbols"
]

AVOID_TERMS = ["reaction", "vlog", "unboxing", "challenge", "prank", "#shorts"]

QUERIES = [
    # PHYSICS (20)
    "Veritasium quantum mechanics explained",
    "PBS Space Time quantum field theory",
    "quantum entanglement tutorial physics",
    "special relativity explained physics",
    "general relativity spacetime curvature",
    "thermodynamics laws explained physics lecture",
    "statistical mechanics entropy Boltzmann",
    "particle physics standard model explained",
    "Fermilab higgs boson explained",
    "electromagnetism Maxwell equations tutorial",
    "wave particle duality quantum mechanics",
    "Schrodinger equation explained physics",
    "Heisenberg uncertainty principle derivation",
    "nuclear physics fission fusion reactions",
    "condensed matter physics semiconductors",
    "optics physics light waves interference",
    "fluid dynamics Navier Stokes equations",
    "classical mechanics Lagrangian Hamiltonian",
    "PBS Space Time black holes physics",
    "dark matter dark energy cosmology",
    # MATHEMATICS (20)
    "3Blue1Brown calculus essence visual",
    "3Blue1Brown linear algebra essence",
    "differential equations tutorial mathematics",
    "3Blue1Brown neural networks gradient descent",
    "Fourier transform explained visualization",
    "complex analysis mathematics tutorial",
    "topology mathematics introduction",
    "group theory abstract algebra lecture",
    "number theory prime numbers distribution",
    "real analysis limits continuity proofs",
    "probability theory statistics mathematics",
    "discrete mathematics combinatorics graphs",
    "graph theory algorithms computer science",
    "numerical methods mathematics computation",
    "partial differential equations PDE tutorial",
    "tensor calculus mathematics physics",
    "manifolds differential geometry topology",
    "cryptography mathematics RSA elliptic",
    "game theory mathematics Nash equilibrium",
    "chaos theory dynamical systems attractors",
    # ENGINEERING (15)
    "MIT OpenCourseWare electrical engineering circuits",
    "control systems engineering feedback loops",
    "signal processing Fourier analysis DSP",
    "mechanical engineering thermodynamics cycles",
    "aerospace engineering orbital mechanics",
    "Scott Manley rocket science propulsion",
    "materials science engineering metallurgy",
    "structural engineering mechanics stress",
    "computer architecture engineering CPU",
    "digital electronics logic gates FPGA",
    "analog circuit design engineering amplifiers",
    "robotics engineering kinematics control",
    "biomedical engineering prosthetics",
    "chemical engineering process design reactors",
    "civil engineering structures bridges",
    # CHEMISTRY (15)
    "NileRed organic chemistry synthesis",
    "organic chemistry reaction mechanisms arrows",
    "inorganic chemistry coordination complexes",
    "physical chemistry thermodynamics kinetics",
    "biochemistry molecular biology proteins",
    "electrochemistry batteries fuel cells",
    "polymer chemistry materials synthesis",
    "analytical chemistry spectroscopy NMR",
    "quantum chemistry molecular orbitals",
    "NileRed chemical reactions experiments",
    "periodic table chemistry elements properties",
    "chemical bonding molecular structure VSEPR",
    "acid base chemistry equilibrium pH",
    "catalysis chemistry enzymes mechanisms",
    "nuclear chemistry radioactivity decay",
    # ASTROPHYSICS (10)
    "PBS Space Time cosmology universe expansion",
    "stellar evolution stars lifecycle HR diagram",
    "black holes astrophysics singularity event horizon",
    "neutron stars pulsars magnetars physics",
    "galaxy formation cosmology dark matter",
    "cosmic microwave background CMB analysis",
    "gravitational waves LIGO detection",
    "exoplanets habitable zones detection methods",
    "big bang cosmology inflation theory",
    "Scott Manley astrophysics spaceflight",
    # EMERGING TECH (10)
    "quantum computing qubits superposition gates",
    "CRISPR gene editing mechanism Cas9",
    "nuclear fusion energy ITER tokamak stellarator",
    "artificial intelligence machine learning tutorial",
    "neural networks deep learning backpropagation",
    "nanotechnology materials science applications",
    "renewable energy solar photovoltaic wind",
    "SpaceX rocket technology reusability Starship",
    "biotechnology synthetic biology genetic",
    "quantum supremacy computing Google Sycamore"
]

def is_quality_content(channel, title):
    combined = (channel + " " + title).lower()
    for term in AVOID_TERMS:
        if term in combined:
            return False, f"Low quality: {term}"
    return True, "OK"

def is_priority_channel(channel):
    for p in PRIORITY_CHANNELS:
        if p in channel.lower():
            return True
    return False

def sanitize_filename(text):
    s = re.sub(r'[<>:"/\\|?*]', '', text)
    return re.sub(r'\s+', '_', s)[:60]

def check_cookies():
    return os.path.exists(COOKIES_FILE)

def search_youtube(query, max_results=2):
    try:
        cmd = ['yt-dlp', '--js-runtimes', 'node', f'ytsearch{max_results*3}:{query}',
               '--flat-playlist', '--dump-json', '--no-warnings', '--quiet']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                                encoding='utf-8', errors='replace')
        videos, rejected = [], []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            try:
                d = json.loads(line)
                vid_id, title = d.get('id',''), d.get('title','')
                channel = d.get('channel', d.get('uploader',''))
                duration = d.get('duration', 0)
                if duration and (duration < 180 or duration > 10800):
                    continue
                ok, reason = is_quality_content(channel, title)
                if not ok:
                    rejected.append({'channel':channel,'title':title,'reason':reason})
                    continue
                videos.append({'video_id':vid_id, 'title':title, 'channel':channel,
                               'duration':duration, 'is_priority':is_priority_channel(channel)})
                if len(videos) >= max_results:
                    break
            except:
                continue
        videos.sort(key=lambda x: (0 if x['is_priority'] else 1, x['title']))
        return videos[:max_results], rejected
    except:
        return [], []

def parse_vtt(content):
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        if not line or '-->' in line or line.isdigit():
            continue
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        if line:
            lines.append(line)
    return ' '.join(lines)

def get_transcript_ytdlp(video_id, use_cookies=False):
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, '%(id)s')
            cmd = ['yt-dlp', '--js-runtimes', 'node', '--write-auto-sub', '--write-sub',
                   '--sub-lang', 'en', '--sub-format', 'vtt', '--skip-download',
                   '-o', out, '--quiet', '--no-warnings']
            if use_cookies and os.path.exists(COOKIES_FILE):
                cmd.extend(['--cookies', COOKIES_FILE])
            cmd.append(f'https://www.youtube.com/watch?v={video_id}')
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                                    encoding='utf-8', errors='replace')
            for ext in ['.en.vtt', '.en-orig.vtt', '.vtt']:
                f = os.path.join(tmp, f'{video_id}{ext}')
                if os.path.exists(f):
                    with open(f, 'r', encoding='utf-8') as fp:
                        text = parse_vtt(fp.read())
                    if text and len(text) > 100:
                        return text, "Success"
            if 'Sign in' in result.stderr or 'bot' in result.stderr.lower():
                return None, "Blocked: Need cookies"
            return None, "No transcript"
    except:
        return None, "Error"

def get_transcript_api(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        data = api.fetch(video_id, languages=['en'])
        texts = [e.text if hasattr(e,'text') else e.get('text','') for e in data]
        text = ' '.join(texts)
        return (text, "Success") if text else (None, "Empty")
    except Exception as e:
        return None, str(e)[:40]

def get_transcript(video_id, use_cookies=False):
    if use_cookies:
        t, s = get_transcript_ytdlp(video_id, True)
        if t: return t, s
    t, s = get_transcript_ytdlp(video_id, False)
    if t: return t, s
    return get_transcript_api(video_id)

def categorize(query):
    q = query.lower()
    if any(t in q for t in ['quantum mechanics','relativity','thermodynamics','particle','electromagnetism','fluid','schrodinger','heisenberg','fermilab','black hole','dark matter']):
        return "Physics"
    if any(t in q for t in ['calculus','linear algebra','3blue1brown','fourier','topology','group theory','number theory','probability','chaos','tensor']):
        return "Mathematics"
    if any(t in q for t in ['engineering','circuit','control system','signal','aerospace','mechanical','robotics','mit opencourseware']):
        return "Engineering"
    if any(t in q for t in ['chemistry','organic','nilered','electrochemistry','biochemistry','periodic','catalysis']):
        return "Chemistry"
    if any(t in q for t in ['cosmology','stellar','neutron star','galaxy','gravitational wave','exoplanet','big bang','scott manley']):
        return "Astrophysics"
    if any(t in q for t in ['quantum computing','crispr','fusion','machine learning','neural network','nanotechnology','spacex','biotechnology']):
        return "EmergingTech"
    return "STEM"

def main():
    start = datetime.now()
    print(f"\n{'='*70}")
    print(f"  NEWTON AGENT - STEM KNOWLEDGE CRAWLER")
    print(f"{'='*70}\n")
    print(f"  Queries: {len(QUERIES)} | Output: {OUTPUT_DIR}")
    print(f"  Started: {start.strftime('%Y-%m-%d %H:%M:%S')}")

    has_cookies = check_cookies()
    if has_cookies:
        print(f"  [OK] Cookies found")
    else:
        print(f"  [!] No cookies - YouTube may block")
    print(f"\n{'='*70}\n")

    stats = {'queries':len(QUERIES), 'searched':0, 'downloaded':0, 'blocked':0,
             'priority':0, 'by_cat':{}, 'videos':[], 'blocked_list':[], 'seen':set()}

    for i, query in enumerate(QUERIES, 1):
        cat = categorize(query)
        print(f"\n[{i}/{len(QUERIES)}] [{cat}] {query[:50]}...")
        results, _ = search_youtube(query, 2)
        if not results:
            print("  [SKIP] No results")
            continue
        for v in results:
            vid, title, channel = v['video_id'], v['title'], v['channel']
            if vid in stats['seen']:
                print(f"  [DUP] {title[:40]}")
                continue
            stats['seen'].add(vid)
            stats['searched'] += 1
            prio = "[PRIORITY]" if v['is_priority'] else ""
            print(f"  {prio} [{channel[:20]}] {title[:35]}...")
            if v['is_priority']:
                stats['priority'] += 1
            text, status = get_transcript(vid, has_cookies)
            if text:
                fname = f"{cat}_{vid}_{sanitize_filename(title)}.txt"
                path = os.path.join(OUTPUT_DIR, fname)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"{'='*70}\nNEWTON KNOWLEDGE BASE - STEM TRANSCRIPT\n{'='*70}\n\n")
                    f.write(f"Title: {title}\nChannel: {channel}\nVideo ID: {vid}\n")
                    f.write(f"URL: https://www.youtube.com/watch?v={vid}\n")
                    f.write(f"Category: {cat}\nQuery: {query}\nPriority: {v['is_priority']}\n")
                    f.write(f"Downloaded: {datetime.now()}\n\n{'='*70}\nTRANSCRIPT\n{'='*70}\n\n{text}")
                kb = len(text)//1024
                stats['downloaded'] += 1
                stats['by_cat'][cat] = stats['by_cat'].get(cat,0) + 1
                stats['videos'].append({'id':vid,'title':title,'channel':channel,'cat':cat,'kb':kb,'prio':v['is_priority']})
                print(f"    [OK] {kb} KB")
            else:
                if 'block' in status.lower():
                    stats['blocked'] += 1
                    stats['blocked_list'].append({'id':vid,'title':title,'channel':channel})
                print(f"    [SKIP] {status}")
            time.sleep(1.5)
        time.sleep(0.5)

    end = datetime.now()
    print(f"\n\n{'='*70}")
    print(f"  NEWTON AGENT - COMPLETE")
    print(f"{'='*70}\n")
    print(f"  Queries: {stats['queries']} | Searched: {stats['searched']}")
    print(f"  Downloaded: {stats['downloaded']} | Blocked: {stats['blocked']}")
    print(f"  Priority sources: {stats['priority']}")
    if stats['searched']>0:
        print(f"  Success rate: {stats['downloaded']/stats['searched']*100:.1f}%")
    print(f"\n  By Category:")
    for c,n in stats['by_cat'].items():
        print(f"    {c}: {n}")
    print(f"\n  Runtime: {end-start}")

    # Count files
    total_size = sum(os.path.getsize(os.path.join(OUTPUT_DIR,f))
                     for f in os.listdir(OUTPUT_DIR) if f.endswith('.txt') and not f.startswith('_'))
    print(f"  Total size: {total_size/(1024*1024):.2f} MB")

    if stats['blocked']>0:
        print(f"\n  [!] {stats['blocked']} blocked - run export_youtube_cookies.py as Admin")

    # Write report
    with open(os.path.join(OUTPUT_DIR,"_CRAWL_REPORT.txt"), 'w') as f:
        f.write(f"NEWTON CRAWLER REPORT\n{'='*50}\n")
        f.write(f"Date: {start}\nDuration: {end-start}\n")
        f.write(f"Downloaded: {stats['downloaded']}\nBlocked: {stats['blocked']}\n\n")
        f.write("DOWNLOADED:\n")
        for v in stats['videos']:
            f.write(f"[{v['cat']}] {v['title'][:50]}\n  {v['channel']} | {v['kb']}KB\n\n")
        if stats['blocked_list']:
            f.write("\nBLOCKED:\n")
            for v in stats['blocked_list']:
                f.write(f"{v['title'][:50]}\n  {v['channel']}\n\n")

    print(f"\n{'='*70}")
    print(f"  Ready for TKB ingestion!")
    print(f"{'='*70}\n")
    return stats

if __name__ == '__main__':
    main()
