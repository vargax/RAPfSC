
variables
x
y sumatoria de cruces
z;



x.LO=0;
x.UP=10;
y.LO=0;
y.UP=10;



equations
obj
rest1

;

obj.. z=e=((y+x)*x)/2;
rest1.. x=l=y;


Model Modelo1 /all/ ;

option nlp=CONOPT
Solve Modelo1 using nlp maximizing x;

Display x.l,y.l,z.l;
