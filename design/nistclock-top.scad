L0=33;
L1=24;
L2=4*L0+L1;
W0=48;
W1=10;
W2=W0+W1;
T=1.5;
H=13.5;
H2=T+1.25;

difference() {
    cube_center([L2,W2,H2]);
    cube_center([L2-2*T,W2-2*T,6]);
}

difference() {
cube_center([L2,W2,1.5]);
    
translate([0,0,0]) {
translate([-L0/2-L0,0,0])
digit();
translate([-L0/2,0,0])
digit();
translate([L0/2,0,0])
digit();
translate([L0/2+L0,0,0])
digit();
}

translate([0,23.5,0.75])
cube_center([L0*4,8,3]);

}

covermount();

module covermount() {
translate([L2/2-5,W2/2-5,0])
standoff(h=H2+8,od=6,id=2);
    translate([-L2/2+5,-W2/2+5,0])
standoff(h=H2+8,od=6,id=2);
    translate([-L2/2+5,W2/2-5,0])
standoff(h=H2+8,od=6,id=2);
    translate([L2/2-5,-W2/2+5,0])
standoff(h=H2+8,od=6,id=2);
}

module digit() {
        translate([0,0,0])
        cube_center([28,28,3]);
}

module standoff(od=5,id=2.5,h=12 ) {
    difference() {
    cylinder(d=od,h=h,$fn=32);
    cylinder(d=id,h=h+0.001,$fn=16);
    }
}
module cube_center(dims) {
  translate([0,0,dims[2]/2])
    cube(dims,center=true);
}