def local_cubic_lagrange(x_target, x_knots, y_knots):
    """Evaluates a 3rd-degree Lagrange polynomial using the 4 nearest knots."""
    n = len(x_knots)
    idx = 0
    for i in range(n-1):
        if x_knots[i] <= x_target <= x_knots[i+1]:
            idx = i
            break
    else:
        idx = n - 2 

    if idx == 0: indices = [0, 1, 2, 3]
    elif idx == n - 2: indices = [n-4, n-3, n-2, n-1]
    else: indices = [idx-1, idx, idx+1, idx+2]

    y_val = 0.0
    for j in indices:
        term = y_knots[j]
        for m in indices:
            if m != j:
                term *= (x_target - x_knots[m]) / (x_knots[j] - x_knots[m])
        y_val += term
    return y_val

def estimate_lagrange_slope(x_list, y_list, target_index):
    """
    Calculates the derivative of a Lagrange polynomial at a specific point.
    target_index: 0 for start slope, len(x_list)-1 for end slope.
    """
    n = len(x_list)
    x_target = x_list[target_index]
    slope = 0.0
    
    for i in range(n):
        # We need to find the derivative of the i-th Lagrange basis function: L'_i(x_target)
        # Using the product rule derivative formula for Lagrange basis:
      
        
        # Calculate the constant denominator for L_i
        denominator = 1
        for j in range(n):
            if i != j:
                denominator *= (x_list[i] - x_list[j])
        
        numerator = 0
        # Calculate the sum for the numerator of the derivative
        for j in range(n):
            if i != j:
                term = 1.0
                for k in range(n):
                    if k != i and k != j:
                        term *= (x_target - x_list[k])
                numerator += term
        
        slope += y_list[i] * (numerator / denominator)
        
    return slope

def generateSlopeDicts(data, pointsToUse=4):
    machArray = data['Mach']
    
    # Identify property headers (all keys except Mach)
    headers = list(data.keys())
    headers.remove('Mach')
    
    slopeStart = {}
    slopeEnd = {}
    
    for header in headers:
        values = data[header]
        
        # Calculate start slope (at index 0) using the first 'n' points
        slopeStart[header] = estimate_lagrange_slope(
            machArray[:pointsToUse], 
            values[:pointsToUse], 
            target_index=0
        )
        
        # Calculate end slope (at the last index) using the last 'n' points
        # target_index is relative to the slice, so it's pointsToUse - 1
        slopeEnd[header] = estimate_lagrange_slope(
            machArray[-pointsToUse:], 
            values[-pointsToUse:], 
            target_index=pointsToUse - 1
        )
        
    return slopeStart, slopeEnd
