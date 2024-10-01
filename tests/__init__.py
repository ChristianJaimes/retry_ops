import pytest

@pytest.fixture(scope="session")
def setup_environment():
    # Aquí podrías configurar variables de entorno, una base de datos, etc.
    return "configuracion_global"
