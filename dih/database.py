import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ['DIH_DATABASE'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import dih.models
    Base.metadata.create_all(bind=engine)
    # Testing env
    db_session.add(dih.models.VO('vo1.example.org'))
    db_session.add(dih.models.VO('vo2.example.org'))
    #for i in range(1, 2):
    #    db_session.add(dih.models.VO('dih-vouchers%02d.eosc-hub.eu' % i))
    db_session.commit()
