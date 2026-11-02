"""Receitas paramétricas dos produtos personalizados, em comandos do SolidCraft (solidcraft-cli).

Cada produto é uma função que recebe os parâmetros (já com os padrões aplicados) e devolve a lista
de comandos que o `solidcraft-cli run` executa. Medidas em mm.

Nome em parede curva: o SolidCraft 0.16.2 só grava texto em face plana (`solid.emboss` em cilindro
aceita apenas retângulos). Por isso cada letra ganha o seu próprio plano tangente, girado em volta
do eixo da peça, e é extrudada até entrar na parede. Com letras de até ~12 mm numa tigela de 70 mm
de raio, a folga entre a face plana da letra e a parede fica em ~0,2 mm.
"""
import math
from pathlib import Path

from PIL import ImageFont

FONTES = {
    "arredondada": r"C:\Windows\Fonts\ARLRDBD.TTF",  # Arial Rounded MT Bold
    "negrito": r"C:\Windows\Fonts\arialbd.ttf",
    "divertida": r"C:\Windows\Fonts\comicbd.ttf",
}
ALTURA_MAIUSCULA = 0.716  # altura da maiúscula / em, medida na Arial; boa aproximação nas três fontes


def largura_letras(texto, fonte, altura):
    """Avanço (mm) de cada letra para uma altura de maiúscula `altura`, pela métrica real da fonte."""
    f = ImageFont.truetype(FONTES[fonte], 1000)
    em = altura / ALTURA_MAIUSCULA
    return [f.getlength(c) / 1000 * em for c in texto]


def nome_em_volta(texto, raio, z_base, altura, fonte, saliencia=1.2, angulo_centro=-90.0, prefixo="Letra"):
    """Comandos que colam `texto` em volta de uma parede cilíndrica de raio `raio`.

    angulo_centro: onde fica o meio do nome (graus; -90 = lado -Y, a frente nas vistas front e iso).
    saliencia: quanto a letra sai da parede (mm). A extrusão entra 1 mm além disso na parede.
    """
    avancos = largura_letras(texto, fonte, altura)
    total = sum(avancos)
    cmds = []
    s = -total / 2
    for i, (c, a) in enumerate(zip(texto, avancos)):
        centro = s + a / 2
        s += a
        if not c.strip():
            continue
        phi = math.radians(angulo_centro) + centro / raio  # sentido de leitura = phi crescente
        n = (math.cos(phi), math.sin(phi), 0.0)          # normal para fora
        t = (-math.sin(phi), math.cos(phi), 0.0)         # direita de quem olha de fora
        r = raio + saliencia
        nome = f"{prefixo}{i + 1}"
        cmds += [
            {"command": "sketch.create", "params": {
                "plane": {"origin": [round(r * n[0], 4), round(r * n[1], 4), 0], "x_dir": list(t), "y_dir": [0, 0, 1]},
                "name": f"{nome}Esboco"}},
            {"command": "sketch.text", "params": {
                "text": c, "at": [0, z_base], "height": altura, "align": "center", "font": FONTES[fonte]}},
            {"command": "solid.extrude", "params": {
                "distance": saliencia + 1.0, "direction": "negative", "operation": "join", "name": nome}},
        ]
    return cmds


