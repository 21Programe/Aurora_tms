from __future__ import annotations

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict
from contextlib import contextmanager
import os

# ============================================================
# AURORA TMS - TRANSPORT MANAGEMENT SYSTEM
# MVP Local completo em um único arquivo Python
# Banco local SQLite + SQLAlchemy + Menu interativo
# ============================================================
# Objetivo:
# - Gerenciar caminhões
# - Gerenciar motoristas
# - Gerenciar cargas
# - Criar viagens
# - Embarcar cargas em veículos
# - Controlar custos operacionais
# - Emitir relatórios
# - Registrar eventos de auditoria
#
# Como rodar:
#   pip install sqlalchemy
#   python aurora_tms_mvp.py
# ============================================================


# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./aurora_tms.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================
# FUNÇÕES UTILITÁRIAS GERAIS
# ============================================================
def agora() -> datetime:
    return datetime.now()


def fmt_dt(valor: Optional[datetime]) -> str:
    if not valor:
        return "-"
    return valor.strftime("%d/%m/%Y %H:%M")


def fmt_data_iso(valor: Optional[datetime]) -> str:
    if not valor:
        return "-"
    return valor.strftime("%Y-%m-%d %H:%M:%S")


def linha(tamanho: int = 72) -> str:
    return "=" * tamanho


def titulo(texto: str) -> None:
    print("\n" + linha())
    print(texto)
    print(linha())


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pedir_texto(msg: str, obrigatorio: bool = True) -> str:
    while True:
        valor = input(msg).strip()
        if valor or not obrigatorio:
            return valor
        print("[ERRO] Campo obrigatório.")


def pedir_int(msg: str, minimo: Optional[int] = None) -> int:
    while True:
        try:
            valor = int(input(msg).strip())
            if minimo is not None and valor < minimo:
                print(f"[ERRO] O valor mínimo é {minimo}.")
                continue
            return valor
        except ValueError:
            print("[ERRO] Digite um número inteiro válido.")


def pedir_float(msg: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            bruto = input(msg).strip().replace(",", ".")
            valor = float(bruto)
            if minimo is not None and valor < minimo:
                print(f"[ERRO] O valor mínimo é {minimo}.")
                continue
            return valor
        except ValueError:
            print("[ERRO] Digite um número válido.")


def pedir_data(msg: str, obrigatorio: bool = False) -> Optional[datetime]:
    while True:
        bruto = input(msg).strip()
        if not bruto and not obrigatorio:
            return None
        try:
            return datetime.strptime(bruto, "%Y-%m-%d %H:%M")
        except ValueError:
            print("[ERRO] Use o formato YYYY-MM-DD HH:MM")


# ============================================================
# ENUMS SIMPLES EM TEXTO (MVP)
# ============================================================
STATUS_CAMINHAO_DISPONIVEL = "Disponível"
STATUS_CAMINHAO_EM_ROTA = "Em Rota"
STATUS_CAMINHAO_MANUTENCAO = "Manutenção"

STATUS_MOTORISTA_DISPONIVEL = "Disponível"
STATUS_MOTORISTA_EM_VIAGEM = "Em Viagem"
STATUS_MOTORISTA_AFASTADO = "Afastado"

STATUS_CARGA_PATIO = "Pátio"
STATUS_CARGA_RESERVADA = "Reservada"
STATUS_CARGA_EMBARCADA = "Embarcada"
STATUS_CARGA_ENTREGUE = "Entregue"
STATUS_CARGA_CANCELADA = "Cancelada"

STATUS_VIAGEM_PLANEJADA = "Planejada"
STATUS_VIAGEM_EM_ANDAMENTO = "Em Andamento"
STATUS_VIAGEM_FINALIZADA = "Finalizada"
STATUS_VIAGEM_CANCELADA = "Cancelada"

TIPO_EVENTO_CADASTRO = "Cadastro"
TIPO_EVENTO_ATUALIZACAO = "Atualização"
TIPO_EVENTO_OPERACAO = "Operação"
TIPO_EVENTO_RELATORIO = "Relatório"
TIPO_EVENTO_ALERTA = "Alerta"


# ============================================================
# MODELOS / TABELAS
# ============================================================
class Caminhao(Base):
    __tablename__ = "caminhoes"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(String, nullable=False)
    capacidade_max_kg = Column(Float, nullable=False)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=True)
    ano = Column(Integer, nullable=True)
    status = Column(String, default=STATUS_CAMINHAO_DISPONIVEL, nullable=False)
    criado_em = Column(DateTime, default=agora, nullable=False)
    atualizado_em = Column(DateTime, default=agora, onupdate=agora, nullable=False)

    cargas = relationship("Carga", back_populates="veiculo")
    viagens = relationship("Viagem", back_populates="caminhao")

    def __repr__(self) -> str:
        return f"<Caminhao id={self.id} placa={self.placa} status={self.status}>"


