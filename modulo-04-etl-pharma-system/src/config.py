"""
config.py
---------
Carrega e valida as configuracoes do pipeline a partir dos YAMLs.

Uso:
    from src.config import Config
    cfg = Config.carregar()
    print(cfg.paths["dados_brutos"])
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml


ROOT = Path(__file__).parent.parent.resolve()


def _expandir_variaveis(valor: Any) -> Any:
    """Substitui ${VAR} pelo valor da variavel de ambiente."""
    if isinstance(valor, str) and valor.startswith("${") and valor.endswith("}"):
        var = valor[2:-1]
        return os.environ.get(var, "")
    if isinstance(valor, dict):
        return {k: _expandir_variaveis(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [_expandir_variaveis(item) for item in valor]
    return valor


@dataclass
class Config:
    """Configuracao completa do pipeline."""
    paths: Dict[str, str] = field(default_factory=dict)
    banco: Dict[str, Any] = field(default_factory=dict)
    pipeline: Dict[str, Any] = field(default_factory=dict)
    regras: Dict[str, Any] = field(default_factory=dict)
    logging: Dict[str, Any] = field(default_factory=dict)
    schema: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def carregar(cls, arquivo_config: str = None, arquivo_schema: str = None) -> "Config":
        """Carrega config.yaml e schema.yaml, expandindo variaveis de ambiente."""
        if arquivo_config is None:
            arquivo_config = str(ROOT / "config" / "config.yaml")
        if arquivo_schema is None:
            arquivo_schema = str(ROOT / "config" / "schema.yaml")

        with open(arquivo_config, "r", encoding="utf-8") as f:
            cfg_dict = yaml.safe_load(f)
        cfg_dict = _expandir_variaveis(cfg_dict)

        with open(arquivo_schema, "r", encoding="utf-8") as f:
            schema_dict = yaml.safe_load(f)

        return cls(
            paths=cfg_dict.get("paths", {}),
            banco=cfg_dict.get("banco", {}),
            pipeline=cfg_dict.get("pipeline", {}),
            regras=cfg_dict.get("regras", {}),
            logging=cfg_dict.get("logging", {}),
            schema=schema_dict,
        )

    def path(self, nome: str) -> Path:
        """Retorna Path absoluto para um dos diretorios configurados."""
        rel = self.paths.get(nome, nome)
        p = Path(rel)
        if not p.is_absolute():
            p = ROOT / p
        return p

    def string_conexao_banco(self) -> str:
        """Retorna string de conexao ou caminho conforme o backend."""
        backend = self.banco.get("backend", "sqlite")
        if backend == "sqlite":
            cam = self.banco["sqlite"]["caminho"]
            p = Path(cam)
            if not p.is_absolute():
                p = ROOT / p
            return f"sqlite:///{p}"
        elif backend == "postgres":
            pg = self.banco["postgres"]
            return (f"postgresql://{pg['user']}:{pg['password']}"
                    f"@{pg['host']}:{pg['port']}/{pg['database']}")
        else:
            raise ValueError(f"Backend nao suportado: {backend}")

    def caminho_sqlite(self) -> Path:
        """Retorna Path do arquivo SQLite (apenas se backend=sqlite)."""
        if self.banco.get("backend") != "sqlite":
            raise ValueError("Backend nao e sqlite")
        cam = self.banco["sqlite"]["caminho"]
        p = Path(cam)
        if not p.is_absolute():
            p = ROOT / p
        return p


if __name__ == "__main__":
    # Modo diagnostico
    cfg = Config.carregar()
    print(f"Backend: {cfg.banco.get('backend')}")
    print(f"String conexao: {cfg.string_conexao_banco()}")
    print(f"Dados brutos: {cfg.path('dados_brutos')}")
    print(f"Schema tem {len(cfg.schema['vendas_filial']['obrigatorias'])} colunas obrigatorias")
