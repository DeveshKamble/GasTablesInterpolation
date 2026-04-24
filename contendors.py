
def calculateStep(data):
    h = []
    machArray = data['Mach']
    prev = machArray[0]
    for m in machArray[1:]:
        h.append(m - prev)
        prev = m
    return h

def solveTridiagonalSystem(lower, main, upper, rhs):
    n = len(main)
    x = [0.0] * n
    c_prime, d_prime = [0.0] * n, [0.0] * n
    c_prime[0] = upper[0] / main[0]
    d_prime[0] = rhs[0] / main[0]

    for i in range(1, n):
        m = main[i] - lower[i] * c_prime[i-1]
        c_prime[i] = upper[i] / m
        d_prime[i] = (rhs[i] - lower[i] * d_prime[i-1]) / m

    x[n-1] = d_prime[n-1]
    for i in range(n-2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i+1]
    return x

def solveMatrixEquations(lower, main, upper, rhs):
    sol = {}
    for header, b in rhs.items():
        sol[header] = solveTridiagonalSystem(lower, main, upper, b)
    return sol

def generate_spline_coefficients(mach_array, y_array, K_array):
    n = len(mach_array)
    splines = []
    for i in range(n - 1):
        h = mach_array[i+1] - mach_array[i]
        a = y_array[i]
        b = ((y_array[i+1] - y_array[i]) / h) - (h / 6.0) * (2.0 * K_array[i] + K_array[i+1])
        c = K_array[i] / 2.0
        d = (K_array[i+1] - K_array[i]) / (6.0 * h)
        splines.append({'x_start': mach_array[i], 'x_end': mach_array[i+1], 'a': a, 'b': b, 'c': c, 'd': d})
    return splines

def evaluate_spline(x_target, splines):
    for spline in splines:
        if spline['x_start'] <= x_target <= spline['x_end']:
            dx = x_target - spline['x_start']
            return spline['a'] + spline['b']*dx + spline['c']*(dx**2) + spline['d']*(dx**3)
    return None