from app.db.database import Base, engine
import app.models.domain.dog
import app.models.domain.owner
import app.models.domain.visit
import app.models.domain.token
import app.models.domain.schedule
import app.models.domain.course


# Se inicia la base de datos y de ser el caso crea la tabla
def init_db():
    print("Creando tablas en la base de datos...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