class Motorista(Base):
    __tablename__ = "motoristas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    cnh = Column(String, unique=True, nullable=False)
    categoria_cnh = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    status = Column(String, default=STATUS_MOTORISTA_DISPONIVEL, nullable=False)
    criado_em = Column(DateTime, default=agora, nullable=False)
    atualizado_em = Column(DateTime, default=agora, onupdate=agora, nullable=False)

    viagens = relationship("Viagem", back_populates="motorista")

    def __repr__(self) -> str:
        return f"<Motorista id={self.id} nome={self.nome} status={self.status}>"


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    documento = Column(String, unique=True, index=True, nullable=False)
    cidade = Column(String, nullable=True)
    contato = Column(String, nullable=True)
    email = Column(String, nullable=True)
    criado_em = Column(DateTime, default=agora, nullable=False)

    cargas = relationship("Carga", back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nome={self.nome}>"


class Carga(Base):
    __tablename__ = "cargas"

    id = Column(Integer, primary_key=True, index=True)
    nota_fiscal = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    peso_kg = Column(Float, nullable=False)
    valor_mercadoria = Column(Float, default=0.0, nullable=False)
    cidade_origem = Column(String, nullable=False)
    cidade_destino = Column(String, nullable=False)
    prazo_entrega = Column(DateTime, nullable=True)
    status = Column(String, default=STATUS_CARGA_PATIO, nullable=False)
    observacoes = Column(Text, nullable=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    caminhao_id = Column(Integer, ForeignKey("caminhoes.id"), nullable=True)
    viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=True)

    criado_em = Column(DateTime, default=agora, nullable=False)
    atualizado_em = Column(DateTime, default=agora, onupdate=agora, nullable=False)

    cliente = relationship("Cliente", back_populates="cargas")
    veiculo = relationship("Caminhao", back_populates="cargas")
    viagem = relationship("Viagem", back_populates="cargas")

    def __repr__(self) -> str:
        return f"<Carga id={self.id} nota={self.nota_fiscal} status={self.status}>"


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    origem = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    distancia_km = Column(Float, default=0.0, nullable=False)
    status = Column(String, default=STATUS_VIAGEM_PLANEJADA, nullable=False)
    data_saida_prevista = Column(DateTime, nullable=True)
    data_saida_real = Column(DateTime, nullable=True)
    data_chegada_prevista = Column(DateTime, nullable=True)
    data_chegada_real = Column(DateTime, nullable=True)
    observacoes = Column(Text, nullable=True)

    caminhao_id = Column(Integer, ForeignKey("caminhoes.id"), nullable=False)
    motorista_id = Column(Integer, ForeignKey("motoristas.id"), nullable=False)

    criado_em = Column(DateTime, default=agora, nullable=False)
    atualizado_em = Column(DateTime, default=agora, onupdate=agora, nullable=False)

    caminhao = relationship("Caminhao", back_populates="viagens")
    motorista = relationship("Motorista", back_populates="viagens")
    cargas = relationship("Carga", back_populates="viagem")
    custos = relationship("CustoViagem", back_populates="viagem")

    def __repr__(self) -> str:
        return f"<Viagem id={self.id} codigo={self.codigo} status={self.status}>"


class CustoViagem(Base):
    __tablename__ = "custos_viagem"

    id = Column(Integer, primary_key=True, index=True)
    viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=False)
    tipo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    criado_em = Column(DateTime, default=agora, nullable=False)

    viagem = relationship("Viagem", back_populates="custos")

    def __repr__(self) -> str:
        return f"<CustoViagem id={self.id} tipo={self.tipo} valor={self.valor}>"


class EventoAuditoria(Base):
    __tablename__ = "eventos_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    entidade = Column(String, nullable=False)
    entidade_id = Column(Integer, nullable=True)
    mensagem = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=agora, nullable=False)

    def __repr__(self) -> str:
        return f"<EventoAuditoria id={self.id} tipo={self.tipo} entidade={self.entidade}>"


# ============================================================
# CONTEXTO DE SESSÃO / UNIT OF WORK SIMPLES
# ============================================================
@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================================
# AUDITORIA
# ============================================================
def registrar_evento(
    db: Session,
    tipo: str,
    entidade: str,
    mensagem: str,
    entidade_id: Optional[int] = None,
) -> EventoAuditoria:
    evento = EventoAuditoria(
        tipo=tipo,
        entidade=entidade,
        entidade_id=entidade_id,
        mensagem=mensagem,
    )
    db.add(evento)
    db.flush()
    return evento


# ============================================================
# SERVIÇOS DE NEGÓCIO - CAMINHÃO
# ============================================================
class CaminhaoService:
    @staticmethod
    def criar(
        db: Session,
        placa: str,
        tipo: str,
        capacidade_max_kg: float,
        marca: str = "",
        modelo: str = "",
        ano: Optional[int] = None,
    ) -> Caminhao:
        placa = placa.upper().strip()
        existente = db.query(Caminhao).filter(Caminhao.placa == placa).first()
        if existente:
            raise ValueError("Já existe um caminhão com esta placa.")

        if capacidade_max_kg <= 0:
            raise ValueError("A capacidade máxima deve ser maior que zero.")

        caminhao = Caminhao(
            placa=placa,
            tipo=tipo.strip(),
            capacidade_max_kg=capacidade_max_kg,
            marca=marca.strip() or None,
            modelo=modelo.strip() or None,
            ano=ano,
            status=STATUS_CAMINHAO_DISPONIVEL,
        )
        db.add(caminhao)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Caminhao",
            f"Caminhão {placa} cadastrado com sucesso.",
            caminhao.id,
        )
        return caminhao

    @staticmethod
    def listar(db: Session) -> List[Caminhao]:
        return db.query(Caminhao).order_by(Caminhao.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, caminhao_id: int) -> Caminhao:
        obj = db.query(Caminhao).filter(Caminhao.id == caminhao_id).first()
        if not obj:
            raise ValueError("Caminhão não encontrado.")
        return obj

    @staticmethod
    def atualizar_status(db: Session, caminhao_id: int, novo_status: str) -> Caminhao:
        caminhao = CaminhaoService.buscar_por_id(db, caminhao_id)
        caminhao.status = novo_status
        caminhao.atualizado_em = agora()
        db.flush()
        registrar_evento(
            db,
            TIPO_EVENTO_ATUALIZACAO,
            "Caminhao",
            f"Status do caminhão {caminhao.placa} alterado para {novo_status}.",
            caminhao.id,
        )
        return caminhao


# ============================================================
# SERVIÇOS DE NEGÓCIO - MOTORISTA
# ============================================================
class MotoristaService:
    @staticmethod
    def criar(
        db: Session,
        nome: str,
        cpf: str,
        cnh: str,
        categoria_cnh: str,
        telefone: str = "",
    ) -> Motorista:
        cpf = cpf.strip()
        cnh = cnh.strip().upper()

        if db.query(Motorista).filter(Motorista.cpf == cpf).first():
            raise ValueError("Já existe um motorista com este CPF.")

        if db.query(Motorista).filter(Motorista.cnh == cnh).first():
            raise ValueError("Já existe um motorista com esta CNH.")

        motorista = Motorista(
            nome=nome.strip(),
            cpf=cpf,
            cnh=cnh,
            categoria_cnh=categoria_cnh.strip().upper(),
            telefone=telefone.strip() or None,
            status=STATUS_MOTORISTA_DISPONIVEL,
        )
        db.add(motorista)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Motorista",
            f"Motorista {motorista.nome} cadastrado com sucesso.",
            motorista.id,
        )
        return motorista

    @staticmethod
    def listar(db: Session) -> List[Motorista]:
        return db.query(Motorista).order_by(Motorista.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, motorista_id: int) -> Motorista:
        obj = db.query(Motorista).filter(Motorista.id == motorista_id).first()
        if not obj:
            raise ValueError("Motorista não encontrado.")
        return obj

    @staticmethod
    def atualizar_status(db: Session, motorista_id: int, novo_status: str) -> Motorista:
        motorista = MotoristaService.buscar_por_id(db, motorista_id)
        motorista.status = novo_status
        motorista.atualizado_em = agora()
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_ATUALIZACAO,
            "Motorista",
            f"Status do motorista {motorista.nome} alterado para {novo_status}.",
            motorista.id,
        )
        return motorista


