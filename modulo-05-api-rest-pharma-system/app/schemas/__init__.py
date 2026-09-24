"""
Schemas de serializacao/validacao.

Cada arquivo tem duas funcoes principais:
    - `serializar_X(row)`: converte sqlite3.Row em dict JSON-friendly
    - `validar_payload_X(payload, criacao=True)`: valida dict recebido

Alternativa considerada: Marshmallow ou Pydantic. Nao usadas para manter
o modulo com zero dependencias externas alem de Flask, expondo os
fundamentos.
"""
