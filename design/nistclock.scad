L0=33;
L1=24;
L2=4*L0+L1;
W0=48;
W1=10;
W2=W0+W1;
T=1.5;
H=13.5;
offset=3;

difference() {
    cube_center([L2,W2,H+T]);
    
    translate([0,0,1.5])
    cube_center([L2-2*1.5,W2-2*T,25]);
    
    translate([0,-50,1.5])
    usb();
    translate([45,8,0])
    hook();
    translate([-45,8,0])
    hook();
    
    covermountminus();
}

difference() {
    union() {
translate([0,0,T]) {
translate([-L0/2-L0,offset,0])
waveshare();
translate([-L0/2,offset,0])
waveshare();
translate([L0/2,offset,0])
waveshare();
translate([L0/2+L0,offset,0])
waveshare();
}
}
translate([0,-50,0])
cube_center([11,100,100]);
}

translate([0,3.5,T])
tinypico();

translate([0,0,T])
covermount();

module covermount() {
translate([L2/2-5,W2/2-5,0])
standoff(h=H-8,od=9,id=6.5);
    translate([-L2/2+5,-W2/2+5,0])
standoff(h=H-8,od=9,id=6.5);
    translate([-L2/2+5,W2/2-5,0])
standoff(h=H-8,od=9,id=6.5);
    translate([L2/2-5,-W2/2+5,0])
standoff(h=H-8,od=9,id=6.5);
    
translate([L2/2-5,W2/2-5,H-8-1])
standoff(h=1,od=9,id=3);
    translate([-L2/2+5,-W2/2+5,H-8-1])
standoff(h=1,od=9,id=3);
    translate([-L2/2+5,W2/2-5,H-8-1])
standoff(h=1,od=9,id=3);
    translate([L2/2-5,-W2/2+5,H-8-1])
standoff(h=1,od=9,id=3);
}
module covermountminus() {
    translate([L2/2-5,W2/2-5,0])
    standoff(h=H,od=6.5,id=0);
    translate([-L2/2+5,-W2/2+5,0])
standoff(h=H,od=6.5,id=0);
    translate([-L2/2+5,W2/2-5,0])
standoff(h=H,od=6.5,id=0);
    translate([L2/2-5,-W2/2+5,0])
standoff(h=H,od=6.5,id=0);
}

module tinypico() {
    /*difference() {
    cube_center([17.5,33,0.4]);
    }*/
    translate([0,-4,0])
    difference() {
    union() {
    cube_center([29,27.5,2.8]);
    cube_center([29,25,3]);
    }
    cube_center([18,27.5,3]);
    }
    
    translate([0,-4,0])
    difference() {
        cube_center([29,31,4.5]);
        cube_center([29,27.5,6]);
        cube_center([18,33,6]);
    }
    
}


module hook() {
        rotate([0,0,-30])
    minkowski() {
        cylinder(d=6,h=10,$fn=3);
        cylinder(d=4,h=10,$fn=16);
    }
}

module usb() {
    cube_center([10.5,100,7]);
}

module waveshare() {
    difference() {
    cube_center([33,48,0.1]);
        translate([0,-3,0])
        cube_center([28,28,0.1]);
    }
translate([28/2,43/2,0])
standoff();
translate([-28/2,43/2,0])
standoff();
translate([28/2,-43/2,0])
standoff();
translate([-28/2,-43/2,0])
standoff();
}

module standoff(od=5.5,id=2,h=12 ) {
    difference() {
    cylinder(d=od,h=h,$fn=32);
    cylinder(d=id,h=h+0.001,$fn=16);
    }
}
module cube_center(dims) {
  translate([0,0,dims[2]/2])
    cube(dims,center=true);
}