import os

from sqlalchemy import create_engine
from sqlalchemy import exc
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
    # Production env
    vos = ['dih-vouchers%02d.eosc-hub.eu' % i for i in range(1, 31)]
    # vos = ['vo%d.example.org' % i for i in range(1, 3)]
    for vo in vos:
        db_session.add(dih.models.VO(name=vo))
        try:
            db_session.commit()
        except exc.IntegrityError:
            print("Not creating VO %s as it already exists" % vo)
            pass
