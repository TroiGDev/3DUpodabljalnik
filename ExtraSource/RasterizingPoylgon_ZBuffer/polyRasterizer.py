def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def point_in_triangle(pt, v1, v2, v3):
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def interpolate(value1, value2, value3, weights):
    return (
        value1 * weights[0] +
        value2 * weights[1] +
        value3 * weights[2]
    )

def interpolate_z(x, y, p1, p2, p3):
        """Calculate interpolated Z value using barycentric coordinates"""
        v0 = (p3[0] - p1[0], p3[1] - p1[1])
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (x - p1[0], y - p1[1])
        
        dot00 = v0[0] * v0[0] + v0[1] * v0[1]
        dot01 = v0[0] * v1[0] + v0[1] * v1[1]
        dot02 = v0[0] * v2[0] + v0[1] * v2[1]
        dot11 = v1[0] * v1[0] + v1[1] * v1[1]
        dot12 = v1[0] * v2[0] + v1[1] * v2[1]
        
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        if u >= 0 and v >= 0 and u + v <= 1:
            return p1[2] * (1 - u - v) + p2[2] * u + p3[2] * v
        return None

def rasterize_triangle(pixels, z_buffer, v1, v2, v3, color):
    # Calculate bounding box
    min_x = max(0, int(min(v1[0], v2[0], v3[0])))
    max_x = min(len(pixels)-1, int(max(v1[0], v2[0], v3[0])))
    min_y = max(0, int(min(v1[1], v2[1], v3[1])))
    max_y = min(len(pixels[0])-1, int(max(v1[1], v2[1], v3[1])))

    # Scan through pixels in bounding box
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pt = (x, y)
            
            # Check if point is inside triangle
            if point_in_triangle(pt, v1, v2, v3):
                # Calculate barycentric coordinates
                area = abs(sign(v1, v2, v3)) * 0.5
                w1 = abs(sign(pt, v2, v3)) * 0.5 / area
                w2 = abs(sign(pt, v3, v1)) * 0.5 / area
                w3 = abs(sign(pt, v1, v2)) * 0.5 / area
                
                # Interpolate color (could be texture coordinates, normals, etc.)
                r = interpolate(color[0], color[0], color[0], [w1, w2, w3])
                g = interpolate(color[1], color[1], color[1], [w1, w2, w3])
                b = interpolate(color[2], color[2], color[2], [w1, w2, w3])

                #check buffer depth
                currDepth = interpolate_z(x, y, v1, v2, v3)
                if currDepth < z_buffer[x][y] or z_buffer[x][y] == None:
                
                    # Set pixel color
                    pixels[x][y] = (int(r), int(g), int(b))
                    z_buffer[x][y] = currDepth