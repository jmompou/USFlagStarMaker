import sys
import math
import itertools

def find_best_pattern(n):
    best_pattern = None
    best_score = float('inf')
    best_is_staggered = False
    
    # We will test different pattern generators that yield a list of row counts
    # Patterns: 
    # 1. Grid: C, C, C...
    # 2. Staggered 1: C, C-1, C, C-1...
    # 3. Staggered 2: C-1, C, C-1, C...
    # 4. Staggered 3: C, C, C, C... (shifted, which we just treat as a grid with a flag to shift)
    
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            
            patterns_to_test = []
            
            # 1. Grid
            if r * c == n:
                patterns_to_test.append(([c]*r, False))
                # Staggered version of same length
                if r > 1:
                    patterns_to_test.append(([c]*r, True))
                    
            # 2. Staggered C, C-1
            p2 = []
            for i in range(r):
                p2.append(c if i % 2 == 0 else c - 1)
            if sum(p2) == n and all(x > 0 for x in p2):
                patterns_to_test.append((p2, True))
                
            # 3. Staggered C-1, C
            p3 = []
            for i in range(r):
                p3.append(c - 1 if i % 2 == 0 else c)
            if sum(p3) == n and all(x > 0 for x in p3):
                patterns_to_test.append((p3, True))
                
            for pattern, is_stag in patterns_to_test:
                # Calculate visual bounding box aspect ratio
                # The flags often use width-heavy spacing, but the true 50-star uses max cols=6, rows=9
                # If we just want to match the ratio of "number of columns" to "number of rows":
                # Wait, for 48 stars: 8 cols / 6 rows = 1.33
                # For 50 stars: 6 cols / 9 rows = 0.66. But it is staggered.
                # In staggered (e.g. 50 stars), the effective horizontal columns are close to C + (C-1) = 2C - 1 half-columns
                # Let's define the ideal ratio for standard grid cols / rows ~ 1.3 to 1.5
                # For staggered, the visual aspect isn't defined just by c/r. 
                # Actually, aesthetics prefer:
                # - r and c are somewhat balanced, but c is usually strictly greater than r, OR
                # - if staggered, r can be larger than c.
                # Let's use a heuristic: 
                # The canton aspect is 1.411.
                # For non-staggered: we want c / r close to 1.411.
                # For staggered: we want c / (r / 2) close to 1.411 ? For 50 stars, c=6, r=9. 6 / 4.5 = 1.33. This fits!
                
                if not is_stag:
                    eff_aspect = c / r
                else:
                    eff_aspect = c / (r / 2.0)
                    
                aspect_diff = abs(eff_aspect - 1.411)
                
                score = aspect_diff
                
                # Penalize 1D patterns unless n <= 3
                if r == 1 or max(pattern) == 1:
                    score += 10
                    
                if score < best_score:
                    best_score = score
                    best_pattern = pattern
                    best_is_staggered = is_stag
                    
    if best_pattern is None:
        return [n], False
    return best_pattern, best_is_staggered

def generate_star_svg(cx, cy, r):
    points = []
    for i in range(10):
        angle = -math.pi/2 + i * math.pi/5
        radius = r if i % 2 == 0 else r * 0.38196601125
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(f"{x:.4f},{y:.4f}")
    return f'<polygon points="{" ".join(points)}" fill="#FFFFFF" />'

def make_flag(n, output_filename="bandera.svg"):
    pattern, is_staggered = find_best_pattern(n)
    print(f"Using pattern for {n} stars: {pattern} (staggered: {is_staggered})")
    
    # Flag proportions
    A = 1.0       # Hoist (height)
    B = 1.9       # Fly (width)
    C = 7/13      # Canton height
    D = 0.76      # Canton width
    L = 1/13      # Stripe width
    K = 0.0616    # Star diameter
    
    # Scale up for SVG coordinates (e.g. A = 1000)
    scale = 1000
    w = B * scale
    h = A * scale
    canton_w = D * scale
    canton_h = C * scale
    stripe_h = L * scale
    star_r = (K / 2) * scale
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    
    # 13 Stripes
    for i in range(13):
        color = "#B22234" if i % 2 == 0 else "#FFFFFF"
        y = i * stripe_h
        svg.append(f'<rect width="{w}" height="{stripe_h:.2f}" y="{y:.2f}" fill="{color}" />')
        
    # Canton
    svg.append(f'<rect width="{canton_w:.2f}" height="{canton_h:.2f}" y="0" fill="#3C3B6E" />')
    
    # Stars
    R = len(pattern)
    sy = canton_h / (R + 1)
    
    max_c = max(pattern)
    
    for i, c in enumerate(pattern):
        cy = (i + 1) * sy
        
        if is_staggered:
            if len(set(pattern)) == 1:
                # C, C, C staggered
                sx = canton_w / (c + 0.5)
                start_x = sx / 2 + (sx / 2 if i % 2 != 0 else 0)
            else:
                # C, C-1 staggered
                sx = canton_w / max_c
                if pattern[0] == max_c:
                    row_shift = 0 if i % 2 == 0 else 0.5
                else:
                    row_shift = 0.5 if i % 2 == 0 else 0
                start_x = sx / 2 + row_shift * sx
        else:
            # Regular grid
            sx = canton_w / max_c
            start_x = sx / 2 + ((max_c - c) / 2.0) * sx
            
        for j in range(c):
            cx = start_x + j * sx
            svg.append(generate_star_svg(cx, cy, star_r))
            
    svg.append('</svg>')
    
    with open(output_filename, 'w') as f:
        f.write("\n".join(svg))
    print(f"Generated {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 50
    make_flag(n)
