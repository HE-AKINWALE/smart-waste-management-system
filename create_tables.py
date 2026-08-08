import app.models.user
import app.models.waste_bin
import app.models.collection_schedule
import app.models.collection_record
import app.models.notification
import app.models.system_config
import app.models.audit_log
import app.models.health_metric

from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")