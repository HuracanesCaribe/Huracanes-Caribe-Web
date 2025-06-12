import cairo

def draw_arrow(ctx, x0=50, y0=80, shaft_w=100, shaft_h=60, head_w=60, head_h=120):
    """
    Draws a right-pointing arrow based on seven editable corners.
    """
    # Derived coordinates
    y1 = y0 + shaft_h                  # Bottom of shaft
    x1 = x0 + shaft_w                  # Start of head base
    x2 = x1  - 8                         # Vertical base of triangle
    x3 = x1 + head_w                   # Tip of arrow
    y2 = y0 + (shaft_h // 2) + (head_h // 2)  # Bottom point of triangle
    y4 = y0 + (shaft_h // 2) - (head_h // 2)  # Top point of triangle

    # Start path at point 1 and go clockwise
    ctx.move_to(x0, y0)     # 1
    ctx.line_to(x0, y1)     # 2
    ctx.line_to(x1, y1)     # 3
    ctx.line_to(x2, y2)     # 4
    ctx.line_to(x3, y0 + shaft_h // 2)  # 5
    ctx.line_to(x2, y4)     # 6
    ctx.line_to(x1, y0)     # 7
    ctx.close_path()


WIDTH, HEIGHT = 400, 200
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

draw_arrow(ctx, x0=50, y0=60, shaft_w=120, shaft_h=60, head_w=60, head_h=100)

ctx.set_source_rgb(0, 0.6, 0)  # green fill
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(2)
ctx.stroke()

surface.write_to_png("arrow_custom.png")
print("✅ Arrow saved")