# ============================================================
# SERVIÇOS DE NEGÓCIO - CLIENTE
# ============================================================
class ClienteService:
    @staticmethod
    def criar(
        db: Session,
        nome: str,
        documento: str,
        cidade: str = "",
        contato: str = "",
        email: str = "",
    ) -> Cliente:
        documento = documento.strip()
        if db.query(Cliente).filter(Cliente.documento == documento).first():
            raise ValueError("Já existe um cliente com este documento.")

        cliente = Cliente(
            nome=nome.strip(),
            documento=documento,
            cidade=cidade.strip() or None,
            contato=contato.strip() or None,
            email=email.strip() or None,
        )
        db.add(cliente)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Cliente",
            f"Cliente {cliente.nome} cadastrado com sucesso.",
            cliente.id,
        )
        return cliente

    @staticmethod
    def listar(db: Session) -> List[Cliente]:
        return db.query(Cliente).order_by(Cliente.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, cliente_id: int) -> Cliente:
        obj = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not obj:
            raise ValueError("Cliente não encontrado.")
        return obj


# ============================================================
# SERVIÇOS DE NEGÓCIO - CARGA
# ============================================================
class CargaService:
    @staticmethod
    def criar(
        db: Session,
        nota_fiscal: str,
        descricao: str,
        peso_kg: float,
        valor_mercadoria: float,
        cidade_origem: str,
        cidade_destino: str,
        prazo_entrega: Optional[datetime] = None,
        cliente_id: Optional[int] = None,
        observacoes: str = "",
    ) -> Carga:
        nota_fiscal = nota_fiscal.strip().upper()

        if db.query(Carga).filter(Carga.nota_fiscal == nota_fiscal).first():
            raise ValueError("Já existe uma carga com esta nota fiscal.")

        if peso_kg <= 0:
            raise ValueError("O peso da carga deve ser maior que zero.")

        cliente = None
        if cliente_id is not None:
            cliente = ClienteService.buscar_por_id(db, cliente_id)

        carga = Carga(
            nota_fiscal=nota_fiscal,
            descricao=descricao.strip(),
            peso_kg=peso_kg,
            valor_mercadoria=valor_mercadoria,
            cidade_origem=cidade_origem.strip(),
            cidade_destino=cidade_destino.strip(),
            prazo_entrega=prazo_entrega,
            status=STATUS_CARGA_PATIO,
            cliente=cliente,
            observacoes=observacoes.strip() or None,
        )
        db.add(carga)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Carga",
            f"Carga NF {nota_fiscal} cadastrada com sucesso.",
            carga.id,
        )
        return carga

    @staticmethod
    def listar(db: Session) -> List[Carga]:
        return db.query(Carga).order_by(Carga.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, carga_id: int) -> Carga:
        obj = db.query(Carga).filter(Carga.id == carga_id).first()
        if not obj:
            raise ValueError("Carga não encontrada.")
        return obj

    @staticmethod
    def peso_total_por_caminhao(db: Session, caminhao_id: int) -> float:
        cargas_ativas = (
            db.query(Carga)
            .filter(Carga.caminhao_id == caminhao_id)
            .filter(Carga.status.in_([STATUS_CARGA_RESERVADA, STATUS_CARGA_EMBARCADA]))
            .all()
        )
        return sum(c.peso_kg for c in cargas_ativas)

    @staticmethod
    def reservar_para_viagem(db: Session, carga_id: int, viagem_id: int) -> Carga:
        carga = CargaService.buscar_por_id(db, carga_id)
        viagem = ViagemService.buscar_por_id(db, viagem_id)

        if carga.status not in [STATUS_CARGA_PATIO, STATUS_CARGA_RESERVADA]:
            raise ValueError("A carga não pode ser reservada para esta viagem.")

        peso_atual = CargaService.peso_total_por_caminhao(db, viagem.caminhao_id)
        caminhao = viagem.caminhao
        peso_resultante = peso_atual + carga.peso_kg

        # Se a carga já estava reservada no mesmo caminhão/viagem, evita dupla soma lógica.
        if carga.caminhao_id == caminhao.id and carga.viagem_id == viagem.id:
            peso_resultante = peso_atual

        if peso_resultante > caminhao.capacidade_max_kg:
            excedente = peso_resultante - caminhao.capacidade_max_kg
            registrar_evento(
                db,
                TIPO_EVENTO_ALERTA,
                "Carga",
                (
                    f"Tentativa de exceder capacidade do caminhão {caminhao.placa}. "
                    f"Excedente: {excedente:.2f} kg."
                ),
                carga.id,
            )
            raise ValueError(
                f"Operação negada. A capacidade do caminhão seria excedida em {excedente:.2f} kg."
            )

        carga.caminhao_id = caminhao.id
        carga.viagem_id = viagem.id
        carga.status = STATUS_CARGA_RESERVADA
        carga.atualizado_em = agora()
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Carga",
            f"Carga NF {carga.nota_fiscal} reservada para a viagem {viagem.codigo}.",
            carga.id,
        )
        return carga

    @staticmethod
    def embarcar_carga(db: Session, carga_id: int) -> Carga:
        carga = CargaService.buscar_por_id(db, carga_id)
        if not carga.viagem_id or not carga.caminhao_id:
            raise ValueError("A carga precisa estar vinculada a uma viagem antes do embarque.")

        if carga.status not in [STATUS_CARGA_RESERVADA, STATUS_CARGA_PATIO]:
            raise ValueError("Esta carga não está apta para embarque.")

        carga.status = STATUS_CARGA_EMBARCADA
        carga.atualizado_em = agora()
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Carga",
            f"Carga NF {carga.nota_fiscal} embarcada com sucesso.",
            carga.id,
        )
        return carga

    @staticmethod
    def entregar_carga(db: Session, carga_id: int) -> Carga:
        carga = CargaService.buscar_por_id(db, carga_id)
        if carga.status != STATUS_CARGA_EMBARCADA:
            raise ValueError("Apenas cargas embarcadas podem ser marcadas como entregues.")

        carga.status = STATUS_CARGA_ENTREGUE
        carga.atualizado_em = agora()
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Carga",
            f"Carga NF {carga.nota_fiscal} entregue com sucesso.",
            carga.id,
        )
        return carga


