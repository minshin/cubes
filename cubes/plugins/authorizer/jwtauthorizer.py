from ...auth import Authorizer, SimpleAuthorizer
import jwt

from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .models import User, Doctor, Clinic
from ...query import Cell, cut_from_string, cut_from_dict, PointCut, SetCut

class JwtAuthorizer(SimpleAuthorizer):

    def __init__(self, rights_file=None, roles_file=None, roles=None,
                 rights=None, identity_dimension=None, order=None,
                 guest=None,**options):
        super(JwtAuthorizer, self).__init__(rights_file, roles_file, roles, rights, identity_dimension, order, guest,**options)
        engine = create_engine('mysql+pymysql://'+'khan'+':'+'Wlswn1565-@@##JU-King'+'@'+'rm-2zeuvipu7f7pg7k72o.mysql.rds.aliyuncs.com'+':3306/'+'boheofficial')
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def authorize(self, user, cubes):
        if user:
            role_group = user.group_unit
        else:
            role_group = 'guest'

        allowed_cubes = SimpleAuthorizer.authorize(self, role_group, cubes)
        return allowed_cubes

    def restricted_cell(self, user, cube, cell):
        if user == None:
            ident_dim_role = None
            try:
                ident_dim_role = cube.dimension('role')
            except NoSuchDimensionError:
                # If cube has the dimension, then use it, otherwise just
                # ignore it
                return Cell(cube, [])
            hier_role = ident_dim_role.hierarchy('default')

            if len(hier_role) != 1:
                raise ConfigurationError("Identity hierarchy has to be flat "
                                         "(%s in dimension %s is not)"
                                         % (str(hier_role), str(ident_dim_role)))

            ident_dim_comm = None
            try:
                ident_dim_comm = cube.dimension('commercial_tenant')
            except NoSuchDimensionError:
                # If cube has the dimension, then use it, otherwise just
                # ignore it
                return Cell(cube, [])
            hier_comm = ident_dim_comm.hierarchy('default')

            if len(hier_comm) != 1:
                 raise ConfigurationError("Identity hierarchy has to be flat "
                                          "(%s in dimension %s is not)"
                                         % (str(hier_comm), str(ident_dim_comm)))
            cuts = []
            if (cell and cell.cut_for_dimension('commercial_tenant')):
                cuts.append(SetCut(ident_dim_role, [['topdoctor'],['basedoctor']], hierarchy=hier_role, hidden=True))
            else:
                cuts.append(PointCut(ident_dim_comm, ['error'], hierarchy=hier_comm, hidden=True))

            if cell:
                return cell & Cell(cube, cuts)
            else:
                return Cell(cube, cuts)


        if user.group_unit == 'clinic':
            user_obj = self.session.query(User).filter(User.id == user.id).first()
            clinic_obj = self.session.query(Clinic).filter(Clinic.user_id == user.id).first()
            ident_dim_comm = None
            cuts = []
            try:
                ident_dim_comm = cube.dimension('commercial_tenant')
            except NoSuchDimensionError:
                # If cube has the dimension, then use it, otherwise just
                # ignore it
                pass
            hier_comm = ident_dim_comm.hierarchy('default')
            
            cuts.append(PointCut(ident_dim_comm, [clinic_obj.group_unit], hierarchy=hier_comm, hidden=True))
            
            if cell:
                return cell & Cell(cube, cuts)
            else:
                return Cell(cube, cuts)


        if user.group_unit == 'doctor':
            user_obj = self.session.query(User).filter(User.id == user.id).first()
            doctor = self.session.query(Doctor).filter(Doctor.user_id == user.id).first()

            groups = {}
            relations = {}
            cuts =[]
            ident_dim_doctor = None
            try:
                ident_dim_doctor = cube.dimension('doctor')
            except NoSuchDimensionError:
                # If cube has the dimension, then use it, otherwise just
                # ignore it
                pass
            hier_doctor = ident_dim_doctor.hierarchy('default')

            if len(hier_doctor) != 1:
                raise ConfigurationError("Identity hierarchy has to be flat "
                                         "(%s in dimension %s is not)"
                                         % (str(hier_doctor), str(ident_dim_doctor)))

            ident_dim_comm = None
            try:
                ident_dim_comm = cube.dimension('commercial_tenant')
            except NoSuchDimensionError:
                # If cube has the dimension, then use it, otherwise just
                # ignore it
                pass
            hier_comm = ident_dim_comm.hierarchy('default')

            if len(hier_comm) != 1:
                raise ConfigurationError("Identity hierarchy has to be flat "
                                         "(%s in dimension %s is not)"
                                         % (str(hier_comm), str(ident_dim_comm)))
            for group in user_obj.groups:
                groups[group.id] = group;
            for relation in user_obj.relations:
                relations[relation.user_group_id] = relation

            cuts.append(PointCut(ident_dim_doctor, [doctor.id], hierarchy=hier_doctor, hidden=True))

            comm = []

            for key, value in groups.items():
                comm.append([value.code])

            cuts.append(SetCut(ident_dim_comm, comm, hierarchy=hier_comm, hidden=True))
            if cell:
                return cell & Cell(cube, cuts)
            else:
                return Cell(cube, cuts)
        else:
            return cell
