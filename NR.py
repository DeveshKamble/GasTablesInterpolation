from evaluateSpline import evaluateSpline, evaluateSplineDerivative
def hybrid_newton_bisection(target_y, bound_a, bound_b, splines, tol=1e-6, max_iter=100):
    """
    A mathematically guaranteed root finder combining Newton-Raphson's speed
    with Bisection's absolute stability.
    """
    # 1. Evaluate the boundaries to ensure the root is actually trapped inside
    # We are solving f(x) = S(x) - target_y = 0
    y_a = evaluateSpline(bound_a, splines)
    y_b = evaluateSpline(bound_b, splines)
    
    f_a = y_a - target_y
    f_b = y_b - target_y
    
    # If the signs are the same, the root isn't in this interval (or there are two)
    if f_a * f_b > 0:
        print(f"Error: The root is not bracketed between Mach {bound_a} and {bound_b}.")
        return None
        
    # 2. Set our initial guess to the midpoint
    x_n = (bound_a + bound_b) / 2.0
    
    for i in range(max_iter):
        # Evaluate current state
        current_y = evaluateSpline(x_n, splines)
        slope = evaluateSplineDerivative(x_n,splines)
        f_x = current_y - target_y
        
        # --- SUCCESS CHECK ---
        if abs(f_x) < tol:
            return x_n
            
        # --- THE HYBRID DECISION ---
        # Calculate where Newton-Raphson WANTS to go
        if slope != 0.0:
            newton_step = f_x / slope
            x_next_newton = x_n - newton_step
        else:
            # Force a rejection if slope is exactly 0
            x_next_newton = bound_a - 1.0 
            
        # Check if the Newton step is safe (strictly inside our current cage)
        # We also force a bisection if it's converging too slowly (taking tiny steps)
        if (bound_a < x_next_newton < bound_b):
            # Take the Newton Step! It's fast and safe.
            x_next = x_next_newton
        else:
            # Newton failed (went out of bounds or slope flatlined). 
            # Take the Bisection Step! It's slow but guaranteed.
            x_next = (bound_a + bound_b) / 2.0
            
        # --- SHRINK THE CAGE ---
        # We need to replace either bound_a or bound_b with our new guess
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
            
        # Update our guess for the next iteration
        x_n = x_next
        
    print(f"Hybrid Solver Failed to converge after {max_iter} iterations.")
    return x_n

