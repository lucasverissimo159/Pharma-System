"""
app/errors.py
-------------
Tratamento centralizado de erros HTTP.

Todos os erros retornam JSON no formato:

    {
      "erro": "nome_do_erro",
      "mensagem": "descricao humana",
      "detalhes": {...}   // opcional
    }

Isso garante que qualquer cliente da API (JS, Postman, etc) receba
sempre uma estrutura previsivel para tratar erros.
"""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


class ErroAPI(Exception):
    """Excecao base para erros previsiveis da API.

    Uso:
        raise ErroAPI("cpf ja cadastrado", 409, {"cpf": cpf})
    """
    def __init__(self, mensagem: str, status: int = 400, detalhes: dict = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status
        self.detalhes = detalhes or {}


class NaoEncontradoError(ErroAPI):
    """Recurso nao encontrado — 404."""
    def __init__(self, recurso: str, id_recurso=None):
        msg = f"{recurso} nao encontrado"
        det = {"recurso": recurso}
        if id_recurso is not None:
            msg += f" (id={id_recurso})"
            det["id"] = id_recurso
        super().__init__(msg, 404, det)


class ValidacaoError(ErroAPI):
    """Payload invalido — 400."""
    def __init__(self, campos_com_erro: dict):
        super().__init__(
            "Dados invalidos", 400,
            {"campos": campos_com_erro}
        )


class ConflitoError(ErroAPI):
    """Conflito de dados (ex: chave unica) — 409."""
    def __init__(self, mensagem: str, detalhes: dict = None):
        super().__init__(mensagem, 409, detalhes)


def _formatar_erro(mensagem: str, status: int, detalhes: dict = None):
    """Formata resposta JSON de erro."""
    corpo = {
        "erro": _nome_erro_por_status(status),
        "mensagem": mensagem,
        "status": status,
    }
    if detalhes:
        corpo["detalhes"] = detalhes
    return jsonify(corpo), status


def _nome_erro_por_status(status: int) -> str:
    mapa = {
        400: "requisicao_invalida",
        401: "nao_autorizado",
        403: "proibido",
        404: "nao_encontrado",
        405: "metodo_nao_permitido",
        409: "conflito",
        415: "midia_nao_suportada",
        422: "entidade_nao_processavel",
        500: "erro_interno",
    }
    return mapa.get(status, "erro")


def registrar_handlers_erro(app: Flask):
    """Registra os handlers globais na app Flask."""

    @app.errorhandler(ErroAPI)
    def erro_api(exc: ErroAPI):
        return _formatar_erro(exc.mensagem, exc.status, exc.detalhes)

    @app.errorhandler(HTTPException)
    def erro_http_generico(exc: HTTPException):
        return _formatar_erro(exc.description, exc.code)

    @app.errorhandler(404)
    def nao_encontrado(exc):
        return _formatar_erro("Rota nao encontrada", 404)

    @app.errorhandler(405)
    def metodo_nao_permitido(exc):
        return _formatar_erro("Metodo HTTP nao permitido nesta rota", 405)

    @app.errorhandler(500)
    def erro_interno(exc):
        # Log seria feito aqui em prod
        return _formatar_erro("Erro interno do servidor", 500)

    @app.errorhandler(Exception)
    def excecao_nao_tratada(exc: Exception):
        """Ultimo recurso: pega qualquer excecao nao prevista."""
        if isinstance(exc, HTTPException):
            return erro_http_generico(exc)
        # Em producao, logar aqui com traceback completo
        return _formatar_erro(
            f"Erro interno: {type(exc).__name__}", 500
        )
