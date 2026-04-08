import pytest
import sqlite3
from src.sesion_4.task_repository import init_db, add_task, get_all_tasks, get_tasks_by_status


@pytest.fixture
def temp_db(tmp_path):
    """
    Fixture que crea una base de datos temporal única para cada test
    y devuelve la ruta al archivo .db.
    """
    db_file = tmp_path / "test_tasks.db"
    db_path = str(db_file)
    
    # Inicializamos la estructura de la base de datos
    init_db(db_path)
    
    return db_path


def test_add_and_get_all_tasks(temp_db):
    # Arrange: Base de datos temporal vacía
    
    # Act: Añadimos tareas reales a la base de datos
    add_task("Comprar leche", "pending", db_path=temp_db)
    add_task("Estudiar pytest", "done", db_path=temp_db)
    
    # Assert: Recuperamos y verificamos la persistencia real
    tasks = get_all_tasks(db_path=temp_db)
    assert len(tasks) == 2
    
    # SQLite devuelve tuplas (id, title, status)
    assert tasks[0][1] == "Comprar leche"
    assert tasks[0][2] == "pending"
    assert tasks[1][1] == "Estudiar pytest"
    assert tasks[1][2] == "done"


def test_get_tasks_by_status_only_returns_requested_status(temp_db):
    # Arrange: Insertamos tareas con diferentes estados en una BD aislada
    add_task("Tarea pendiente 1", "pending", db_path=temp_db)
    add_task("Tarea completada", "done", db_path=temp_db)
    add_task("Tarea pendiente 2", "pending", db_path=temp_db)

    # Act: Consultamos filtrando por estado "pending" y "done"
    pending_tasks = get_tasks_by_status("pending", db_path=temp_db)
    done_tasks = get_tasks_by_status("done", db_path=temp_db)

    # Assert: Comprobamos exhaustivamente que NO se filtran estados incorrectos
    assert len(pending_tasks) == 2
    for task in pending_tasks:
        assert task[2] == "pending"
        
    assert len(done_tasks) == 1
    for task in done_tasks:
        assert task[2] == "done"


def test_get_all_tasks_empty_db(temp_db):
    # Act & Assert: Verificar comportamiento con base de datos recién creada
    tasks = get_all_tasks(db_path=temp_db)
    assert len(tasks) == 0
    assert isinstance(tasks, list)


def test_add_task_empty_title_raises_error(temp_db):
    # Act & Assert: Se espera que la regla de negocio impida títulos vacíos
    with pytest.raises(ValueError):
        add_task("", "pending", db_path=temp_db)
        
    with pytest.raises(ValueError):
        add_task("   ", "pending", db_path=temp_db)  # Título con solo espacios


def test_add_task_invalid_status_raises_error(temp_db):
    # Act & Assert: Se espera que la regla de negocio impida estados desconocidos
    with pytest.raises(ValueError):
        add_task("Aprender IA", "in_progress", db_path=temp_db)