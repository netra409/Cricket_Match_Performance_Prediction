from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:system@localhost/air_quality_db")

conn = engine.connect()

print("Connection successful!") 