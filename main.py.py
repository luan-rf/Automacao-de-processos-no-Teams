from pathlib import Path
import logging
import time

import pandas as pd
import pyautogui as py
import pyperclip


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"

PLANILHA = DATA_DIR / "chamados_cancelados.xlsx"

COLUNA_CHAMADO = "Numero_Chamado"
COLUNA_STATUS = "Status_Processamento"

IMAGE_CONFIDENCE = 0.8
IMAGE_GRAYSCALE = True

TEMPO_ESPERA_PADRAO = 1
TEMPO_VERIFICACAO_FILTRO = 5
TEMPO_VERIFICACAO_CHAMADO = 3

# Coordenadas utilizadas para interação com elementos
# que não possuem uma referência visual dedicada.
COORDENADA_SELECAO_CONTA = (2198, 29)
COORDENADA_CONTA = (2184, 514)
COORDENADA_ACAO_LISTA = (2482, 1283)


# ============================================================
# IMAGENS
# ============================================================

IMG_APROVACOES = IMAGES_DIR / "aprovacoes_teams.png"
IMG_ENVIADOS = IMAGES_DIR / "botao_enviados.png"
IMG_FILTRAR = IMAGES_DIR / "botao_filtrar.png"
IMG_CANCELAR = IMAGES_DIR / "btn_cancelar_pedido.png"
IMG_NAO_ENCONTRADO = IMAGES_DIR / "nao_encontrado.png"
IMG_STATUS_CANCELADO = IMAGES_DIR / "status_cancelado.png"
IMG_STATUS_SOLICITADO = IMAGES_DIR / "status_solicitado.png"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# FUNÇÕES DE AUTOMAÇÃO VISUAL
# ============================================================

def localizar_imagem(imagem: Path):
    """
    Localiza uma imagem na tela.

    Retorna a posição encontrada ou None caso o elemento
    não esteja visível.
    """
    try:
        return py.locateOnScreen(
            str(imagem),
            grayscale=IMAGE_GRAYSCALE,
            confidence=IMAGE_CONFIDENCE,
        )
    except py.ImageNotFoundException:
        return None


def aguarda_imagem(imagem: Path, intervalo: float = 1):
    """
    Aguarda indefinidamente até que a imagem seja encontrada.
    """
    logger.info("Aguardando elemento: %s", imagem.name)

    while True:
        posicao = localizar_imagem(imagem)

        if posicao is not None:
            return posicao

        time.sleep(intervalo)


def imagem_visivel(imagem: Path, tempo_limite: int = 3) -> bool:
    """
    Verifica se uma imagem aparece na tela dentro do tempo limite.
    """
    inicio = time.time()

    while time.time() - inicio < tempo_limite:
        if localizar_imagem(imagem) is not None:
            return True

        time.sleep(0.5)

    return False


def clicar_imagem(imagem: Path):
    """
    Aguarda uma imagem aparecer e clica no centro dela.
    """
    posicao = aguarda_imagem(imagem)
    py.click(py.center(posicao))


def escrever_texto(texto):
    """
    Insere texto utilizando a área de transferência.
    """
    pyperclip.copy(str(texto))
    py.hotkey("ctrl", "v")


# ============================================================
# VALIDAÇÃO
# ============================================================

def validar_arquivos():
    """
    Verifica se os arquivos necessários para a execução existem.
    """
    if not PLANILHA.exists():
        raise FileNotFoundError(
            f"Planilha não encontrada: {PLANILHA}"
        )

    imagens_obrigatorias = [
        IMG_APROVACOES,
        IMG_ENVIADOS,
        IMG_FILTRAR,
        IMG_CANCELAR,
        IMG_NAO_ENCONTRADO,
        IMG_STATUS_CANCELADO,
        IMG_STATUS_SOLICITADO,
    ]

    imagens_faltantes = [
        imagem.name
        for imagem in imagens_obrigatorias
        if not imagem.exists()
    ]

    if imagens_faltantes:
        raise FileNotFoundError(
            "Imagens de referência não encontradas: "
            + ", ".join(imagens_faltantes)
        )


def carregar_planilha() -> pd.DataFrame:
    """
    Carrega e valida a planilha de entrada.
    """
    logger.info("Carregando planilha: %s", PLANILHA)

    tabela = pd.read_excel(PLANILHA)

    if COLUNA_CHAMADO not in tabela.columns:
        raise ValueError(
            f"A planilha precisa possuir a coluna "
            f"'{COLUNA_CHAMADO}'."
        )

    if COLUNA_STATUS not in tabela.columns:
        tabela[COLUNA_STATUS] = ""

    return tabela


# ============================================================
# PERSISTÊNCIA
# ============================================================

def salvar_progresso(tabela: pd.DataFrame):
    """
    Salva o estado atual da planilha.
    """
    tabela.to_excel(PLANILHA, index=False)


# ============================================================
# TEAMS
# ============================================================

