# -*- encoding: utf-8 -*-
from ...auth import Authenticator, NotAuthenticated
from .user import Model as User
import jwt
import time
from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class JwtAuthenticator(Authenticator):
    def __init__(self, parameter=None, **options):
        self.token_key = "Authorization-2nd"
        self.header_prefix = "Bearer"
        engine = create_engine('mysql+pymysql://'+'khan'+':'+'Wlswn1565-@@##JU-King'+'@'+'rm-2zeuvipu7f7pg7k72o.mysql.rds.aliyuncs.com'+':3306/'+'boheofficial')

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    def getUser(self, identity):
        user = self.session.query(User).filter(User.id == identity['sub']).first()
        if user.token_create_time > identity['iat']:
            self.session.close()
            raise NotAuthenticated
        else:
            self.session.close()
            return user

    def authenticate(self, request):
        token = request.headers.get(self.token_key)
        if token:
            token = token.decode('utf-8')
            if token.startswith(self.header_prefix):
                jwttoken = token.replace("Bearer","").strip()
                try:
                    options = {
                     'verify_signature': True,
                     'verify_exp': True,
                     'verify_nbf': True,
                     'verify_iat': True,
                     'verify_aud': False,
                     'require_exp': False,
                     'require_iat': False,
                     'require_nbf': False
                    }
                    identity = jwt.decode(jwttoken,u"iOjEsImlzcyI6I",algorithms=['HS256'],options=options)
                    return self.getUser(identity)
                except jwt.ExpiredSignatureError:
                    pass
                except jwt.InvalidAlgorithmError:
                    pass
                except jwt.InvalidIssuerError:
                    pass
                except jwt.DecodeError:
                    pass
                except jwt.InvalidIssuedAtError:
                    pass
                except jwt.ImmatureSignatureError:
                    pass
                except jwt.InvalidAudienceError:
                    pass
                except jwt.MissingRequiredClaimError:
                    pass
                except jwt.InvalidTokenError:
                    pass
                try:
                    identity = jwt.decode(jwttoken,"TYGHJK45SSAttt",algorithms=['HS256'],options=options)
                    return self.getUser(identity)
                except jwt.InvalidTokenError:
                    raise NotAuthenticated
        self.session.close()
