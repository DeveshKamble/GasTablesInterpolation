from evaluateSpline import evaluateSpline, evaluateSplineDerivative
def hybrid_newton_bisection(target_y, bound_a, bound_b, splines, tol=1e-6, max_iter=100):
    
    # Evaluate the boundaries to ensure the root is actually trapped inside
    # solving f(x) = S(x) - target_y = 0
    y_a = evaluateSpline(bound_a, splines)
    y_b = evaluateSpline(bound_b, splines)
    
    f_a = y_a - target_y
    f_b = y_b - target_y
    
    # If the signs are the same, the root isn't in this interval (or there are two)
    if f_a * f_b > 0:
        print(f"Error: The root is not bracketed between Mach {bound_a} and {bound_b}.")
        return None
        
    # 2. Set initial guess to the midpoint
    x_n = (bound_a + bound_b) / 2.0
    
    for i in range(max_iter):
        # Evaluate current state
        current_y = evaluateSpline(x_n, splines)
        slope = evaluateSplineDerivative(x_n,splines)
        f_x = current_y - target_y
        
        # Checkpoint
        if abs(f_x) < tol:
            return x_n
        
        # Calculate the direction of Newton-Raphson
        if slope != 0.0:
            newton_step = f_x / slope
            x_next_newton = x_n - newton_step
        else:
            x_next_newton = bound_a - 1.0 
            
        # Check if the step is strictly inside the bounds
        if (bound_a < x_next_newton < bound_b):
            x_next = x_next_newton
        else:
            # Newton failed 
            x_next = (bound_a + bound_b) / 2.0
            
        # Replace either bound_a or bound_b with our new guess
        # Evaluate the function at our new point
        y_next= evaluateSpline(x_next, splines)
        f_next = y_next - target_y
        
        # If f_next and f_a have the same sign, x_next becomes the new bound_a
        if f_a * f_next > 0:
            bound_a = x_next
            f_a = f_next
        else:
            bound_b = x_next
            f_b = f_next
            
        # Update guess for the next iteration
        x_n = x_next
        
    print(f"Hybrid Solver Failed to converge after {max_iter} iterations.")
    return x_n

