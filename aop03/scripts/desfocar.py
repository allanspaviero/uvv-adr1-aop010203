# -*- coding: utf-8 -*-
"""
AOP03 - Arquitetura de Dados Relacionais I - UVV
Allan Spaviero Alpoim - matricula 202636574

Borra regioes de uma imagem antes de ela entrar no relatorio de evidencias.

As orientacoes da atividade proibem mostrar rostos, criancas e uniformes ou
logos identificaveis nas evidencias de divulgacao. Quando um enquadramento sair
com algo assim visivel, use este utilitario em vez de descartar a foto.

    python aop03/scripts/desfocar.py foto.png 120,80,300,200
    python aop03/scripts/desfocar.py foto.png 120,80,300,200 40,60,90,90

Cada regiao e x,y,largura,altura em pixels, medidos do canto superior esquerdo.
A imagem original nao e alterada: a saida vai para <nome>-desfocada.<extensao>.

ponytail: regiao informada a mao. Deteccao automatica de rosto so se as fotos
da sessao vierem mesmo com rostos - no formato escolhido (videoconferencia com
camera desligada) isso nao deve acontecer.
"""
import pathlib
import sys

from PIL import Image, ImageFilter


def regiao(texto):
    """Converte 'x,y,largura,altura' na caixa (esquerda, topo, direita, base)."""
    try:
        x, y, largura, altura = (int(parte) for parte in texto.split(","))
    except ValueError:
        raise SystemExit(f"Regiao invalida: {texto!r}. Use x,y,largura,altura.")
    if largura <= 0 or altura <= 0:
        raise SystemExit(f"Regiao invalida: {texto!r}. Largura e altura devem ser > 0.")
    return (x, y, x + largura, y + altura)


def desfocar(origem, regioes):
    imagem = Image.open(origem)
    largura, altura = imagem.size

    for caixa in regioes:
        esquerda, topo, direita, base = caixa
        recortada = (max(0, esquerda), max(0, topo),
                     min(largura, direita), min(altura, base))
        if recortada[0] >= recortada[2] or recortada[1] >= recortada[3]:
            print(f"  aviso: regiao {caixa} esta fora da imagem, ignorada")
            continue
        pedaco = imagem.crop(recortada)
        # O raio acompanha o tamanho da regiao: um borrao fixo deixa rosto grande
        # ainda reconhecivel e apaga demais uma regiao pequena.
        raio = max(8, min(pedaco.size) // 4)
        imagem.paste(pedaco.filter(ImageFilter.GaussianBlur(raio)), recortada)

    destino = origem.with_name(f"{origem.stem}-desfocada{origem.suffix}")
    imagem.save(destino)
    return destino


def main(argumentos):
    if len(argumentos) < 2:
        print(__doc__.strip())
        return 1

    origem = pathlib.Path(argumentos[0])
    if not origem.exists():
        print(f"Arquivo nao encontrado: {origem}")
        return 1

    regioes = [regiao(texto) for texto in argumentos[1:]]
    destino = desfocar(origem, regioes)
    print(f"{len(regioes)} regiao(oes) borrada(s) -> {destino}")
    return 0


def demonstracao():
    """Auto-teste sem depender de foto: confere que a regiao muda e o resto nao."""
    import tempfile

    with tempfile.TemporaryDirectory() as pasta:
        origem = pathlib.Path(pasta) / "teste.png"
        imagem = Image.new("RGB", (100, 100), "white")
        for x in range(20, 60, 4):          # listras, para o borrao ter o que borrar
            for y in range(20, 60):
                imagem.putpixel((x, y), (0, 0, 0))
        imagem.save(origem)

        destino = desfocar(origem, [regiao("20,20,40,40")])
        antes, depois = Image.open(origem), Image.open(destino)

        assert antes.getpixel((30, 30)) != depois.getpixel((30, 30)), \
            "a regiao indicada deveria ter sido borrada"
        assert antes.getpixel((90, 90)) == depois.getpixel((90, 90)), \
            "o restante da imagem deveria ficar intacto"
        assert origem.stat().st_size > 0 and destino != origem, \
            "o original nao pode ser sobrescrito"
    print("demonstracao: ok")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demonstracao()
    else:
        sys.exit(main(sys.argv[1:]))