def tigela(p):
    """Tigela de parede reta (cilíndrica), com nome em volta.

    estilo: lisa | canelada (frisos verticais na parte de baixo, faixa lisa em cima para o nome).
    """
    D, H, parede, fundo = p["diametro"], p["altura"], p["parede"], p["fundo"]
    R = D / 2
    cmds = [{"command": "solid.cylinder", "params": {"diameter": D, "height": H, "name": "Corpo"}}]
    faixa_nome = p["altura_letra"] + 8
    if p["estilo"] == "canelada":
        # Frisos: meia-cana saliente, só abaixo da faixa do nome.
        h_friso = H - faixa_nome - 3
        cmds += [
            {"command": "solid.cylinder", "params": {
                "diameter": p["friso"], "height": h_friso, "base": [R, 0, 3], "operation": "join", "name": "Friso"}},
            {"command": "solid.pattern.circular", "params": {
                "features": ["Friso"], "axis": "Z", "count": p["n_frisos"], "name": "Frisos"}},
        ]
    if p["nome"]:
        if p["estilo"] == "canelada":
            z_base = H - faixa_nome / 2 - p["altura_letra"] / 2  # no meio da faixa lisa de cima
        else:
            z_base = H / 2 - p["altura_letra"] / 2               # no meio da altura
        cmds += nome_em_volta(p["nome"], R, z_base, p["altura_letra"], p["fonte"], p["saliencia"])
    ri = R - parede
    cmds += [
        {"command": "solid.cylinder", "params": {
            "diameter": D - 2 * parede, "height": H, "base": [0, 0, fundo], "operation": "cut", "name": "Miolo"}},
        # Borda arredondada (conforto) e canto interno do fundo arredondado (limpeza). Pontos em +X,
        # longe do nome (que fica em -Y) e acima dos frisos.
        {"command": "solid.fillet", "params": {"edges": [[R, 0, H], [ri, 0, H]], "radius": min(1.0, parede / 3),
                                               "name": "Borda"}},
        {"command": "solid.fillet", "params": {"edges": [[ri, 0, fundo]], "radius": p["raio_fundo"],
                                               "name": "FundoInterno"}},
    ]
    return cmds


def plaquinha(p):
    """Plaquinha de coleira redonda com furo e nome em relevo na frente."""
    D, esp = p["diametro"], p["espessura"]
    cmds = [
        {"command": "solid.cylinder", "params": {"diameter": D, "height": esp, "name": "Placa"}},
        {"command": "solid.cylinder", "params": {
            "diameter": p["furo"], "height": esp + 2, "base": [0, D / 2 - p["furo"] / 2 - 2, -1],
            "operation": "cut", "name": "Furo"}},
    ]
    if p["nome"]:
        cmds += [
            {"command": "sketch.create", "params": {"plane": "XY", "offset": str(esp), "name": "NomeEsboco"}},
            {"command": "sketch.text", "params": {
                "text": p["nome"], "at": [0, -p["altura_letra"] / 2 - 1], "height": p["altura_letra"],
                "align": "center", "font": FONTES[p["fonte"]]}},
            {"command": "solid.extrude", "params": {"distance": p["saliencia"], "operation": "join", "name": "Nome"}},
        ]
    return cmds


PRODUTOS = {
    "tigela": {
        "funcao": tigela,
        "padrao": {"estilo": "lisa", "diametro": 140, "altura": 60, "parede": 4, "fundo": 4,
                   "nome": "", "fonte": "arredondada", "altura_letra": 12, "saliencia": 1.2,
                   "friso": 6, "n_frisos": 36, "raio_fundo": 6},
        "limites": {"diametro": (80, 220), "altura": (35, 110), "parede": (2.4, 8), "fundo": (2.4, 8),
                    "altura_letra": (7, 20), "raio_fundo": (0.5, 15)},
    },
    "plaquinha": {
        "funcao": plaquinha,
        "padrao": {"diametro": 32, "espessura": 3, "furo": 4, "nome": "", "fonte": "arredondada",
                   "altura_letra": 6, "saliencia": 0.8},
        "limites": {"diametro": (22, 45), "espessura": (2, 5), "furo": (3, 6), "altura_letra": (4, 9)},
    },
}


def montar(produto, params):
    """Aplica padrões e limites e devolve (parâmetros finais, comandos)."""
    if produto not in PRODUTOS:
        raise ValueError(f"produto desconhecido: {produto} (há: {', '.join(PRODUTOS)})")
    info = PRODUTOS[produto]
    p = {**info["padrao"], **{k: v for k, v in params.items() if v is not None}}
    for k, (lo, hi) in info["limites"].items():
        if not lo <= float(p[k]) <= hi:
            raise ValueError(f"{k}={p[k]} fora do limite {lo}–{hi} mm")
    if p.get("fonte") not in FONTES:
        raise ValueError(f"fonte desconhecida: {p.get('fonte')} (há: {', '.join(FONTES)})")
    if not Path(FONTES[p["fonte"]]).exists():
        raise ValueError(f"fonte não instalada: {FONTES[p['fonte']]}")
    return p, info["funcao"](p)
