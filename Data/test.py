import csv

# =============================================================================
# 1. PHYSICS EQUATIONS & CONSTANTS
# =============================================================================
GAMMA = 1.4

def exact_area_ratio(M):
    """A / A*"""
    if M == 0:
        return float('inf') # Avoid division by zero
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    exponent = (GAMMA + 1.0) / (2.0 * (GAMMA - 1.0))
    return (1.0 / M) * ((2.0 / (GAMMA + 1.0)) * core) ** exponent

def exact_pressure_ratio(M):
    """P / P0"""
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return core ** (-GAMMA / (GAMMA - 1.0))

def exact_temp_ratio(M):
    """T / T0"""
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return 1.0 / core

def exact_density_ratio(M):
    """rho / rho0"""
    core = 1.0 + ((GAMMA - 1.0) / 2.0) * (M**2)
    return core ** (-1.0 / (GAMMA - 1.0))

# =============================================================================
# 2. HELPER TO GENERATE MACH NUMBERS
# =============================================================================
def linspace(start, stop, n):
    if n == 1: return [start]
    step = (stop - start) / (n - 1)
    return [start + i * step for i in range(n)]

# =============================================================================
# 3. CSV GENERATION
# =============================================================================
def generate_csv(filename="isentropic_gas_table.csv", m_start=0.1, m_end=3.0, num_points=30):
    mach_array = linspace(m_start, m_end, num_points)
    
    # Define the headers for the CSV
    headers = ['Mach','A/A*','P0/P','T0/T','rho0/rho']
    
    # Open the file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(headers)
        
        # Calculate properties and write each row
        for M in mach_array:
            a_ratio = exact_area_ratio(M)
            p_ratio = exact_pressure_ratio(M)
            t_ratio = exact_temp_ratio(M)
            d_ratio = exact_density_ratio(M)
            
            # Write the formatted data (rounding to 6 decimal places for cleanliness)
            writer.writerow([
                f"{M:.4f}",
                f"{a_ratio:.6f}",
                f"{p_ratio:.6f}",
                f"{t_ratio:.6f}",
                f"{d_ratio:.6f}"
            ])
            
    print(f"Success! Generated {num_points} rows of isentropic data in '{filename}'.")

# =============================================================================
# 4. EXECUTION
# =============================================================================
if __name__ == "__main__":
    # You can change the start, end, and number of points here
    generate_csv(filename="Data\isentropic_gas_table.csv", m_start=0.1, m_end=3.0, num_points=100)
    
    # Example for generating a high-density table:
    # generate_csv("dense_gas_table.csv", 0.01, 30.0, 700)