# ============================================================
# SERVIÇOS DE NEGÓCIO - VIAGEM
# ============================================================
class ViagemService:
    @staticmethod
    def gerar_codigo(db: Session) -> str:
        ultimo = db.query(Viagem).order_by(Viagem.id.desc()).first()
        proximo_numero = 1 if not ultimo else ultimo.id + 1
        return f"VG-{datetime.now().strftime('%Y%m')}-{proximo_numero:05d}"

    @staticmethod
    def criar(
        db: Session,
        origem: str,
        destino: str,
        distancia_km: float,
        caminhao_id: int,
        motorista_id: int,
        data_saida_prevista: Optional[datetime] = None,
        data_chegada_prevista: Optional[datetime] = None,
        observacoes: str = "",
    ) -> Viagem:
        caminhao = CaminhaoService.buscar_por_id(db, caminhao_id)
        motorista = MotoristaService.buscar_por_id(db, motorista_id)

        if caminhao.status != STATUS_CAMINHAO_DISPONIVEL:
            raise ValueError("O caminhão selecionado não está disponível.")

        if motorista.status != STATUS_MOTORISTA_DISPONIVEL:
            raise ValueError("O motorista selecionado não está disponível.")

        codigo = ViagemService.gerar_codigo(db)

        viagem = Viagem(
            codigo=codigo,
            origem=origem.strip(),
            destino=destino.strip(),
            distancia_km=distancia_km,
            status=STATUS_VIAGEM_PLANEJADA,
            data_saida_prevista=data_saida_prevista,
            data_chegada_prevista=data_chegada_prevista,
            observacoes=observacoes.strip() or None,
            caminhao=caminhao,
            motorista=motorista,
        )
        db.add(viagem)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Viagem",
            f"Viagem {codigo} criada com sucesso.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def listar(db: Session) -> List[Viagem]:
        return db.query(Viagem).order_by(Viagem.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, viagem_id: int) -> Viagem:
        obj = db.query(Viagem).filter(Viagem.id == viagem_id).first()
        if not obj:
            raise ValueError("Viagem não encontrada.")
        return obj

    @staticmethod
    def iniciar(db: Session, viagem_id: int) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)

        if viagem.status != STATUS_VIAGEM_PLANEJADA:
            raise ValueError("Somente viagens planejadas podem ser iniciadas.")

        if viagem.caminhao.status != STATUS_CAMINHAO_DISPONIVEL:
            raise ValueError("O caminhão desta viagem não está disponível para início.")

        if viagem.motorista.status != STATUS_MOTORISTA_DISPONIVEL:
            raise ValueError("O motorista desta viagem não está disponível para início.")

        viagem.status = STATUS_VIAGEM_EM_ANDAMENTO
        viagem.data_saida_real = agora()
        viagem.caminhao.status = STATUS_CAMINHAO_EM_ROTA
        viagem.motorista.status = STATUS_MOTORISTA_EM_VIAGEM
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} iniciada.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def finalizar(db: Session, viagem_id: int) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)

        if viagem.status not in [STATUS_VIAGEM_PLANEJADA, STATUS_VIAGEM_EM_ANDAMENTO]:
            raise ValueError("A viagem não pode ser finalizada no estado atual.")

        for carga in viagem.cargas:
            if carga.status == STATUS_CARGA_EMBARCADA:
                carga.status = STATUS_CARGA_ENTREGUE
                carga.atualizado_em = agora()

        viagem.status = STATUS_VIAGEM_FINALIZADA
        viagem.data_chegada_real = agora()
        viagem.caminhao.status = STATUS_CAMINHAO_DISPONIVEL
        viagem.motorista.status = STATUS_MOTORISTA_DISPONIVEL
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} finalizada.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def cancelar(db: Session, viagem_id: int, motivo: str) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)
        if viagem.status == STATUS_VIAGEM_FINALIZADA:
            raise ValueError("Uma viagem finalizada não pode ser cancelada.")

        viagem.status = STATUS_VIAGEM_CANCELADA
        viagem.observacoes = (viagem.observacoes or "") + f"\\n[CANCELAMENTO] {motivo}"
        viagem.caminhao.status = STATUS_CAMINHAO_DISPONIVEL
        viagem.motorista.status = STATUS_MOTORISTA_DISPONIVEL

        for carga in viagem.cargas:
            if carga.status in [STATUS_CARGA_RESERVADA, STATUS_CARGA_EMBARCADA]:
                carga.status = STATUS_CARGA_PATIO
                carga.caminhao_id = None
                carga.viagem_id = None
                carga.atualizado_em = agora()

        db.flush()
        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} cancelada. Motivo: {motivo}",
            viagem.id,
        )
        return viagem
    @staticmethod
    def gerar_codigo(db: Session) -> str:
        ultimo = db.query(Viagem).order_by(Viagem.id.desc()).first()
        proximo_numero = 1 if not ultimo else ultimo.id + 1
        return f"VG-{datetime.now().strftime('%Y%m')}-{proximo_numero:05d}"

    @staticmethod
    def criar(
        db: Session,
        origem: str,
        destino: str,
        distancia_km: float,
        caminhao_id: int,
        motorista_id: int,
        data_saida_prevista: Optional[datetime] = None,
        data_chegada_prevista: Optional[datetime] = None,
        observacoes: str = "",
    ) -> Viagem:
        caminhao = CaminhaoService.buscar_por_id(db, caminhao_id)
        motorista = MotoristaService.buscar_por_id(db, motorista_id)

        if caminhao.status != STATUS_CAMINHAO_DISPONIVEL:
            raise ValueError("O caminhão selecionado não está disponível.")

        if motorista.status != STATUS_MOTORISTA_DISPONIVEL:
            raise ValueError("O motorista selecionado não está disponível.")

        codigo = ViagemService.gerar_codigo(db)

        viagem = Viagem(
            codigo=codigo,
            origem=origem.strip(),
            destino=destino.strip(),
            distancia_km=distancia_km,
            status=STATUS_VIAGEM_PLANEJADA,
            data_saida_prevista=data_saida_prevista,
            data_chegada_prevista=data_chegada_prevista,
            observacoes=observacoes.strip() or None,
            caminhao=caminhao,
            motorista=motorista,
        )
        db.add(viagem)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Viagem",
            f"Viagem {codigo} criada com sucesso.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def iniciar(db: Session, viagem_id: int) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)

        if viagem.status != STATUS_VIAGEM_PLANEJADA:
            raise ValueError("Somente viagens planejadas podem ser iniciadas.")

        if viagem.caminhao.status != STATUS_CAMINHAO_DISPONIVEL:
            raise ValueError("O caminhão desta viagem não está disponível para início.")

        if viagem.motorista.status != STATUS_MOTORISTA_DISPONIVEL:
            raise ValueError("O motorista desta viagem não está disponível para início.")

        viagem.status = STATUS_VIAGEM_EM_ANDAMENTO
        viagem.data_saida_real = agora()
        viagem.caminhao.status = STATUS_CAMINHAO_EM_ROTA
        viagem.motorista.status = STATUS_MOTORISTA_EM_VIAGEM
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} iniciada.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def finalizar(db: Session, viagem_id: int) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)

        if viagem.status not in [STATUS_VIAGEM_PLANEJADA, STATUS_VIAGEM_EM_ANDAMENTO]:
            raise ValueError("A viagem não pode ser finalizada no estado atual.")

        for carga in viagem.cargas:
            if carga.status == STATUS_CARGA_EMBARCADA:
                carga.status = STATUS_CARGA_ENTREGUE
                carga.atualizado_em = agora()

        viagem.status = STATUS_VIAGEM_FINALIZADA
        viagem.data_chegada_real = agora()
        viagem.caminhao.status = STATUS_CAMINHAO_DISPONIVEL
        viagem.motorista.status = STATUS_MOTORISTA_DISPONIVEL
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} finalizada.",
            viagem.id,
        )
        return viagem
    @staticmethod
    def gerar_codigo(db: Session) -> str:
        ultimo = db.query(Viagem).order_by(Viagem.id.desc()).first()
        proximo_numero = 1 if not ultimo else ultimo.id + 1
        return f"VG-{datetime.now().strftime('%Y%m')}-{proximo_numero:05d}"

    @staticmethod
    def criar(
        db: Session,
        origem: str,
        destino: str,
        distancia_km: float,
        caminhao_id: int,
        motorista_id: int,
        data_saida_prevista: Optional[datetime] = None,
        data_chegada_prevista: Optional[datetime] = None,
        observacoes: str = "",
    ) -> Viagem:
        caminhao = CaminhaoService.buscar_por_id(db, caminhao_id)
        motorista = MotoristaService.buscar_por_id(db, motorista_id)

        if caminhao.status != STATUS_CAMINHAO_DISPONIVEL:
            raise ValueError("O caminhão selecionado não está disponível.")

        if motorista.status != STATUS_MOTORISTA_DISPONIVEL:
            raise ValueError("O motorista selecionado não está disponível.")

        codigo = ViagemService.gerar_codigo(db)

        viagem = Viagem(
            codigo=codigo,
            origem=origem.strip(),
            destino=destino.strip(),
            distancia_km=distancia_km,
            status=STATUS_VIAGEM_PLANEJADA,
            data_saida_prevista=data_saida_prevista,
            data_chegada_prevista=data_chegada_prevista,
            observacoes=observacoes.strip() or None,
            caminhao=caminhao,
            motorista=motorista,
        )
        db.add(viagem)
        db.flush()

        caminhao.status = STATUS_CAMINHAO_EM_ROTA
        motorista.status = STATUS_MOTORISTA_EM_VIAGEM
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_CADASTRO,
            "Viagem",
            f"Viagem {codigo} criada com sucesso.",
            viagem.id,
        )
        return viagem

    @staticmethod
    def listar(db: Session) -> List[Viagem]:
        return db.query(Viagem).order_by(Viagem.id.asc()).all()

    @staticmethod
    def buscar_por_id(db: Session, viagem_id: int) -> Viagem:
        obj = db.query(Viagem).filter(Viagem.id == viagem_id).first()
        if not obj:
            raise ValueError("Viagem não encontrada.")
        return obj

    @staticmethod
    def iniciar(db: Session, viagem_id: int) -> Viagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)
        if viagem.status != STATUS_VIAGEM_PLANEJADA:
            raise ValueError("Somente viagens planejadas podem ser iniciadas.")

        viagem.status = STATUS_VIAGEM_EM_ANDAMENTO
        viagem.data_saida_real = agora()
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "Viagem",
            f"Viagem {viagem.codigo} iniciada.",
            viagem.id,
        )
        return viagem

