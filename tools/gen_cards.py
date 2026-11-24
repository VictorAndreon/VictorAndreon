"""Gera os cards de terminal (SVG) do README do perfil.

Uso (a partir da raiz do repositório):
    python3 tools/gen_cards.py

Edite o texto no dicionário `cards` abaixo e rode de novo. Os SVGs saem em cards/.
"""
import html, os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cards")
W = 860
LH = 24
PROMPT = '<tspan class="p">victor@passo-fundo</tspan><tspan class="d">:</tspan><tspan class="path">~</tspan><tspan class="d">$ </tspan>'

def seg(cls, txt):
    return f'<tspan class="{cls}">{html.escape(txt)}</tspan>'

# each line: list of (class, text); None = blank line; "cmd:xxx" = prompt line
cards = {
 "whoami": ("Sobre: Victor Hugo Andreon, Desenvolvedor Full-Stack, IA aplicada", [
   "cmd:whoami",
   [("c", "victor")],
   "cmd:cat sobre.txt",
   [("h", "Victor Hugo Andreon"), ("c", " · Desenvolvedor Full-Stack · IA aplicada")],
   [("d", "Veplex Sistemas de Informação · Passo Fundo, RS · Ciência da Computação @ IFSul")],
   None,
   "cmd:cat agora.txt",
   [("c", "Estudando backend além do Laravel e me aprofundando em LLMs, RAG e agentes.")],
 ]),
 "destaques": ("Destaques", [
   "cmd:cat destaques.log",
   [("y", "[voz]   "), ("c", "áudio → transcrição (OpenAI) → LLM → pedido em JSON estruturado")],
   [("y", "[busca] "), ("c", "pgvector + pg_trgm, ranking top-3 "), ("d", "· ~80% de acerto nos testes")],
   [("y", "[sql]   "), ("c", "PostgreSQL 120 s → 0,3 s "), ("d", "· EXISTS → JOIN + tabela temporária")],
 ]),
 "stack": ("Stack", [
   "cmd:cat stack.txt",
   [("m", "dia a dia  "), ("c", "PHP · Laravel · PostgreSQL · React · OpenAI API · pgvector")],
   [("m", "também     "), ("c", "TypeScript · Node.js · Electron · Python · Docker · Git")],
 ]),
 "projetos": ("Projetos", [
   "cmd:cat projetos.txt",
   [("path", "Clawd-mini     "), ("d", "mascote Linux que reage ao Claude Code (TypeScript, Electron)")],
   [("path", "orquestrador   "), ("d", "fila de prioridade com Factory/Observer e testes (Python)")],
   "prompt",
 ]),
}
nlines = {k: len(v[1]) for k, v in cards.items()}

STYLE = """<style>
text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;font-size:15px;white-space:pre}
.p{fill:#3fb950}.path{fill:#58a6ff}.c{fill:#e6edf3}.d{fill:#8b949e}.y{fill:#e3b341}.m{fill:#d2a8ff}.g{fill:#3fb950;opacity:.7}
.h{fill:#f0f6fc;font-weight:bold;font-size:17px}.t{fill:#8b949e;font-size:13px}
.cur{fill:#3fb950;animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}
</style>"""

for name, (title, lines) in cards.items():
    H = 38 + 26 + nlines[name] * LH + 10
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">', STYLE,
           f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="#0d1117" stroke="#30363d"/>',
           f'<path d="M.5 10.5a10 10 0 0 1 10-10h{W-21}a10 10 0 0 1 10 10v27h-{W-1}z" fill="#161b22"/>',
           f'<line x1="0" y1="38" x2="{W}" y2="38" stroke="#30363d"/>',
           '<circle cx="20" cy="19" r="5.5" fill="#ff5f57"/><circle cx="38" cy="19" r="5.5" fill="#febc2e"/><circle cx="56" cy="19" r="5.5" fill="#28c840"/>',
           f'<text x="{W//2}" y="23" text-anchor="middle" class="t">victor@passo-fundo: ~</text>']
    y = 38 + 26
    for ln in lines:
        if ln is None:
            pass
        elif ln == "prompt":
            out.append(f'<text x="26" y="{y}">{PROMPT}<tspan class="cur">█</tspan></text>')
        elif isinstance(ln, str):
            out.append(f'<text x="26" y="{y}">{PROMPT}{seg("c", ln[4:])}</text>')
        else:
            out.append(f'<text x="26" y="{y}">' + "".join(seg(c, t) for c, t in ln) + '</text>')
        y += LH
    out.append('</svg>')
    open(f"{OUT}/{name}.svg", "w").write("\n".join(out) + "\n")
print("ok")
