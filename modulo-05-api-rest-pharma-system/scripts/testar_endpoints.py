"""
testar_endpoints.py
-------------------
Smoke test cobrindo TODOS os endpoints da API PharmaSystem.

Usa o test_client do Flask — nao precisa que o servidor esteja rodando.
Cria uma copia do banco em /tmp antes de rodar (para nao contaminar o db real).

Uso:
    python scripts/testar_endpoints.py

Saida:
    - Uma linha por endpoint testado (VERDE se passou, VERMELHO se falhou)
    - Resumo final com contagem
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT))

from app import create_app
from app.config import Config


# ANSI
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
RESET = "\033[0m"
NEGRITO = "\033[1m"


def status_indicador(ok: bool) -> str:
    return f"{VERDE}[OK]{RESET}" if ok else f"{VERMELHO}[FAIL]{RESET}"


class Testador:
    def __init__(self, client):
        self.client = client
        self.total = 0
        self.ok = 0
        self.falhas = []

    def check(self, descricao: str, metodo: str, url: str,
              status_esperado, json_body=None, valida_resposta=None):
        """Executa um teste. Retorna o response para uso posterior."""
        self.total += 1

        fn = getattr(self.client, metodo.lower())
        kwargs = {}
        if json_body is not None:
            kwargs["json"] = json_body
        resp = fn(url, **kwargs)

        # status pode ser int ou lista
        if isinstance(status_esperado, int):
            ok = resp.status_code == status_esperado
        else:
            ok = resp.status_code in status_esperado

        # Validacao adicional
        if ok and valida_resposta is not None:
            try:
                data = resp.get_json()
                erro_valida = valida_resposta(data)
                if erro_valida:
                    ok = False
                    descricao += f"  ({erro_valida})"
            except Exception as e:
                ok = False
                descricao += f"  (erro no parser: {e})"

        cor_metodo = CIANO
        print(f"  {status_indicador(ok)} {cor_metodo}{metodo:6}{RESET} "
              f"{url:60}  {resp.status_code}  {descricao}")

        if ok:
            self.ok += 1
        else:
            self.falhas.append((descricao, metodo, url, resp.status_code, status_esperado))

        return resp

    def resumo(self):
        print()
        print("=" * 90)
        cor = VERDE if self.ok == self.total else VERMELHO
        print(f"  {cor}{NEGRITO}RESULTADO: {self.ok}/{self.total} testes passaram{RESET}")
        print("=" * 90)

        if self.falhas:
            print(f"\n{VERMELHO}Falhas:{RESET}")
            for desc, metodo, url, real, esperado in self.falhas:
                print(f"  - {metodo} {url}: {real} != {esperado}  ({desc})")

        return self.ok == self.total


def preparar_banco_teste():
    """Copia o banco de producao para /tmp para nao contaminar."""
    origem = ROOT / "db" / "pharma.db"
    if not origem.exists():
        print(f"{VERMELHO}Banco nao encontrado: {origem}{RESET}")
        print(f"Rode primeiro: python scripts/inicializar_banco.py")
        sys.exit(1)

    destino = Path(tempfile.gettempdir()) / "pharma_test.db"
    shutil.copy(origem, destino)
    return str(destino)


def main():
    print(f"\n{NEGRITO}{'=' * 90}{RESET}")
    print(f"{NEGRITO}  SMOKE TEST — PharmaSystem API{RESET}")
    print(f"{NEGRITO}{'=' * 90}{RESET}\n")

    # Configurar app com banco temporario
    banco_teste = preparar_banco_teste()

    class ConfigTeste(Config):
        DATABASE = banco_teste

    app = create_app(ConfigTeste())
    client = app.test_client()

    t = Testador(client)

    # ================================================================
    # HEALTH
    # ================================================================
    print(f"{NEGRITO}{AMARELO}[Health]{RESET}")
    t.check("healthcheck simples", "GET", "/api/health", 200,
            valida_resposta=lambda d: None if d.get("status") == "ok" else "status != ok")
    t.check("health com banco", "GET", "/api/health/db", 200,
            valida_resposta=lambda d: None if d.get("filiais") == 15 else f"filiais={d.get('filiais')}")
    t.check("versao", "GET", "/api/versao", 200)

    # ================================================================
    # FILIAIS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Filiais]{RESET}")
    resp = t.check("listar filiais", "GET", "/api/filiais", 200,
                    valida_resposta=lambda d: None if d["paginacao"]["total"] == 15 else "total != 15")

    t.check("filtro por estado", "GET", "/api/filiais?estado=MG", 200,
            valida_resposta=lambda d: None if len(d["dados"]) > 0 else "sem dados")
    t.check("paginacao", "GET", "/api/filiais?pagina=1&por_pagina=5", 200,
            valida_resposta=lambda d: None if len(d["dados"]) == 5 else f"esperava 5, veio {len(d['dados'])}")
    t.check("buscar filial 1", "GET", "/api/filiais/1", 200,
            valida_resposta=lambda d: None if d.get("codigo") == "FIL001" else f"codigo={d.get('codigo')}")
    t.check("filial inexistente -> 404", "GET", "/api/filiais/999", 404)

    # CREATE
    nova = t.check("criar filial", "POST", "/api/filiais", 201, json_body={
        "codigo": "TST001",
        "nome": "Filial de Teste API",
        "cidade": "Teste",
        "estado": "MG",
    })
    id_nova = nova.get_json()["id"]

    # CONFLICT
    t.check("criar duplicada -> 409", "POST", "/api/filiais", 409, json_body={
        "codigo": "TST001", "nome": "outra", "cidade": "x", "estado": "MG"
    })

    # VALIDATION
    t.check("validacao ausente -> 400", "POST", "/api/filiais", 400,
            json_body={"nome": "faltando codigo"})
    t.check("UF invalida -> 400", "POST", "/api/filiais", 400, json_body={
        "codigo": "TST002", "nome": "x", "cidade": "y", "estado": "XX"
    })

    # UPDATE
    t.check("atualizar filial", "PUT", f"/api/filiais/{id_nova}", 200,
            json_body={"nome": "Filial de Teste API Atualizada"})

    # DELETE
    t.check("deletar filial teste", "DELETE", f"/api/filiais/{id_nova}", 204)
    t.check("filial 1 tem vendas -> 409 no delete", "DELETE", "/api/filiais/1", 409)

    # ================================================================
    # CATEGORIAS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Categorias]{RESET}")
    t.check("listar categorias", "GET", "/api/categorias", 200,
            valida_resposta=lambda d: None if d["total"] == 10 else f"total={d['total']}")
    t.check("buscar categoria 1", "GET", "/api/categorias/1", 200,
            valida_resposta=lambda d: None if "total_produtos" in d else "sem total_produtos")
    t.check("criar categoria", "POST", "/api/categorias", 201,
            json_body={"nome": "Homeopaticos-Teste"})
    t.check("duplicada -> 409", "POST", "/api/categorias", 409,
            json_body={"nome": "Homeopaticos-Teste"})

    # ================================================================
    # PRODUTOS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Produtos]{RESET}")
    t.check("listar produtos", "GET", "/api/produtos", 200,
            valida_resposta=lambda d: None if d["paginacao"]["total"] == 71 else f"total={d['paginacao']['total']}")
    t.check("filtro categoria_id=1", "GET", "/api/produtos?categoria_id=1", 200)
    t.check("filtro preco_min=100", "GET", "/api/produtos?preco_min=100", 200)
    t.check("filtro exige_receita=true", "GET", "/api/produtos?exige_receita=true", 200)
    t.check("busca por nome", "GET", "/api/produtos?nome=Dipirona", 200)
    t.check("produto por id", "GET", "/api/produtos/1", 200,
            valida_resposta=lambda d: None if "margem_lucro" in d else "sem margem_lucro")
    t.check("produto 999 -> 404", "GET", "/api/produtos/999", 404)

    novo_prod = t.check("criar produto", "POST", "/api/produtos", 201, json_body={
        "codigo_barras": "99999999999999",
        "nome": "Produto Teste",
        "categoria_id": 1,
        "preco_custo": 10.0,
        "preco_venda": 20.0,
    })
    id_prod = novo_prod.get_json()["id"]

    t.check("preco_venda < custo -> 400", "POST", "/api/produtos", 400, json_body={
        "codigo_barras": "88888888888888", "nome": "x", "categoria_id": 1,
        "preco_custo": 20.0, "preco_venda": 10.0,
    })

    t.check("atualizar produto", "PUT", f"/api/produtos/{id_prod}", 200,
            json_body={"preco_venda": 25.0})

    t.check("deletar produto teste", "DELETE", f"/api/produtos/{id_prod}", 204)

    # ================================================================
    # CLIENTES
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Clientes]{RESET}")
    t.check("listar clientes", "GET", "/api/clientes", 200,
            valida_resposta=lambda d: None if d["paginacao"]["total"] == 200 else f"total={d['paginacao']['total']}")
    t.check("cliente por id", "GET", "/api/clientes/1", 200,
            valida_resposta=lambda d: None if "n_compras" in d else "sem n_compras")

    novo_cli = t.check("criar cliente", "POST", "/api/clientes", 201, json_body={
        "nome": "Cliente Teste",
        "cpf": "111.444.777-35",  # CPF valido pelo dv
        "email": "teste@example.com",
        "estado": "MG",
    })
    id_cli = novo_cli.get_json()["id"]

    t.check("CPF invalido -> 400", "POST", "/api/clientes", 400, json_body={
        "nome": "x", "cpf": "111.111.111-11",
    })
    t.check("email invalido -> 400", "POST", "/api/clientes", 400, json_body={
        "nome": "x", "email": "isso-nao-e-email",
    })
    t.check("CPF duplicado -> 409", "POST", "/api/clientes", 409, json_body={
        "nome": "outro", "cpf": "111.444.777-35",
    })
    t.check("deletar cliente teste", "DELETE", f"/api/clientes/{id_cli}", 204)

    # ================================================================
    # VENDAS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Vendas]{RESET}")
    t.check("listar vendas", "GET", "/api/vendas?por_pagina=5", 200,
            valida_resposta=lambda d: None if len(d["dados"]) <= 5 else "mais que 5")
    t.check("vendas por filial", "GET", "/api/vendas?filial_id=1&por_pagina=5", 200)
    t.check("vendas com status CANCELADA", "GET", "/api/vendas?status=CANCELADA&por_pagina=5", 200)
    t.check("venda por id", "GET", "/api/vendas/1", 200,
            valida_resposta=lambda d: None if "itens" in d else "sem itens")

    nova_venda = t.check("criar venda com 2 itens", "POST", "/api/vendas", 201, json_body={
        "filial_id": 1,
        "cliente_id": 1,
        "forma_pagamento": "PIX",
        "itens": [
            {"produto_id": 1, "quantidade": 2},
            {"produto_id": 2, "quantidade": 1},
        ]
    })
    id_venda_nova = nova_venda.get_json()["id"]

    t.check("forma_pagamento invalida -> 400", "POST", "/api/vendas", 400, json_body={
        "filial_id": 1, "forma_pagamento": "BOLETO",
        "itens": [{"produto_id": 1, "quantidade": 1}]
    })
    t.check("produto inexistente -> 400", "POST", "/api/vendas", 400, json_body={
        "filial_id": 1, "forma_pagamento": "PIX",
        "itens": [{"produto_id": 99999, "quantidade": 1}]
    })
    t.check("sem itens -> 400", "POST", "/api/vendas", 400, json_body={
        "filial_id": 1, "forma_pagamento": "PIX", "itens": []
    })

    t.check("cancelar venda", "POST", f"/api/vendas/{id_venda_nova}/cancelar", 200)
    t.check("cancelar 2x -> 409", "POST", f"/api/vendas/{id_venda_nova}/cancelar", 409)

    # ================================================================
    # INDICADORES
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Indicadores]{RESET}")
    t.check("KPIs gerais", "GET", "/api/indicadores/kpis-gerais", 200,
            valida_resposta=lambda d: None if d.get("faturamento_total", 0) > 100000
                                      else f"faturamento={d.get('faturamento_total')}")
    t.check("faturamento mensal", "GET", "/api/indicadores/faturamento-mensal", 200,
            valida_resposta=lambda d: None if len(d["dados"]) > 0 else "sem meses")
    t.check("faturamento mensal com ano", "GET", "/api/indicadores/faturamento-mensal?ano=2026", 200)
    t.check("top produtos", "GET", "/api/indicadores/top-produtos?limite=5", 200,
            valida_resposta=lambda d: None if len(d["dados"]) == 5 else f"veio {len(d['dados'])}")
    t.check("top produtos por quantidade", "GET",
            "/api/indicadores/top-produtos?ordem=quantidade", 200)
    t.check("top filiais", "GET", "/api/indicadores/top-filiais", 200,
            valida_resposta=lambda d: None if len(d["dados"]) > 0 and d["dados"][0].get("ranking") == 1
                                      else "sem ranking")
    t.check("faturamento por categoria", "GET",
            "/api/indicadores/faturamento-por-categoria", 200)
    t.check("formas de pagamento", "GET", "/api/indicadores/formas-pagamento", 200)

    # ================================================================
    # DOCS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Docs]{RESET}")
    t.check("Swagger UI HTML", "GET", "/api/docs", 200)
    t.check("OpenAPI JSON", "GET", "/api/openapi.json", 200,
            valida_resposta=lambda d: None if d.get("openapi") == "3.0.3"
                                       else f"openapi={d.get('openapi')}")
    t.check("raiz da API", "GET", "/api/", 200)

    # ================================================================
    # ERROS
    # ================================================================
    print(f"\n{NEGRITO}{AMARELO}[Erros]{RESET}")
    t.check("rota inexistente -> 404", "GET", "/api/aleatorio", 404)
    t.check("metodo nao permitido -> 405", "PATCH", "/api/filiais/1", 405)

    # Limpar categoria de teste
    client.delete_by_nome = lambda nome: None  # noop
    # Achar id da categoria teste e deletar (cleanup)
    resp = client.get("/api/categorias")
    for cat in resp.get_json()["dados"]:
        if cat["nome"] == "Homeopaticos-Teste":
            client.delete(f"/api/categorias/{cat['id']}")
            break

    return t.resumo()


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
