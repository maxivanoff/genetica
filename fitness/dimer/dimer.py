from fftoolbox2.parser import XYZ
from fftoolbox2.molecule import Molecule
import logging, sys
import time
import numpy as np

logger = logging.getLogger(__name__)
lf = '%(levelname)s: %(funcName)s at %(filename)s +%(lineno)s\n%(message)s\n'
logging.basicConfig(level=logging.DEBUG, format=lf)

class BenzeneDimer(object):

    def __init__(self):
        parser = XYZ(filename='benzene.xyz', here=True)
        self.data = {'name':'benzene'}
        self.data.update(parser.data)
        self.b1 = Molecule(data=self.data)

    def energy(self, individual=None):
        self.b2 = Molecule(data=self.data)
        v = np.array([0, 1, 0])
        self.b2.translate(v)
        self.dimer = self.b1 + self.b2
        self.write_com()
        E = None
        #individual.objectives['energy'] = E

    def write_com(self):
        s = '%NProc=8\n%mem=16gb\n%Chk=p-b3lyp-pvdz.chk\n#P PBE1PBE/gen EmpiricalDispersion=GD3 scf(fermi,xqc,maxcycle=200)\n\nbenzene dimer\n\n0 1\n'
        for site in self.dimer.sites:
            s += '%s   %f %f %f\n' % (site.element, site.x, site.y, site.z)
        s += '\n@/home/MARQNET/talipovm/basis-library/def2-TZVPPD.gbs\n\n\n'
        f = open('dimer.com', 'w')
        f.write(s)
        f.close()

d = BenzeneDimer()
d.energy()

