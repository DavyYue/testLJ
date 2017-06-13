
import hoomd
import hoomd.md
from hoomd.deprecated.init import read_xml
from hoomd.deprecated import dump

#replace next three lines with lj thing
# pot_width = 61
# table = hoomd.md.pair.table(width=pot_width, nlist=nl_c)
# table.set_from_file('1', '1', filename='/Users/davyyue/Research/msibi/msibi/tutorials/lj/potentials/pot.1-1.txt') #defines potential for particleto particle with energy


def writeTraj(epsilon, sigma): #seqNum is the number in the loop
    hoomd.context.initialize("")
    system = read_xml(filename="start.hoomdxml", wrap_coordinates=True) #artificial infinity
    nl_c = hoomd.md.nlist.cell()
    T_final = 0.05

    lj = hoomd.md.pair.lj(r_cut=3.0, nlist=nl_c)
    lj.pair_coeff.set('1', '1', epsilon=epsilon, sigma=sigma) # epsilon is energy, sigma is distance

    all_particles = hoomd.group.all()
    nvt_int = hoomd.md.integrate.langevin(seed=1, group=all_particles, kT=T_final)
    #dynamic temp change with for loop (can maybe check out)
    hoomd.md.integrate.mode_standard(dt=0.001)
    #integrate.\*_rigid() no longer exists. Use a standard integrator on group.rigid_center(), and define rigid bodies using constrain.rigid()


    hoomd.run(1e2) #equilibration
    output_dcd = hoomd.dump.dcd(filename='query-epsilon{0}.dcd'.format(epsilon), period=100, overwrite=True)
    #
    hoomd.run(1e3)

    output_xml = dump.xml(group=all_particles)
    output_xml.set_params(all=True)
    output_xml.write(filename='final-epsilon{0}.hoomdxml'.format(epsilon))


params = [(1.0, 1.0), (1.5, 1.0), (2.0, 1.0)]
for epsilon, sigma in params:
    writeTraj(epsilon, sigma)
