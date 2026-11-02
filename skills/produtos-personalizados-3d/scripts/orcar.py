"""Fatia a peça no Bambu Studio (CLI) e calcula custo e preço de venda na Shopee.

Uso:
  python orcar.py <peca.3mf|stl> [--material PETG|PLA] [--paredes 4] [--suporte] [--embalagem 2]
                  [--preco 59.90]

Configuração (custos da loja) em %APPDATA%\\Progress Code\\produtos-personalizados-3d\\config.json,
fora da pasta da skill para sobreviver a atualizações. O primeiro uso cria o arquivo com valores de
exemplo. Revise os valores: são do dono da loja, não regras fixas.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

CONFIG = Path(os.environ.get("APPDATA", Path.home())) / "Progress Code" / "produtos-personalizados-3d" / "config.json"
CONFIG_PADRAO = {
    "impressora": "Bambu Lab A1 0.4 nozzle",
    "processo": "0.20mm Standard @BBL A1",
    "filamentos": {"PETG": "Bambu PETG Basic @BBL A1", "PLA": "Bambu PLA Basic @BBL A1"},
    "preco_kg": {"PETG": 60.0, "PLA": 100.0},
    "potencia_kw": 0.095,
    "tarifa_kwh": 0.95,
    "perda": 0.10,
    "embalagem": 4.0,
    "lucro_alvo": 0.35,
    "shopee": {"faixas": [[80, 0.20, 4.50], [100, 0.14, 16.0], [200, 0.14, 20.0], [999999, 0.14, 26.0]],
               "adicional_cpf": 3.0},
}


def config():
    if not CONFIG.exists():
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps(CONFIG_PADRAO, ensure_ascii=False, indent=1), encoding="utf-8")
    return {**CONFIG_PADRAO, **json.loads(CONFIG.read_text(encoding="utf-8"))}


def bambu_exe():
    for c in (os.environ.get("BAMBU_STUDIO"), r"C:\Program Files\Bambu Studio\bambu-studio.exe"):
        if c and Path(c).exists():
            return c
    sys.exit("Bambu Studio não encontrado (defina BAMBU_STUDIO com o caminho do bambu-studio.exe)")


def preset(tipo, nome):
    """Preset de sistema com a cadeia de 'inherits' resolvida."""
    sistema = Path(os.environ["APPDATA"]) / "BambuStudio" / "system" / "BBL" / tipo
    achados = list(sistema.rglob(f"{nome}.json"))
    if not achados:
        sys.exit(f"preset não encontrado: {tipo}/{nome} (abra o Bambu Studio uma vez para baixar os presets)")
    dados = json.loads(achados[0].read_text(encoding="utf-8"))
    pai = dados.pop("inherits", None)
    base = preset(tipo, pai) if pai else {}
    base.update(dados)
    return base


def fatiar(peca, material, suporte, paredes, cfg):
    """Devolve (horas, gramas). Contornos do CLI comprovados no Bambu Studio 2.x:
    -17 sem compatible_printers no processo/filamento; -50 sem 'inherits' na impressora;
    -61 sem curr_bed_type compatível com o filamento."""
    tmp = Path(tempfile.mkdtemp())
    maq = preset("machine", cfg["impressora"])
    proc = preset("process", cfg["processo"])
    fil = preset("filament", cfg["filamentos"][material])
    maq.update({"from": "User", "inherits": cfg["impressora"]})
    proc["curr_bed_type"] = "Textured PEI Plate"
    if paredes:
        proc["wall_loops"] = str(paredes)
    if suporte:
        proc.update({"enable_support": "1", "support_type": "tree(auto)"})
    for d in (proc, fil):
        d.update({"from": "User", "compatible_printers": [cfg["impressora"]], "compatible_printers_condition": ""})
    for nome, d in (("m", maq), ("p", proc), ("f", fil)):
        (tmp / f"{nome}.json").write_text(json.dumps(d), encoding="utf-8")
    saida = tmp / "fatiado.3mf"
    r = subprocess.run([bambu_exe(), "--arrange", "1",
                        "--load-settings", f"{tmp / 'm.json'};{tmp / 'p.json'}",
                        "--load-filaments", str(tmp / "f.json"),
                        "--slice", "0", "--export-3mf", str(saida), str(Path(peca).resolve())],
                       capture_output=True, text=True, timeout=3600, cwd=tmp)  # o CLI grava result.json no cwd
    if not saida.exists():
        cod = r.returncode - (1 << 32) if r.returncode > (1 << 31) else r.returncode
        sys.exit(f"fatiamento falhou (código {cod}; -50 = peça fora da mesa, -100 = erro de fatiamento)")
    info = zipfile.ZipFile(saida).read("Metadata/slice_info.config").decode()
    seg = sum(int(v) for v in re.findall(r'key="prediction" value="(\d+)"', info))
    pesos = re.findall(r'key="weight" value="([\d.]+)"', info)
    gramas = sum(map(float, pesos)) if pesos else sum(map(float, re.findall(r'used_g="([\d.]+)"', info)))
    return seg / 3600, gramas


def taxa_shopee(preco, cfg):
    for limite, pct, fixa in cfg["shopee"]["faixas"]:
        if preco < limite:
            return preco * pct + fixa + cfg["shopee"]["adicional_cpf"]


def preco_sugerido(custo, cfg):
    """Menor preço terminado em ,90 que deixa o lucro_alvo depois de custo e taxas."""
    p = 9.90
    while p < 2000:
        if p - custo - taxa_shopee(p, cfg) >= cfg["lucro_alvo"] * p:
            return p
        p += 1.0
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("peca")
    ap.add_argument("--material", default="PETG", choices=["PETG", "PLA"])
    ap.add_argument("--suporte", action="store_true")
    ap.add_argument("--paredes", type=int, help="perímetros (wall_loops); tigela para água: 4 ou mais")
    ap.add_argument("--embalagem", type=float, help="custo da embalagem deste produto (R$)")
    ap.add_argument("--preco", type=float, help="preço que você quer conferir (opcional)")
    a = ap.parse_args()
    cfg = config()
    if a.embalagem is not None:
        cfg["embalagem"] = a.embalagem
    horas, gramas = fatiar(a.peca, a.material, a.suporte, a.paredes, cfg)
    energia = horas * cfg["potencia_kw"] * cfg["tarifa_kwh"]
    filamento = gramas * (1 + cfg["perda"]) * cfg["preco_kg"][a.material] / 1000
    custo = energia + filamento + cfg["embalagem"]
    preco = a.preco or preco_sugerido(custo, cfg)
    taxa = taxa_shopee(preco, cfg)
    lucro = preco - custo - taxa
    print(json.dumps({
        "material": a.material, "paredes": a.paredes or "padrão do perfil", "horas": round(horas, 2),
        "gramas": round(gramas, 1),
        "energia": round(energia, 2), "filamento": round(filamento, 2), "embalagem": cfg["embalagem"],
        "custo": round(custo, 2), "preco": round(preco, 2), "taxa_shopee": round(taxa, 2),
        "lucro": round(lucro, 2), "margem": f"{lucro / preco:.0%}",
        "preco_sugerido": not a.preco, "config": str(CONFIG),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