# ============================================================
# SERVIÇOS DE NEGÓCIO - CUSTOS
# ============================================================
class CustoViagemService:
    @staticmethod
    def adicionar(db: Session, viagem_id: int, tipo: str, descricao: str, valor: float) -> CustoViagem:
        viagem = ViagemService.buscar_por_id(db, viagem_id)
        if valor < 0:
            raise ValueError("O valor do custo não pode ser negativo.")

        custo = CustoViagem(
            viagem=viagem,
            tipo=tipo.strip(),
            descricao=descricao.strip(),
            valor=valor,
        )
        db.add(custo)
        db.flush()

        registrar_evento(
            db,
            TIPO_EVENTO_OPERACAO,
            "CustoViagem",
            f"Custo '{descricao}' adicionado à viagem {viagem.codigo}.",
            custo.id,
        )
        return custo

    @staticmethod
    def listar_por_viagem(db: Session, viagem_id: int) -> List[CustoViagem]:
        return (
            db.query(CustoViagem)
            .filter(CustoViagem.viagem_id == viagem_id)
            .order_by(CustoViagem.id.asc())
            .all()
        )

    @staticmethod
    def total_por_viagem(db: Session, viagem_id: int) -> float:
        itens = CustoViagemService.listar_por_viagem(db, viagem_id)
        return sum(i.valor for i in itens)


