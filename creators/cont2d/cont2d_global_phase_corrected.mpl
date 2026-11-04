# cont2d_global_phase_corrected.mpl
#
# Produces: cont2d_global_phase1.png (mu = -0.26) and cont2d_global_phase2.png
#           (mu = -0.24), panels (a, b) of fig:cont2d:global in maple/cont2d.md,
#           plus cont2d_global_r.png, panel (c): dr/dt against r. Each also as .eps.
#
# Why this replaces cont2d_global.mws / cont2d_global2.mws: those worksheets
# integrated x' = -f, y' = -g with f = -y + x(...), g = x + y(...), i.e. the
# clockwise system x' = y - x(...), y' = -x - y(...) (theta' = -1). The
# chapter prints the counter-clockwise system
#     x' = -y - x (mu + r^2 - r^4),   y' = x - y (mu + r^2 - r^4),
# i.e. r' = -mu r - r^3 + r^5, theta' = +1, which is what this script
# integrates. Panel (c) is derived from the same system, so it plots
# r' = -mu r - r^3 + r^5. Reference implementation:
# creators/python/cont2d/fig_global.py.
#
# Usage: in Maple, currentdir("<repo>/maple/_static/cont2d"); then
#        read "<repo>/creators/cont2d/cont2d_global_phase_corrected.mpl";

restart; with(plots): with(DEtools):

# -- the model as printed in the chapter (counter-clockwise, theta' = +1) ------
F := (x, y) -> -y - x*(mu + x^2 + y^2 - (x^2 + y^2)^2):
G := (x, y) ->  x - y*(mu + x^2 + y^2 - (x^2 + y^2)^2):
DE1 := diff(x(t), t) = F(x(t), y(t)):
DE2 := diff(y(t), t) = G(x(t), y(t)):
ic  := x(0) = 0.15, y(0) = 0:
tstart := 0: tend := 200:

# -- check the polar form: r' = -mu r - r^3 + r^5 ----------------------------
rdot := simplify(subs(x = r*cos(theta), y = r*sin(theta),
                      (x*F(x, y) + y*G(x, y))/r)):
if simplify(rdot - (-mu*r - r^3 + r^5)) <> 0 then
    error "radial equation is not -mu*r - r^3 + r^5: %1", rdot;
end if:
fr := unapply(rdot, r):

# -- phase portrait for one value of mu ----------------------------------------
# Direction field (fixed-length arrows) plus the trajectory from (0.15, 0).
# For mu = -0.26 the trajectory escapes to infinity; the event halts the
# integration once it leaves the circle r = 3, well outside the plot window,
# so a "cannot evaluate the solution further right" warning is expected there.
phase := proc(muval, fname)
    local sys, sol, ptraj, parrows, P;
    sys := subs(mu = muval, {DE1, DE2});
    sol := dsolve(sys union {ic}, {x(t), y(t)}, numeric, maxfun = 0,
                  abserr = 1e-10, relerr = 1e-10,
                  events = [[x(t)^2 + y(t)^2 - 9, halt]]);
    ptraj := odeplot(sol, [x(t), y(t)], tstart .. tend, numpoints = 20000,
                     color = black, thickness = 2);
    parrows := fieldplot(subs(mu = muval, [F(x, y), G(x, y)]),
                         x = -1.25 .. 1.25, y = -1.25 .. 1.25, grid = [20, 20],
                         fieldstrength = fixed, arrows = SLIM, color = black);
    P := display([parrows, ptraj], view = [-1.25 .. 1.25, -1.25 .. 1.25],
                 axes = boxed, labels = ["x", "y"],
                 labeldirections = [horizontal, vertical]);
    plotsetup(ps, plotoutput = cat(fname, ".eps"),
              plotoptions = `portrait,noborder,width=256,height=256`);
    print(P);
    plotsetup(png, plotoutput = cat(fname, ".png"),
              plotoptions = "width=630,height=630");
    print(P);
    plotsetup(default);
end proc:

# -- panels (a) and (b): just before and just after the bifurcation -----------
phase(-0.26, "cont2d_global_phase1");
phase(-0.24, "cont2d_global_phase2");

# -- panel (c): dr/dt against r for three values of mu -------------------------
Pr := plot([subs(mu = -0.3, fr(r)), subs(mu = -0.2, fr(r)), subs(mu = -0.1, fr(r))],
           r = 0 .. 1, thickness = 2, color = black,
           linestyle = [solid, dash, dashdot],
           legend = ['mu = -0.3', 'mu = -0.2', 'mu = -0.1'],
           labels = ["r", "dr/dt"], labeldirections = [horizontal, vertical]):
plotsetup(ps, plotoutput = `cont2d_global_r.eps`,
          plotoptions = `portrait,noborder,width=384,height=192`):
print(Pr);
plotsetup(png, plotoutput = "cont2d_global_r.png",
          plotoptions = "width=768,height=384"):
print(Pr);
plotsetup(default):
