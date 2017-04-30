constants = {'X_0': 155000,
             'Y_0': 463000,
             'phi_0': 52.15517440,
             'lambda_0': 5.38720621,
             'K_p': [0, 2, 0, 2, 0, 2, 1, 4, 2, 4, 1],
             'K_q': [1, 0, 2, 1, 3, 2, 0, 0, 3, 1, 1],
             'K_pq': [3235.65389, -32.58297, -0.24750, -0.84978, -0.06550, -0.01709, -0.00738, 0.00530, -0.00039, 0.00033, -0.00012],
             'L_p': [1, 1, 1, 3, 1, 3, 0, 3, 1, 0, 2, 5],
             'L_q': [0, 1, 2, 0, 3, 1, 1, 2, 4, 2, 0, 0],
             'L_pq': [5260.52916, 105.94684, 2.45656, -0.81885, 0.05594, -0.05607, 0.01199, -0.00256, 0.00128, 0.00022, -0.00022, 0.00026]}

def convert_rd_wgs84(RD_X, RD_Y):
    d_X = 1E-5 * float(int(RD_X) - constants['X_0'])
    d_Y = 1E-5 * float(int(RD_Y) - constants['Y_0'])
    phi = 0
    lambd = 0

    for i in range(len(constants['K_p'])):
        phi += (constants['K_pq'][i] * d_X**constants['K_p'][i] * d_Y**constants['K_q'][i])
    phi = constants['phi_0'] + phi / 3600
    for i in range(len(constants['L_p'])):
        lambd += (constants['L_pq'][i] * d_X**constants['L_p'][i] * d_Y**constants['L_q'][i])
    lambd = constants['lambda_0'] + lambd / 3600

    return phi, lambd