# ============================================================
# RELATÓRIOS
# ============================================================
class RelatorioService:
    @staticmethod
    def dashboard_operacional(db: Session) -> Dict[str, int]:
        dados = {
            "caminhoes_total": db.query(Caminhao).count(),
            "caminhoes_disponiveis": db.query(Caminhao).filter(Caminhao.status == STATUS_CAMINHAO_DISPONIVEL).count(),
            "motoristas_total": db.query(Motorista).count(),
            "motoristas_disponiveis": db.query(Motorista).filter(Motorista.status == STATUS_MOTORISTA_DISPONIVEL).count(),
            "cargas_total": db.query(Carga).count(),
            "cargas_patio": db.query(Carga).filter(Carga.status == STATUS_CARGA_PATIO).count(),
            "cargas_embarcadas": db.query(Carga).filter(Carga.status == STATUS_CARGA_EMBARCADA).count(),
            "cargas_entregues": db.query(Carga).filter(Carga.status == STATUS_CARGA_ENTREGUE).count(),
            "viagens_total": db.query(Viagem).count(),
            "viagens_ativas": db.query(Viagem).filter(Viagem.status.in_([STATUS_VIAGEM_PLANEJADA, STATUS_VIAGEM_EM_ANDAMENTO])).count(),
        }
        registrar_evento(
            db,
            TIPO_EVENTO_RELATORIO,
            "Dashboard",
            "Dashboard operacional consultado.",
            None,
        )
        return dados

    @staticmethod
    def ocupacao_frota(db: Session) -> List[Tuple[str, float, float, float]]:
        resultado = []
        caminhoes = CaminhaoService.listar(db)
        for c in caminhoes:
            peso_total = CargaService.peso_total_por_caminhao(db, c.id)
            capacidade = c.capacidade_max_kg
            ocupacao_pct = (peso_total / capacidade * 100.0) if capacidade > 0 else 0.0
            resultado.append((c.placa, capacidade, peso_total, ocupacao_pct))

        registrar_evento(
            db,
            TIPO_EVENTO_RELATORIO,
            "Frota",
            "Relatório de ocupação da frota consultado.",
            None,
        )
        return resultado

    @staticmethod
    def rentabilidade_viagem(db: Session, viagem_id: int) -> Dict[str, float]:
        viagem = ViagemService.buscar_por_id(db, viagem_id)
        receita = sum(c.valor_mercadoria * 0.05 for c in viagem.cargas)
        custo_total = sum(c.valor for c in viagem.custos)
        margem = receita - custo_total
        margem_pct = (margem / receita * 100.0) if receita > 0 else 0.0

        registrar_evento(
            db,
            TIPO_EVENTO_RELATORIO,
            "Rentabilidade",
            f"Relatório de rentabilidade consultado para a viagem {viagem.codigo}.",
            viagem.id,
        )

        return {
            "receita_estimativa": receita,
            "custo_total": custo_total,
            "margem": margem,
            "margem_pct": margem_pct,
        }

    @staticmethod
    def alertas_prazo(db: Session) -> List[Carga]:
        limite = agora() + timedelta(hours=24)
        cargas = (
            db.query(Carga)
            .filter(Carga.prazo_entrega.isnot(None))
            .filter(Carga.prazo_entrega <= limite)
            .filter(Carga.status.in_([STATUS_CARGA_PATIO, STATUS_CARGA_RESERVADA, STATUS_CARGA_EMBARCADA]))
            .order_by(Carga.prazo_entrega.asc())
            .all()
        )
        registrar_evento(
            db,
            TIPO_EVENTO_RELATORIO,
            "Prazo",
            "Relatório de cargas com prazo próximo consultado.",
            None,
        )
        return cargas

    @staticmethod
    def ultimos_eventos(db: Session, limite: int = 20) -> List[EventoAuditoria]:
        return (
            db.query(EventoAuditoria)
            .order_by(EventoAuditoria.id.desc())
            .limit(limite)
            .all()
        )


# ============================================================
# CAMADA DE APRESENTAÇÃO - IMPRESSÃO FORMATADA
# ============================================================
def mostrar_caminhoes(itens: List[Caminhao]) -> None:
    titulo("FROTA DE CAMINHÕES")
    if not itens:
        print("Nenhum caminhão cadastrado.")
        return
    for c in itens:
        print(
            f"ID: {c.id} | Placa: {c.placa} | Tipo: {c.tipo} | "
            f"Capacidade: {c.capacidade_max_kg:.2f} kg | Status: {c.status}"
        )


def mostrar_motoristas(itens: List[Motorista]) -> None:
    titulo("MOTORISTAS")
    if not itens:
        print("Nenhum motorista cadastrado.")
        return
    for m in itens:
        print(
            f"ID: {m.id} | Nome: {m.nome} | CPF: {m.cpf} | "
            f"CNH: {m.cnh}/{m.categoria_cnh} | Status: {m.status}"
        )


def mostrar_clientes(itens: List[Cliente]) -> None:
    titulo("CLIENTES")
    if not itens:
        print("Nenhum cliente cadastrado.")
        return
    for c in itens:
        print(
            f"ID: {c.id} | Nome: {c.nome} | Documento: {c.documento} | "
            f"Cidade: {c.cidade or '-'} | Contato: {c.contato or '-'}"
        )


def mostrar_cargas(itens: List[Carga]) -> None:
    titulo("CARGAS")
    if not itens:
        print("Nenhuma carga cadastrada.")
        return
    for c in itens:
        print(
            f"ID: {c.id} | NF: {c.nota_fiscal} | Desc: {c.descricao} | "
            f"Peso: {c.peso_kg:.2f} kg | Destino: {c.cidade_destino} | "
            f"Status: {c.status} | Caminhão ID: {c.caminhao_id or '-'} | Viagem ID: {c.viagem_id or '-'}"
        )