def abrir_teams():
    """
    Abre o Microsoft Teams através do menu Iniciar.
    """
    logger.info("Abrindo Microsoft Teams.")

    py.press("win")
    py.write("teams")
    py.press("enter")

    time.sleep(3)


def selecionar_conta():
    """
    Seleciona a conta previamente configurada no Teams.

    As coordenadas são específicas do ambiente onde a automação
    foi configurada.
    """
    logger.info("Selecionando conta do Teams.")

    py.click(*COORDENADA_SELECAO_CONTA)
    py.click(*COORDENADA_CONTA)


def acessar_aprovacoes():
    """
    Navega até a tela de aprovações e itens enviados.
    """
    logger.info("Acessando tela de aprovações.")

    clicar_imagem(IMG_APROVACOES)
    clicar_imagem(IMG_ENVIADOS)


# ============================================================
# BUSCA DE CHAMADOS
# ============================================================

def preparar_filtro():
    """
    Aguarda o botão de filtro ficar disponível.
    """
    while not imagem_visivel(
        IMG_FILTRAR,
        tempo_limite=TEMPO_VERIFICACAO_FILTRO,
    ):
        logger.info(
            "Botão de filtro ainda não disponível. "
            "Resetando foco da tela."
        )

        py.press("esc")
        time.sleep(1)

    posicao = localizar_imagem(IMG_FILTRAR)

    if posicao is None:
        raise RuntimeError(
            "O botão de filtro não foi localizado."
        )

    py.click(py.center(posicao))


def pesquisar_chamado(numero_chamado, primeira_iteracao: bool):
    """
    Preenche o filtro com o número do chamado.
    """
    preparar_filtro()

    if not primeira_iteracao:
        py.press("tab")

    py.hotkey("ctrl", "a")
    py.press("backspace")

    escrever_texto(numero_chamado)
    py.press("enter")

    time.sleep(1)
    py.press("esc")
    time.sleep(2)

    py.press("tab")
    py.click(*COORDENADA_ACAO_LISTA)


# ============================================================
# PROCESSAMENTO
# ============================================================

def chamado_nao_encontrado(numero_chamado) -> bool:
    """
    Verifica se o chamado não foi localizado.
    """
    if imagem_visivel(
        IMG_NAO_ENCONTRADO,
        tempo_limite=TEMPO_VERIFICACAO_CHAMADO,
    ):
        logger.warning(
            "Chamado %s não encontrado.",
            numero_chamado,
        )
        return True

    return False


def cancelar_solicitacoes():
    """
    Localiza e cancela todas as solicitações com status
    'Solicitado' encontradas para o chamado atual.

    Retorna True caso pelo menos uma solicitação tenha sido
    cancelada.
    """
    cancelou_algum = False

    while True:
        item_solicitado = localizar_imagem(IMG_STATUS_SOLICITADO)

        if item_solicitado is None:
            break

        logger.info("Solicitação 'Solicitado' encontrada.")

        py.click(py.center(item_solicitado))

        clicar_imagem(IMG_CANCELAR)

        aguarda_imagem(IMG_STATUS_CANCELADO)

        py.press("esc")
        time.sleep(2)

        cancelou_algum = True

    return cancelou_algum


def processar_chamado(
    tabela: pd.DataFrame,
    linha,
    primeira_iteracao: bool,
):
    """
    Processa um único chamado e atualiza seu status na tabela.
    """
    numero_chamado = tabela.loc[linha, COLUNA_CHAMADO]

    logger.info(
        "Processando chamado %s.",
        numero_chamado,
    )

    py.press("esc")
    time.sleep(0.5)

    pesquisar_chamado(
        numero_chamado,
        primeira_iteracao=primeira_iteracao,
    )

    if chamado_nao_encontrado(numero_chamado):
        tabela.loc[linha, COLUNA_STATUS] = "Não encontrado"
        salvar_progresso(tabela)
        return

    cancelou_algum = cancelar_solicitacoes()

    if cancelou_algum:
        status = "Cancelado"

        logger.info(
            "Chamado %s cancelado com sucesso.",
            numero_chamado,
        )
    else:
        status = "Já cancelado"

        logger.info(
            "Chamado %s já estava cancelado.",
            numero_chamado,
        )

    tabela.loc[linha, COLUNA_STATUS] = status

    salvar_progresso(tabela)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    """
    Executa o fluxo completo da automação.
    """
    logger.info("Iniciando automação.")

    validar_arquivos()

    tabela = carregar_planilha()

    py.PAUSE = TEMPO_ESPERA_PADRAO

    abrir_teams()
    selecionar_conta()
    acessar_aprovacoes()

    for indice, linha in enumerate(tabela.index):

        processar_chamado(
            tabela=tabela,
            linha=linha,
            primeira_iteracao=(indice == 0),
        )

    logger.info(
        "Processamento finalizado. "
        "Planilha atualizada com sucesso."
    )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        logger.warning(
            "Execução interrompida pelo usuário."
        )

    except Exception:
        logger.exception(
            "Erro inesperado durante a execução."
        )

        raise