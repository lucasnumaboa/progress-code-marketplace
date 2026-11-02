"""Gera um produto personalizado: script do SolidCraft, 3MF/STL, imagem e medidas.

Uso:
  python gerar.py <produto> [--nome Thor] [--estilo canelada] [--diametro 140] ... [--saida PASTA]
  python gerar.py --listar

Saída em <PASTA>/<produto>-<estilo>-<nome>/: receita.json, peca.3mf, peca.stl, previa-iso.png,
previa-front.png, medidas.json, parametros.json.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from produtos import FONTES, PRODUTOS, montar  # noqa: E402


def achar_cli():
    """solidcraft-cli.exe instalado pelo 3D Maker do Progress Code (ou SOLIDCRAFT_CLI)."""
    if os.environ.get("SOLIDCRAFT_CLI"):
        return os.environ["SOLIDCRAFT_CLI"]
    raiz = Path(os.environ.get("APPDATA", "")) / "Progress Code" / "tools" / "solidcraft"
    achados = sorted(raiz.glob("v*/*/solidcraft-cli.exe"), key=lambda p: p.stat().st_mtime)
    if not achados:
        sys.exit("solidcraft-cli.exe não encontrado: abra o 3D Maker no Progress Code para instalar o SolidCraft, "
                 "ou defina SOLIDCRAFT_CLI")
    return str(achados[-1])


def rodar(cli, *args):
    r = subprocess.run([cli, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"solidcraft-cli {args[0]} falhou: {(r.stderr or r.stdout).strip()[-1500:]}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("produto", nargs="?")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--saida", default=str(Path.home() / "Documents" / "3D Maker" / "personalizados"))
    ap.add_argument("--sem-previa", action="store_true")
    conhecidos, extras = ap.parse_known_args()
    if conhecidos.listar or not conhecidos.produto:
        for nome, info in PRODUTOS.items():
            print(f"{nome}: padrões {json.dumps(info['padrao'], ensure_ascii=False)}")
            print(f"   limites (mm) {json.dumps(info['limites'])}")
        print("fontes:", ", ".join(FONTES))
        return
    params = {}
    it = iter(extras)
    for chave in it:
        if not chave.startswith("--"):
            sys.exit(f"argumento inesperado: {chave}")
        valor = next(it, None)
        try:
            valor = float(valor) if "." in valor else int(valor)
        except (TypeError, ValueError):
            pass
        params[chave[2:].replace("-", "_")] = valor
    try:
        p, cmds = montar(conhecidos.produto, params)
    except ValueError as e:
        sys.exit(str(e))

    nome_pasta = f"{conhecidos.produto}-{p.get('estilo', 'padrao')}-{p.get('nome') or 'sem-nome'}"
    pasta = Path(conhecidos.saida) / "".join(c if c.isalnum() or c in "-_" else "_" for c in nome_pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    receita = pasta / "receita.json"
    receita.write_text(json.dumps(cmds, ensure_ascii=False, indent=1), encoding="utf-8")

    cli = achar_cli()
    medidas_arq = pasta / "medidas.json"
    # Um único recálculo da receita: exporta tudo e grava as medidas (run sem --results escreve a medição).
    step = pasta / "peca.step"
    rodar(cli, "run", str(receita), "--out", str(pasta / "peca.3mf"), "--out", str(pasta / "peca.stl"),
          "--out", str(step), "--json-out", str(medidas_arq), "--quiet")
    if not conhecidos.sem_previa:
        # As prévias partem do STEP pronto, sem refazer a receita.
        for vista in ("iso", "front"):
            rodar(cli, "snapshot", "--in", str(step), "--out", str(pasta / f"previa-{vista}.png"), "--view", vista,
                  "--width", "900", "--height", "700", "--no-grid", "--no-axes")
    medidas = json.loads(medidas_arq.read_text(encoding="utf-8"))
    (pasta / "parametros.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"pasta": str(pasta), "parametros": p, "medidas": medidas}, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
