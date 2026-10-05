from types import SimpleNamespace

from oraculo_ia import PastorSalmo23


def make_carga(**kwargs):
    defaults = {
        "peso_kg": 3200,
        "valor_mercadoria": 55000,
        "prazo_entrega": None,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def test_score_carga_returns_weighted_score():
    carga = make_carga()
    score = PastorSalmo23._score_carga(carga)
    assert 0 <= score <= 100


def test_route_classification_boundaries():
    assert PastorSalmo23._classificar_rota(85) == "Pastos Verdes"
    assert PastorSalmo23._classificar_rota(50) == "Vale da Sombra"
    assert PastorSalmo23._classificar_rota(49.9) == "Mesa Preparada"
