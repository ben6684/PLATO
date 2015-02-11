/*
   Based on PeasyCam by Jonathan Feinberg
   which is distributed under the Apache Public License, version 2.0 http://www.apache.org/licenses/LICENSE-2.0.html
   which there is a good chance I am not following
http://mrfeinberg.com/peasycam/
*/

function Camera()
{
    this.rot = quat4.create([0,0,0,1]);
    this.center = vec3.create([0,0,0]);
    this.distance = 10;
    this.velocityX = 0;
    this.velocityY = 0;
    this.velocityZ = 0;
    this.dampening = 0.84;
    this.startDistance = 10;
    this.minDistance = 1;
    this.drag = false;
}

vec3.angle = function(v1,v2) {
    return Math.acos(vec3.dot(v1,v2)/(vec3.length(v1)*vec3.length(v2)));
}

Camera.prototype.feed = function(mat) {
    this.step();
    var pos = [0,0,1];
    var up = [0,1,0];

    quat4.multiplyVec3(this.rot,pos);
    vec3.scale(pos,this.distance);
    vec3.add(pos, this.center);
    quat4.multiplyVec3(this.rot, up);
    mat4.multiply(mat, mat4.lookAt(pos,this.center,up));
}

Camera.prototype.mouseDragged = function(dx,dy,mx,my,button) {
    if(button == 1) {
        this.mouseRotate(dx,dy,mx,my);
    } else if(button == 2) {
        this.mousePan(dx,dy);
    }
}

Camera.prototype.mouseWheel = function(dy) {
    this.mouseZoom(-dy);
}

Camera.prototype.mousePan = function(dx,dy) {
    var panScale = Math.sqrt(this.distance *0.0001);
    this.pan(-dx*panScale, -dy*panScale);
}

Camera.prototype.pan = function(dx,dy) {
    vec3.add(this.center,quat4.multiplyVec3(this.rot,[dx,dy,0]));
}

Camera.prototype.mouseRotate = function(dx,dy,mx,my) {
    if(!this.drag)
    {
        this.velocityX = 0;
        this.velocityY = 0;
        this.velocityZ = 0;
        this.drag = true;
    }
    var u = [0,0,-100*.6*this.startDistance]; //this.distance?
    var rho = Math.abs((gl.viewportWidth / 2.0) - mx) / (gl.viewportWidth/2.0);
    //console.log(rho, u);
    var adz = Math.abs(dy) * rho;
    var ady = Math.abs(dy) * (1 - rho);
    var ySign = dy < 0 ? -1 : 1;
    var vy = [0,0,0];
    vec3.add(u,[0,ady,0],vy);
    this.velocityX += vec3.angle(u,vy)*ySign;
    var vz = [0,0,0];
    vec3.add(u,[0,adz,0],vz);
    this.velocityZ += vec3.angle(u, vz) * -ySign
        * (mx < gl.viewportWidth / 2 ? -1 : 1);
    var eccentricity = Math.abs((gl.viewportHeight / 2.0) - my)
        / (gl.viewportHeight / 2.0);
    var xSign = dx > 0 ? -1 : 1;
    adz = Math.abs(dx) * eccentricity;
    var adx = Math.abs(dx) * (1 - eccentricity);
    var vx = [0,0,0]
        vec3.add(u,[adx, 0, 0],vx);
    this.velocityY += vec3.angle(u,vx)*xSign;
    vec3.add(u,[0,adz,0],vz);
    this.velocityZ += vec3.angle(u,vz)*xSign
        * (my > gl.viewportHeight / 2 ? -1 : 1);
}

Camera.prototype.mouseZoom = function(delta) {
    this.distance = Math.max(this.minDistance, this.distance - delta * Math.sqrt(this.distance * .02));
}

Camera.prototype.step = function() {
     //if(Math.abs(this.velocityX)<0.03)
        this.velocityX *= this.dampening;
     //if(Math.abs(this.velocityY)<0.03)
       this.velocityY *= this.dampening;
     //if(Math.abs(this.velocityZ)<0.03)
       this.velocityZ *= this.dampening;
    if(Math.abs(this.velocityX) < 0.001) this.velocityX = 0;
    if(Math.abs(this.velocityY) < 0.001) this.velocityY = 0;
    if(Math.abs(this.velocityZ) < 0.001) this.velocityZ = 0;
    //is create necessary? Also is w first or last
    if(this.velocityX != 0) quat4.multiply(this.rot,quat4.create([Math.sin(this.velocityX/2.0),0,0,Math.cos(this.velocityX/2.0)]));
    if(this.velocityY != 0) quat4.multiply(this.rot,quat4.create([0,Math.sin(this.velocityY/2.0),0,Math.cos(this.velocityY/2.0)]));
    if(this.velocityZ != 0) quat4.multiply(this.rot,quat4.create([0,0,Math.sin(this.velocityZ/2.0),Math.cos(this.velocityZ/2.0)]));
}