def mostrar_viagens(itens: List[Viagem]) -> None:
    titulo("VIAGENS")
    if not itens:
        print("Nenhuma viagem cadastrada.")
        return
    for v in itens:
        print(
            f"ID: {v.id} | Código: {v.codigo} | {v.origem} -> {v.destino} | "
            f"KM: {v.distancia_km:.1f} | Status: {v.status} | "
            f"Caminhão: {v.caminhao.placa} | Motorista: {v.motorista.nome}"
        )


def mostrar_custos(itens: List[CustoViagem]) -> None:
    titulo("CUSTOS DA VIAGEM")
    if not itens:
        print("Nenhum custo registrado para esta viagem.")
        return
    total = 0.0
    for i in itens:
        total += i.valor
        print(f"ID: {i.id} | Tipo: {i.tipo} | Desc: {i.descricao} | Valor: R$ {i.valor:.2f}")
    print(f"\nTOTAL: R$ {total:.2f}")


def mostrar_dashboard(dados: Dict[str, int]) -> None:
    titulo("DASHBOARD OPERACIONAL")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")


def mostrar_ocupacao_frota(dados: List[Tuple[str, float, float, float]]) -> None:
    titulo("OCUPAÇÃO DA FROTA")
    if not dados:
        print("Nenhum caminhão cadastrado.")
        return
    for placa, capacidade, peso_total, pct in dados:
        print(
            f"Placa: {placa} | Capacidade: {capacidade:.2f} kg | "
            f"Ocupado: {peso_total:.2f} kg | Ocupação: {pct:.2f}%"
        )


def mostrar_rentabilidade(dados: Dict[str, float]) -> None:
    titulo("RENTABILIDADE DA VIAGEM")
    print(f"Receita estimada: R$ {dados['receita_estimativa']:.2f}")
    print(f"Custo total:       R$ {dados['custo_total']:.2f}")
    print(f"Margem:            R$ {dados['margem']:.2f}")
    print(f"Margem %:          {dados['margem_pct']:.2f}%")


def mostrar_alertas_prazo(itens: List[Carga]) -> None:
    titulo("ALERTAS DE PRAZO")
    if not itens:
        print("Nenhuma carga em alerta de prazo nas próximas 24 horas.")
        return
    for c in itens:
        print(
            f"NF: {c.nota_fiscal} | Destino: {c.cidade_destino} | "
            f"Prazo: {fmt_dt(c.prazo_entrega)} | Status: {c.status}"
        )


def mostrar_eventos(itens: List[EventoAuditoria]) -> None:
    titulo("AUDITORIA / ÚLTIMOS EVENTOS")
    if not itens:
        print("Nenhum evento registrado.")
        return
    for e in itens:
        print(
            f"[{fmt_data_iso(e.criado_em)}] {e.tipo} | {e.entidade}#{e.entidade_id or '-'} | {e.mensagem}"
        )


# ============================================================
# SEED DE DEMONSTRAÇÃO
# ============================================================
def seed_demo(db: Session) -> None:
    if db.query(Caminhao).count() > 0:
        print("[SEED] Dados já existem. Seed ignorado.")
        return

    # Caminhões
    c1 = CaminhaoService.criar(db, "ABC1D23", "Truck", 14000, "Volvo", "VM 270", 2022)
    c2 = CaminhaoService.criar(db, "EFG4H56", "Carreta", 28000, "Scania", "R450", 2023)
    c3 = CaminhaoService.criar(db, "IJK7L89", "Toco", 8000, "Mercedes", "Atego", 2021)

    # Motoristas
    m1 = MotoristaService.criar(db, "Carlos Mendes", "11111111111", "CNH001", "E", "11999990001")
    m2 = MotoristaService.criar(db, "Roberto Lima", "22222222222", "CNH002", "D", "11999990002")
    MotoristaService.criar(db, "João Alves", "33333333333", "CNH003", "E", "11999990003")

    # Clientes
    cl1 = ClienteService.criar(db, "Atacado Central", "12345678000100", "São Paulo", "Marina", "marina@cliente.com")
    cl2 = ClienteService.criar(db, "Distribuidora Sul", "00999888000199", "Curitiba", "Paulo", "paulo@cliente.com")

    # Cargas
    CargaService.criar(
        db,
        "NF1001",
        "Eletrodomésticos",
        3200,
        55000,
        "São Paulo",
        "Campinas",
        agora() + timedelta(hours=18),
        cl1.id,
        "Carga frágil",
    )
    CargaService.criar(
        db,
        "NF1002",
        "Alimentos embalados",
        4500,
        42000,
        "São Paulo",
        "Sorocaba",
        agora() + timedelta(days=2),
        cl1.id,
        "Entrega em doca 2",
    )
    CargaService.criar(
        db,
        "NF1003",
        "Peças automotivas",
        7800,
        88000,
        "Guarulhos",
        "Curitiba",
        agora() + timedelta(hours=20),
        cl2.id,
        "Exige conferência no recebimento",
    )

    # Viagem
    viagem = ViagemService.criar(
        db,
        "São Paulo",
        "Campinas",
        105,
        c1.id,
        m1.id,
        agora() + timedelta(hours=2),
        agora() + timedelta(hours=6),
        "Viagem inicial de demonstração",
    )

    # Reservar e embarcar uma carga
    carga1 = db.query(Carga).filter(Carga.nota_fiscal == "NF1001").first()
    if carga1:
        CargaService.reservar_para_viagem(db, carga1.id, viagem.id)
        CargaService.embarcar_carga(db, carga1.id)

    # Custos
    CustoViagemService.adicionar(db, viagem.id, "Combustível", "Abastecimento inicial", 750.00)
    CustoViagemService.adicionar(db, viagem.id, "Pedágio", "Pedágios ida", 65.50)

    # Ajustar status de outro caminhão
    CaminhaoService.atualizar_status(db, c2.id, STATUS_CAMINHAO_MANUTENCAO)

    registrar_evento(db, TIPO_EVENTO_OPERACAO, "Seed", "Carga inicial do sistema concluída.")
    print("[SEED] Dados de demonstração carregados com sucesso.")


