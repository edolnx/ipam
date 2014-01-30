from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(39), nullable=False)
    network_id = Column(Integer, ForeignKey('network.id'), nullable=False)
    interface_id = Column(Integer)

    def __init__(self, address, network_id, interface_id):
        self.address = address
        self.network_id = network_id
        self.interface_id = interface_id

    def __repr__(self):
        return "<Address('%s','%s','%s')>" % (self.address,
                self.network_id,
                self.interface_id)


class Network(Base):
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True, nullable=False)
    cidr = Column(String(43, nullable=False))
    parent_network = Column(Integer, ForeignKey('network.id'))
    forward_zone = Column(Integer, ForeignKey('zone.id'))

    def __init__(self, cidr, parent_network, forward_zone):
        self.cidr = cidr
        self.parent_network = parent_network
        self.forward_zone = forward_zone


class Instance(Base):
    __tablename__ = 'instance'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))

    def __init__(self, name):
        self.name = name


class Interface(Base):
    __tablename__ = 'interface'
    id = Column(Integer, primary_key=True, nullable=False)
    instance_id = Column(Integer, ForeignKey('instance.id'))
    vnet_id = Column(Integer, ForeignKey('vnet.id'))

    def __init__(self, instance_id, vnet_id):
        self.instance_id = instance_id
        self.vnet_id = vnet_id


class Zone(Base):
    name = Column(String(255), primary_key=True, nullable=False)
    ttl = Column(Integer, default=6000)

    def __init__(self, ttl):
        self.ttl = ttl


class Vnet(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


addr = Address('1.2.3.4', '15', '18')
session = Session()
session.add(addr)
session.commit()
print addr.address
