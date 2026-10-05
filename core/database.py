"""Infraestrutura de persistência do Aurora TMS.

A implementação histórica do domínio permanece em legacy enquanto o
projeto evolui para módulos separados. Esta camada centraliza a importação
do mesmo engine, SessionLocal e Base usados pelo restante da aplicação.
"""

from legacy.aurora_tms_mvp import Base, SessionLocal, engine

__all__ = ["Base", "SessionLocal", "engine"]