# ============================================================
# MENUS - OPERAÇÕES
# ============================================================
def menu_cadastrar_caminhao() -> None:
    titulo("CADASTRAR CAMINHÃO")
    placa = pedir_texto("Placa: ")
    tipo = pedir_texto("Tipo (Toco/Truck/Carreta): ")
    capacidade = pedir_float("Capacidade máxima (kg): ", 1)
    marca = pedir_texto("Marca (opcional): ", obrigatorio=False)
    modelo = pedir_texto("Modelo (opcional): ", obrigatorio=False)
    ano_txt = pedir_texto("Ano (opcional): ", obrigatorio=False)
    ano = int(ano_txt) if ano_txt else None

    with get_db() as db:
        obj = CaminhaoService.criar(db, placa, tipo, capacidade, marca, modelo, ano)
        print(f"[OK] Caminhão {obj.placa} cadastrado com sucesso (ID: {obj.id}).")


def menu_cadastrar_carga() -> None:
    titulo("CADASTRAR CARGA (NF)")
    nf = pedir_texto("Nota Fiscal (Ex: NF2001): ")
    desc = pedir_texto("Descrição do material: ")
    peso = pedir_float("Peso (kg): ", 0.1)
    valor = pedir_float("Valor da Mercadoria (R$): ", 0)
    origem = pedir_texto("Cidade de Origem: ")
    destino = pedir_texto("Cidade de Destino: ")
    prazo = pedir_data("Prazo de entrega (YYYY-MM-DD HH:MM) [Opcional]: ", obrigatorio=False)
    
    with get_db() as db:
        # Simplificação para o MVP: cadastra sem atrelar a um cliente específico no momento da criação rápida
        obj = CargaService.criar(
            db, nf, desc, peso, valor, origem, destino, prazo, None, "Criado via Menu"
        )
        print(f"[OK] Carga NF {obj.nota_fiscal} cadastrada (ID: {obj.id}). Status: {obj.status}")


def menu_criar_viagem() -> None:
    titulo("PLANEJAR NOVA VIAGEM")
    origem = pedir_texto("Origem: ")
    destino = pedir_texto("Destino: ")
    dist = pedir_float("Distância estimada (km): ", 0.1)
    
    with get_db() as db:
        mostrar_caminhoes(CaminhaoService.listar(db))
        cam_id = pedir_int("Digite o ID do Caminhão: ")
        
        mostrar_motoristas(MotoristaService.listar(db))
        mot_id = pedir_int("Digite o ID do Motorista: ")
        
        # Para simplificar o MVP, não pedimos as datas no menu, deixamos None (a calcular)
        try:
            viagem = ViagemService.criar(
                db, origem, destino, dist, cam_id, mot_id, None, None, "Viagem planejada via Menu"
            )
            print(f"[OK] Viagem {viagem.codigo} planejada com sucesso! (ID: {viagem.id})")
        except Exception as e:
            print(f"[ERRO] {e}")


def menu_alocar_carga() -> None:
    titulo("ALOCAR CARGA EM VIAGEM")
    with get_db() as db:
        cargas_patio = db.query(Carga).filter(Carga.status == STATUS_CARGA_PATIO).all()
        if not cargas_patio:
            print("[INFO] Não há cargas no pátio aguardando alocação.")
            return
            
        mostrar_cargas(cargas_patio)
        carga_id = pedir_int("Digite o ID da Carga para alocar: ")
        
        viagens_plan = db.query(Viagem).filter(Viagem.status == STATUS_VIAGEM_PLANEJADA).all()
        if not viagens_plan:
            print("[INFO] Não há viagens planejadas para receber carga.")
            return
            
        mostrar_viagens(viagens_plan)
        viagem_id = pedir_int("Digite o ID da Viagem destino: ")
        
        try:
            CargaService.reservar_para_viagem(db, carga_id, viagem_id)
            print(f"[OK] Carga ID {carga_id} reservada para a viagem ID {viagem_id}.")
            
            embarcar = pedir_texto("Deseja embarcar (carregar no caminhão) agora? (S/N): ")
            if embarcar.upper() == 'S':
                CargaService.embarcar_carga(db, carga_id)
                print("[OK] Carga constando como EMBARCADA no sistema.")
        except Exception as e:
            print(f"[ERRO - OPERAÇÃO ABORTADA] {e}")


def menu_ver_dashboard() -> None:
    with get_db() as db:
        dados = RelatorioService.dashboard_operacional(db)
        mostrar_dashboard(dados)
        
        print("\n")
        ocupacao = RelatorioService.ocupacao_frota(db)
        mostrar_ocupacao_frota(ocupacao)
        
        print("\n")
        alertas = RelatorioService.alertas_prazo(db)
        mostrar_alertas_prazo(alertas)


def menu_auditoria() -> None:
    with get_db() as db:
        eventos = RelatorioService.ultimos_eventos(db, 30)
        mostrar_eventos(eventos)


# ============================================================
# LOOP PRINCIPAL
# ============================================================
def iniciar_sistema() -> None:
    # Cria as tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    # Roda o seed para ter dados iniciais de teste
    with get_db() as db:
        try:
            seed_demo(db)
        except Exception as e:
            print(f"[AVISO SEED] {e}")

    while True:
        titulo("AURORA TMS - TERMINAL TÁTICO")
        print("1. Cadastrar Caminhão")
        print("2. Cadastrar Carga (NF)")
        print("3. Planejar Nova Viagem")
        print("4. Alocar/Embarcar Carga")
        print("5. Ver Dashboard Operacional (Heatmap Lógico)")
        print("6. Ver Logs de Auditoria (Eventos)")
        print("0. Sair do Sistema")
        
        opcao = pedir_texto("\nComando: ", obrigatorio=True)
        
        try:
            if opcao == "1":
                menu_cadastrar_caminhao()
            elif opcao == "2":
                menu_cadastrar_carga()
            elif opcao == "3":
                menu_criar_viagem()
            elif opcao == "4":
                menu_alocar_carga()
            elif opcao == "5":
                menu_ver_dashboard()
            elif opcao == "6":
                menu_auditoria()
            elif opcao == "0":
                print("\n[AURORA TMS] Encerrando sistema. Até logo.")
                break
            else:
                print("[ERRO] Comando inválido.")
        except Exception as e:
            print(f"\n[ERRO FATAL NO SISTEMA] {e}")
            
        input("\nPressione [ENTER] para continuar...")
        limpar_tela()


if __name__ == "__main__":
    limpar_tela()
    iniciar_sistema()