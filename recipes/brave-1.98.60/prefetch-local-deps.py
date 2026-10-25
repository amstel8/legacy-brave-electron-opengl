from pathlib import Path
import concurrent.futures,json,re,subprocess
w=Path.home()/'Documents/chromium-build'
brave=w/'projects/brave-stable-1.97.56'
electron=w/'projects/electron'
entries=json.loads((w/'logs/brave-1.98.60-dependency-revisions.json').read_text())
def has(repo,sha):
    return subprocess.run(['git','-C',str(repo),'cat-file','-e',sha+'^{commit}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
def prefetch(item):
    path,info=item;sha=info.get('rev') or '';target=brave/path
    if not re.fullmatch('[0-9a-f]{40}',sha) or not (target/'.git').exists() or has(target,sha):return
    source=electron/path
    if (source/'.git').exists() and has(source,sha):
        print('Reusing exact Electron dependency:',path,sha,flush=True)
        subprocess.run(['git','-C',str(target),'fetch','--depth=1','--no-tags',str(source),sha],check=True)
    else:
        print('Fetching exact upstream dependency:',path,sha,flush=True)
        subprocess.run(['git','-C',str(target),'fetch','--depth=1','--no-tags','origin',sha],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(prefetch,entries.items()))
print('Exact dependency revisions available locally.',flush=True)
