import makepath

import numpy as np
import matplotlib.pyplot as plt

from pyFEM import Structure


# Momentos máximos
# pyFEM
params = {}    
# datos entrada
model = params['model'] = Structure(uy=True, rz=False)

# materiales
model.add_material('mat', E=1)

# secciones
model.add_section('sec', Iy=0.594)

# nodos
separacion_centros_vigas = 45
model.add_joint('A', x=0)
model.add_joint('B', x=separacion_centros_vigas)

# elementos aporticados
model.add_frame('1', 'A', 'B', 'mat', 'sec')

# apoyos
model.add_support('A', uy=True)
model.add_support('B', uy=True)

# patrones de carga
DC = 0.867 * 2.4
model.add_load_pattern('MDC')
model.add_distributed_load('MDC', '1', fy=-DC)

DW = 1
model.add_load_pattern('MDW')
model.add_distributed_load('MDW', '1', fy=-DW)

# solve
model.solve()
frame = model.frames['1']
loadPattern = model.load_patterns['MDC']
print(model.reactions[loadPattern])

# plot
loadPattern = model.load_patterns['MDC']
mz = model.internal_forces[loadPattern][frame].mz
x = np.linspace(0, frame.get_length(), len(mz))
    
fig, ax = plt.subplots()
    
ax.plot(x, -mz, 'r')
ax.set_title('Momento flector')
ax.set_xlim(min(x), max(x))
ax.set_ylim(ymax=0)

ax.set_xlabel('m')
ax.set_ylabel('kN m')

ax.set_xticks(x[::2])
ax.set_yticks(list(set(np.round_(-mz[::2], 3))))
ax.grid(True)
    
fig.savefig('MDC.png')
