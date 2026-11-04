# cont3d_LorenzLyapComprehensive_corrected.mpl
#
# Produces: cont3d_LorenzLyapComprehensive.png, fig:cont3d:lorenzlyapcomprehensive
#           in maple/cont3d.md, as two stacked panels:
#             top    - the local stretching rates Lambda_1 <= Lambda_2 <= Lambda_3
#                      (eigenvalues of the symmetric Jacobian J_S) and the
#                      effective Lyapunov exponent Lambda_e along a Lorenz orbit;
#             bottom - the cumulative time averages of the same four curves.
#           The two panels are also kept as ..._top.png and ..._bottom.png.
#
# Why this replaces cont3d_lorenz.mw: the worksheet's figure has only the top
# panel, while the chapter text and caption now discuss the cumulative
# averages (the averaged stretching rates converge to about 4.2, -2.3, -15.6,
# but only the average of Lambda_e converges to the largest Lyapunov
# exponent, about 0.9). The bottom panel needs a second plot.
#
# Method (as in creators/python/cont3d/fig_lorenz_lyapunov.py): Lorenz system
# at r = 28, sigma = 10, b = 8/3; start at (2, 5, 5), discard a transient up
# to t = 10, then sample every dt = 0.005 up to t = 11. Lambda_e is
# eps . J_S eps / eps . eps for a perturbation eps that starts along x. The
# Python script takes eps as the difference of two trajectories 1e-12 apart;
# here eps obeys the tangent equation eps' = J eps, which is the limit of that
# difference for a vanishingly small initial separation.
#
# Usage: in Maple, currentdir("<repo>/maple/_static/cont3d"); then
#        read "<repo>/creators/cont3d/cont3d_LorenzLyapComprehensive_corrected.mpl";

restart; with(plots): with(LinearAlgebra):

# -- the Lorenz system ---------------------------------------------------------
r := 28: b := 8/3: sigma := 10:
f1 := (x, y, z) -> sigma*(y - x):
f2 := (x, y, z) -> -x*z + r*x - y:
f3 := (x, y, z) -> x*y - b*z:
DE := diff(x(t), t) = f1(x(t), y(t), z(t)),
      diff(y(t), t) = f2(x(t), y(t), z(t)),
      diff(z(t), t) = f3(x(t), y(t), z(t)):

# -- Jacobian J and its symmetric part J_S -------------------------------------
fs := [f1(x, y, z), f2(x, y, z), f3(x, y, z)]:
vs := [x, y, z]:
Jx := Matrix(3, 3, (i, j) -> diff(fs[i], vs[j])):
Js := unapply((Jx + Transpose(Jx))/2, [x, y, z]):

# -- transient: integrate from (2, 5, 5) to t = 10 onto the attractor ----------
sol0 := dsolve({DE, x(0) = 2, y(0) = 5, z(0) = 5}, numeric,
               method = dverk78, abserr = 1e-12, relerr = 1e-12):
p10 := sol0(10):
x10 := eval(x(t), p10): y10 := eval(y(t), p10): z10 := eval(z(t), p10):

# -- orbit plus tangent equation eps' = J(x(t)) eps, sampled every dt ----------
tmax := 11: dt := 0.005: N := round(tmax/dt) + 1:
timesteps := Array(1 .. N, i -> (i - 1)*dt):
E  := [e1(t), e2(t), e3(t)]:
JX := map(eval, Jx, {x = x(t), y = y(t), z = z(t)}):
TDE := seq(diff(E[i], t) = add(JX[i, j]*E[j], j = 1 .. 3), i = 1 .. 3):
ics := x(0) = x10, y(0) = y10, z(0) = z10, e1(0) = 1, e2(0) = 0, e3(0) = 0:
sol_arr := dsolve({DE, TDE, ics}, [x(t), y(t), z(t), op(E)], numeric,
                  method = dverk78, abserr = 1e-12, relerr = 1e-12,
                  output = timesteps):
hdr  := convert(sol_arr[1, 1], list):         # column names
data := sol_arr[2, 1]:                         # N x 7 Matrix of samples
col  := v -> ListTools:-Search(v, hdr):
tt := data[1 .. N, col(t)]:
xx := data[1 .. N, col(x(t))]:  yy := data[1 .. N, col(y(t))]:
zz := data[1 .. N, col(z(t))]:
ee := data[1 .. N, [col(e1(t)), col(e2(t)), col(e3(t))]]:

# -- local stretching rates and effective exponent at every sample -------------
L1 := Array(1 .. N): L2 := Array(1 .. N): L3 := Array(1 .. N): Le := Array(1 .. N):
for i from 1 to N do
    S  := evalf(Js(xx[i], yy[i], zz[i]));
    ev := sort(map(Re, convert(Eigenvalues(S), list)));   # Lambda_1 <= Lambda_2 <= Lambda_3
    L1[i] := ev[1]; L2[i] := ev[2]; L3[i] := ev[3];
    ep := Vector([ee[i, 1], ee[i, 2], ee[i, 3]]);      # perturbation at t_i
    Le[i] := (ep . (S . ep))/(ep . ep);
end do:

# -- cumulative time averages <Lambda>_t ---------------------------------------
cumavg := proc(A)
    local B, s, k;
    B := Array(1 .. N); s := 0;
    for k from 1 to N do s := s + A[k]; B[k] := s/k; end do;
    B;
end proc:
C1 := cumavg(L1): C2 := cumavg(L2): C3 := cumavg(L3): Ce := cumavg(Le):
printf("cumulative averages at t = %g: Lambda_3 %.2f, Lambda_2 %.2f, Lambda_1 %.2f, Lambda_e %.2f\n",
       tmax, C3[N], C2[N], C1[N], Ce[N]);

# -- the two panels: same colours as the Python figure -------------------------
pts := A -> [seq([tt[k], A[k]], k = 1 .. N)]:
Ptop := plot([pts(L3), pts(L2), pts(L1), pts(Le)],
             color = [red, green, blue, black], thickness = 1,
             legend = [Lambda[3], Lambda[2], Lambda[1], Lambda[e]],
             legendstyle = [location = top],
             view = [0 .. tmax, DEFAULT], labels = ["", 'Lambda'],
             labeldirections = [horizontal, vertical]):
Pbot := plot([pts(C3), pts(C2), pts(C1), pts(Ce)],
             color = [red, green, blue, black], thickness = 1,
             view = [0 .. tmax, DEFAULT],
             labels = ["t", "<Lambda>_t"],
             labeldirections = [horizontal, vertical]):

# -- output: each panel as png, then stack them into one image -----------------
plotsetup(png, plotoutput = "cont3d_LorenzLyapComprehensive_top.png",
          plotoptions = "width=750,height=375"):
print(Ptop);
plotsetup(png, plotoutput = "cont3d_LorenzLyapComprehensive_bottom.png",
          plotoptions = "width=750,height=375"):
print(Pbot);
plotsetup(default):
imgtop := ImageTools:-Read("cont3d_LorenzLyapComprehensive_top.png"):
imgbot := ImageTools:-Read("cont3d_LorenzLyapComprehensive_bottom.png"):
ImageTools:-Write("cont3d_LorenzLyapComprehensive.png",
                  ArrayTools:-Concatenate(1, imgtop, imgbot)):
