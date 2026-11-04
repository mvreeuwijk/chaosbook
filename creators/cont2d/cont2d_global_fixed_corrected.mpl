# cont2d_global_fixed_corrected.mpl
#
# Produces: cont2d_global_fixed.png (and cont2d_global_fixed.eps), panel (d) of
#           fig:cont2d:global in maple/cont2d.md: the radii r* of the fixed
#           points of the radial equation against mu, stable branches black,
#           unstable branches grey.
#
# Why this replaces cont2d_global2.mws: that worksheet took dr/dt from the
# clockwise version of the model, so its radial function had the opposite
# sign of the one printed in the chapter and the stability diagram came out
# with black and grey swapped. This script derives dr/dt from the corrected
# printed system
#     x' = -y - x (mu + r^2 - r^4),   y' = x - y (mu + r^2 - r^4),
# i.e. r' = -mu r - r^3 + r^5, theta' = 1, and colours the branches by the
# sign of d(r')/dr. Reference implementation: creators/python/cont2d/fig_global.py.
#
# Usage: in Maple, currentdir("<repo>/maple/_static/cont2d"); then
#        read "<repo>/creators/cont2d/cont2d_global_fixed_corrected.mpl";

restart; with(plots):

# -- the model as printed in the chapter (counter-clockwise, theta' = +1) ------
F := (x, y) -> -y - x*(mu + x^2 + y^2 - (x^2 + y^2)^2):
G := (x, y) ->  x - y*(mu + x^2 + y^2 - (x^2 + y^2)^2):

# -- radial equation: dr/dt = (x x' + y y')/r, in polar coordinates -----------
rdot := simplify(subs(x = r*cos(theta), y = r*sin(theta),
                      (x*F(x, y) + y*G(x, y))/r)):
if simplify(rdot - (-mu*r - r^3 + r^5)) <> 0 then
    error "radial equation is not -mu*r - r^3 + r^5: %1", rdot;
end if:
g := unapply(rdot, [r, mu]):

# -- fixed points and their stability -----------------------------------------
# r* = 0 for every mu, with dg/dr = -mu: unstable for mu < 0, stable for mu > 0.
# The non-trivial fixed points satisfy mu = r^4 - r^2, so the branches can be
# drawn parametrically in r. On them dg/dr = 2 r^2 (2 r^2 - 1): the inner
# branch r < 1/sqrt(2) is stable, the outer branch r > 1/sqrt(2) is unstable.
# They meet in the saddle-node (blue-sky) bifurcation at mu = -1/4.
mufp   := r^4 - r^2:
dgfp   := factor(simplify(subs(mu = mufp, diff(g(r, mu), r)))):
print(dgfp);                                   # 2 r^2 (2 r^2 - 1)
rc     := 1/sqrt(2):                           # where dg/dr changes sign
print(subs(r = rc, mufp));                     # -1/4

# -- the four branches: black = stable, grey = unstable ------------------------
p_origin_u := plot([[-0.4, 0], [0, 0]],   color = gray,  thickness = 3):
p_origin_s := plot([[0, 0], [0.2, 0]],    color = black, thickness = 3):
p_inner_s  := plot([mufp, r, r = 0 .. rc], color = black, thickness = 3):
p_outer_u  := plot([mufp, r, r = rc .. 1], color = gray,  thickness = 3):

P := display([p_origin_u, p_origin_s, p_inner_s, p_outer_u],
             view = [-0.4 .. 0.2, 0 .. 1.02], labels = ['mu', "r*"],
             labeldirections = [horizontal, vertical]):

# -- output: eps as in the original worksheet, png for the HTML/PDF build -----
plotsetup(ps, plotoutput = `cont2d_global_fixed.eps`,
          plotoptions = `portrait,noborder,width=384,height=192`):
print(P);
plotsetup(png, plotoutput = "cont2d_global_fixed.png",
          plotoptions = "width=768,height=384"):
print(P);
plotsetup(default):
