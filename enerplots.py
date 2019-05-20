# import matplotlib
# matplotlib.rc("text", usetex=True)
# import matplotlib.pyplot as plt
# plt.switch_backend('agg')

import yt
Rsun = 7.0e10
ds = yt.load('star.out.000030', n_ref=1)

s = yt.SlicePlot(ds, 'z', ('gas','density'), width=4.0e13, fontsize=35)
s.set_zlim('all',1.0e-12,5.0e-3)
ds.define_unit('Solar_Radii',(Rsun,'cm'))
s.set_axes_unit('Solar_Radii')
s.annotate_contour(field='Etot', factor=4, clim=(0.5,1.0), ncont=1, take_log=False, plot_args={"colors": "black","linewidths": 1})
# s.annotate_contour(field='Etot_noIe', factor=4, clim=(0.5,1.0), ncont=1, take_log=False, plot_args={"colors": "red","linewidths": 1})
s.save('dens_C.png')
print('saved dens')

# phi = yt.SlicePlot(ds, 'z', ('gas','Phi_phys'), width=4.0e13, fontsize=35)
# phi.set_zlim('all',-1.5e15,0.0)
# phi.annotate_contour(field='Etot', factor=4, clim=(0.5,1.0), ncont=1, take_log=False)
# phi.save('phi_wCM.png')
# print('saved phi')
#
# u = yt.SlicePlot(ds, 'z', ('gas','ie_phys'), width=4.0e13, fontsize=35)
# u.set_zlim('all',1.0e13,3.0e17)
# u.annotate_contour(field='Etot', factor=4, clim=(0.5,1.0), ncont=1, take_log=False)
# u.save('u_wCM.png')
# print('saved u')
#
# ke = yt.SlicePlot(ds, 'z', ('gas','ke_phys'), width=4.0e13, fontsize=35)
# ke.set_zlim('all',5.0e12,1.0e15)
# ke.annotate_contour(field='Etot', factor=4, clim=(0.5,1.0), ncont=1, take_log=False)
# ke.annotate_quiver('velocity_x','velocity_y',factor=32,normalize=False)
# ke.save('ke_wCM.png')
# print('saved ke')
