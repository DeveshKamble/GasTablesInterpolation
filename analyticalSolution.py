GAMMA = 1.4

def exactAreaRatio(M):
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    exponent = (GAMMA + 1.0) / (2.0 * (GAMMA - 1.0))
    return (1.0 / M) * ((2.0 / (GAMMA + 1.0)) * core) ** exponent

def exactPressureRatio(M):
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return core ** (-GAMMA / (GAMMA - 1.0))

def exactTempRatio(M):
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return 1.0 / core

def exactDensityRatio(M):
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return core ** (-1.0 / (GAMMA - 1.0))