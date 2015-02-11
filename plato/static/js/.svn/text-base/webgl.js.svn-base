var gl;

function initGL(canvas) {
    try {
        gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl",{preserveDrawingBuffer: true});
        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
        alert("Unable to initialize WebGL. Your browser may not support it :-(");
    }
}



function getShader(gl, id) {
    var shaderScript = document.getElementById(id);
    if (!shaderScript) {
        return null;
    }

    var str = "";
    var k = shaderScript.firstChild;
    while (k) {
        if (k.nodeType == 3) {
            str += k.textContent;
        }
        k = k.nextSibling;
    }

    var shader;
    if (shaderScript.type == "x-shader/x-fragment") {
        shader = gl.createShader(gl.FRAGMENT_SHADER);
    } else if (shaderScript.type == "x-shader/x-vertex") {
        shader = gl.createShader(gl.VERTEX_SHADER);
    } else {
        return null;
    }

    gl.shaderSource(shader, str);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert(gl.getShaderInfoLog(shader));
        return null;
    }

    return shader;
}


var shaderProgram;

function initShaders() {
    var fragmentShader = getShader(gl, "shader-fs");
    var vertexShader = getShader(gl, "shader-vs");

    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

	// If creating the shader program failed, alert

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert("Could not initialise shaders");
    }

    gl.useProgram(shaderProgram);

    shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
    gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

    shaderProgram.vertexNormalAttribute = gl.getAttribLocation(shaderProgram, "aVertexNormal");
    gl.enableVertexAttribArray(shaderProgram.vertexNormalAttribute);

    //shaderProgram.textureCoordAttribute = gl.getAttribLocation(shaderProgram, "aTextureCoord");
    //gl.enableVertexAttribArray(shaderProgram.textureCoordAttribute);

    shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
    shaderProgram.nMatrixUniform = gl.getUniformLocation(shaderProgram, "uNMatrix");
    //shaderProgram.samplerUniform = gl.getUniformLocation(shaderProgram, "uSampler");
    shaderProgram.useLightingUniform = gl.getUniformLocation(shaderProgram, "uUseLighting");
    shaderProgram.useTexturingUniform = gl.getUniformLocation(shaderProgram, "uUseTexturing");
    shaderProgram.usePointSet = gl.getUniformLocation(shaderProgram, "uPointSet");
    shaderProgram.useSmoothedPoint = gl.getUniformLocation(shaderProgram, "uSmoothedPoint");
    shaderProgram.ambientColorUniform = gl.getUniformLocation(shaderProgram, "uAmbientColor");
    shaderProgram.lightingDirectionUniform2 = gl.getUniformLocation(shaderProgram, "uLightingDirection2");
    shaderProgram.directionalColorUniform2 = gl.getUniformLocation(shaderProgram, "uDirectionalColor2");
    shaderProgram.lightingDirectionUniform = gl.getUniformLocation(shaderProgram, "uLightingDirection");
    shaderProgram.directionalColorUniform = gl.getUniformLocation(shaderProgram, "uDirectionalColor");
    shaderProgram.alphaUniform = gl.getUniformLocation(shaderProgram, "uAlpha");
    shaderProgram.pointSize = gl.getUniformLocation(shaderProgram, "uPointSize");
}

/*function handleLoadedTexture(texture) {
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);

    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texture.image);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    gl.generateMipmap(gl.TEXTURE_2D);

    gl.bindTexture(gl.TEXTURE_2D, null);
}

var glassTexture;

function initTexture() {
    glassTexture = gl.createTexture();
    glassTexture.image = new Image();
    glassTexture.image.onload = function () {
        handleLoadedTexture(glassTexture)
    }

    glassTexture.image.src = "texture/glass.gif";
}*/

var mvMatrix = mat4.create();
var mvMatrixStack = [];
var pMatrix = mat4.create();

/*function mvPushMatrix() {
    var copy = mat4.create();
    mat4.set(mvMatrix, copy);
    mvMatrixStack.push(copy);
}

function mvPopMatrix() {
    if (mvMatrixStack.length == 0) {
        throw "Invalid popMatrix!";
    }
    mvMatrix = mvMatrixStack.pop();
}*/


function setMatrixUniforms() {
    gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, pMatrix);
    gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);

    var normalMatrix = mat3.create();
    mat4.toInverseMat3(mvMatrix, normalMatrix);
    mat3.transpose(normalMatrix);
    gl.uniformMatrix3fv(shaderProgram.nMatrixUniform, false, normalMatrix);
}


/*function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

var xRot = 0;
var xSpeed = 0;

var yRot = 0;
var ySpeed = 0;

var z = -5.0;

var filter = 0;


var currentlyPressedKeys = {};

function handleKeyDown(event) {
    // Empeche d'executer l'evenement par defaut par exemple descrendre la page
    // quand on tape sur la fleche du bas
    if(event.keyCode == 38 || event.keyCode == 40 || event.keyCode == 34 || event.keyCode == 33)
    {
        event.preventDefault();
    }
    currentlyPressedKeys[event.keyCode] = true;

    if (String.fromCharCode(event.keyCode) == "F") {
        filter += 1;
        if (filter == 3) {
            filter = 0;
        }
    }
}


function handleKeyUp(event) {
    currentlyPressedKeys[event.keyCode] = false;
}


function handleKeys() {
    if (currentlyPressedKeys[33]) {
        // Page Up
        z -= 0.05;
        currentlyPressedKeys[33] = false;
    }
    if (currentlyPressedKeys[34]) {
        // Page Down
        z += 0.05;
        currentlyPressedKeys[34] = false;
    }
    if (currentlyPressedKeys[37]) {
        // Left cursor key
        ySpeed -= 10;
        currentlyPressedKeys[37] = false;
    }
    if (currentlyPressedKeys[39]) {
        // Right cursor key
        ySpeed += 10;
        currentlyPressedKeys[39] = false;
    }
    if (currentlyPressedKeys[38]) {
        // Up cursor key
        xSpeed -= 10;
        currentlyPressedKeys[38] = false;
    }
    if (currentlyPressedKeys[40]) {
        // Down cursor key
        xSpeed += 10;
        currentlyPressedKeys[40] = false;
    }
}

var cubeVertexTextureCoordBuffer;*/

var mesh;

function initBuffers() {
    mesh = Mesh.loadCube();
}

/*var xRot = 0;
var yRot = 0;
var zRot = 0;*/

var camera = new Camera();
function initMouseEvents(canvas)
{
    canvas.addEventListener("mouseup",mouseUpMan,false);

    canvas.addEventListener("DOMMouseScroll",wheel,false);
	canvas.addEventListener ("mousewheel", wheel, false);

    canvas.addEventListener("mousemove",mouseMoveMan,false);
    canvas.addEventListener("mousedown",mouseDownMan,false);
    //canvas.addEventListener("contextmenu",contextMenu,false);
    document.addEventListener("mousedown",function() {isMouseDown = true;},false);
    document.addEventListener("mouseup",function() {isMouseDown = false;mouseDragging = false;},false);
}

var pmouseX, pmouseY, mouseX, mouseY;
var mouseDragging = false;
var mouseButton = -1;
var isMouseDown = false;

function wheel(event) {
	if('wheelDelta' in event){
		camera.mouseWheel(-event.wheelDelta/40);
	}
	else{ //firefox
		camera.mouseWheel(event.detail);
	}
	if (event.preventDefault)
        event.preventDefault();
	event.returnValue = false;
}

function mouseUpMan(event) {
    isMouseDown = false;
    camera.drag = false;
}

function mouseMoveMan(event) {
    pmouseX = mouseX;
    pmouseY = mouseY;
    mouseX = event.clientX;
    mouseY = event.clientY;
    if(isMouseDown) {
        mouseDragging = true;
        mouseDraggedMan(event);
    }
}

function mouseDownMan(event) {
    isMouseDown = true;
    mouseDragging = false;
    mouseButton = event.which;
}

function inside2DGUI(x,y){
    if(x> draw2Dx && x<(draw2Dx+draw2DWidth+40)) {
        if(y> draw2Dy && y<(draw2Dy+draw2DHeight)) return true;
        else return false;
    }
    else return false;
}

function mouseDownManPJS(event) {
    if(event.clientX>300 && !inside2DGUI(event.clientX,event.clientY)) {
        mouseDownMan(event);
    }
}

function mouseMoveManPJS(event) {
    if(event.clientX>300 && !inside2DGUI(event.clientX,event.clientY)) {
        mouseMoveMan(event);
    }
}

function mouseUpManPJS(event) {
    if(event.clientX>300 && !inside2DGUI(event.clientX,event.clientY)) {
        mouseUpMan(event);
    }
}

function mouseDraggedMan(event) {
    camera.mouseDragged(mouseX-pmouseX,-(mouseY-pmouseY), mouseX, mouseY,mouseButton);
}

function contextMenu(event) {
    event.preventDefault();
    event.stopPropagation();
}

function drawScene() {

    // var canvas = document.getElementById("viewer-canvas");
    // gl.viewportWidth = canvas.width;
    // gl.viewportHeight = canvas.height;

    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    mat4.perspective(45, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0, pMatrix);

    mat4.identity(mvMatrix);
    camera.feed(mvMatrix);
    if(document.getElementById("pointSet").checked)
    {
        gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vertexPositionBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, mesh.vertexPositionBuffer.itemSize, gl.FLOAT, false, 0, 0);
        if(mesh.vertices.hasN)
        {
            gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vertexNormalBuffer);
            gl.vertexAttribPointer(shaderProgram.vertexNormalAttribute, mesh.vertexNormalBuffer.itemSize, gl.FLOAT, false, 0, 0);
        }
    }
    else
    {
        gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vertexTrianglesPositionBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, mesh.vertexTrianglesPositionBuffer.itemSize, gl.FLOAT, false, 0, 0);
        if(mesh.vertices.hasN)
        {
            gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vertexTrianglesNormalBuffer);
            gl.vertexAttribPointer(shaderProgram.vertexNormalAttribute, mesh.vertexTrianglesNormalBuffer.itemSize, gl.FLOAT, false, 0, 0);
        }
    }
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

    gl.activeTexture(gl.TEXTURE0);

    /*gl.bindBuffer(gl.ARRAY_BUFFER, cubeVertexTextureCoordBuffer);
      gl.vertexAttribPointer(shaderProgram.textureCoordAttribute, cubeVertexTextureCoordBuffer.itemSize, gl.FLOAT, false, 0, 0);

      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, glassTexture);
      gl.uniform1i(shaderProgram.samplerUniform, 0);*/

///////////////////Modif petitpas => because i don't have this features => add in the futur ! //////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // var texturing = document.getElementById("texturing").checked;
    gl.uniform1i(shaderProgram.useTexturingUniform, false);

    gl.uniform1i(shaderProgram.usePointSet, true);
    gl.uniform1i(shaderProgram.useSmoothedPoint, false);

    // var blending = document.getElementById("blending").checked;
    // if (blending) {
    //     gl.enable(gl.BLEND);
    //     gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
    //     gl.disable(gl.DEPTH_TEST);
    //     gl.uniform1f(shaderProgram.alphaUniform, parseFloat(document.getElementById("alpha").value));
    // } else {
    //     gl.disable(gl.BLEND);
    //     gl.enable(gl.DEPTH_TEST);
    // }

    gl.uniform1f(shaderProgram.pointSize, parseFloat(document.getElementById("pointSize").value));

	///////////// added by petitpas ////////////////
	//gl.uniform1f(shaderProgram.pointSize, 1.0);
	////////////////////////////

    // var lighting = document.getElementById("lighting").checked;
    gl.uniform1i(shaderProgram.useLightingUniform, true);
    // if (lighting) {
    //     gl.uniform3f(
    //             shaderProgram.ambientColorUniform,
    //             parseFloat(document.getElementById("ambientR").value),
    //             parseFloat(document.getElementById("ambientG").value),
    //             parseFloat(document.getElementById("ambientB").value)
    //             );

    //     var lightingDirection = [
    //         parseFloat(document.getElementById("lightDirectionX").value),
    //         parseFloat(document.getElementById("lightDirectionY").value),
    //         parseFloat(document.getElementById("lightDirectionZ").value)
    //             ];
    //     var adjustedLD = vec3.create();
    //     vec3.normalize(lightingDirection, adjustedLD);
    //     vec3.scale(adjustedLD, -1);
    //     gl.uniform3fv(shaderProgram.lightingDirectionUniform, adjustedLD);

    //     var lightingDirection1 = [-473, 351, 259];
    //     var adjustedLD1 = vec3.create();
    //     vec3.normalize(lightingDirection1, adjustedLD1);
    //     vec3.scale(adjustedLD1, -1);
    //     gl.uniform3fv(shaderProgram.lightingDirectionUniform2, adjustedLD1);

    //     gl.uniform3f(shaderProgram.directionalColorUniform2, 0.28, 0.39, 1.0 ,1.0);

    //     gl.uniform3f(
    //             shaderProgram.directionalColorUniform,
    //             parseFloat(document.getElementById("directionalR").value),
    //             parseFloat(document.getElementById("directionalG").value),
    //             parseFloat(document.getElementById("directionalB").value)
    //             );
    // }
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mesh.vertexIndexBuffer);
    setMatrixUniforms();

    if(document.getElementById("pointSet").checked)
    {
        gl.drawArrays(gl.POINTS, 0, mesh.vertexPositionBuffer.numItems);
    }
    else
    {
        gl.drawArrays(gl.TRIANGLES, 0, mesh.vertexTrianglesPositionBuffer.numItems, gl.UNSIGNED_SHORT, 0);
    }

}

/*var lastTime = 0;

function animate() {
    var timeNow = new Date().getTime();
    if (lastTime != 0) {
        var elapsed = timeNow - lastTime;

        xRot += (xSpeed * elapsed) / 1000.0;
        yRot += (ySpeed * elapsed) / 1000.0;
    }
    lastTime = timeNow;
}*/

var canvas;

function tick() {
    updateGL(document.getElementById("viewer-canvas"));
    requestAnimFrame(tick);
    // handleKeys();
    drawScene();
    // animate();
}

function webGLStart() {
    canvas = document.getElementById("viewer-canvas");
    canvas.height = 600;//window.innerHeight;
    canvas.style.height = 600;//window.innerHeight;
    canvas.width = 800;//window.innerWidth;
    canvas.style.width = 800;//window.innerWidth;

    initGL(canvas);
    initMouseEvents(canvas);
    initShaders();
    initBuffers();
    //initTexture();

    // 0 en alpha permet de faire de sauvegarde sans fond
    gl.clearColor(0.2, 0.2, 0.2, 0.0);
    gl.enable(gl.DEPTH_TEST);

    //document.onkeydown = handleKeyDown;
    //document.onkeyup = handleKeyUp;

    tick();
}

function updateGL(canvas) {
    canvas.height = 600;//window.innerHeight;
    canvas.style.height = 600;//window.innerHeight;
    canvas.width = 800;//window.innerWidth;
    canvas.style.width = 800;//window.innerWidth;
    // canvas.style.height = window.innerHeight;
    // canvas.height = window.innerHeight;
    // canvas.style.width = window.innerWidth;
    // canvas.width = window.innerWidth;
    try {

        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
    } catch (e) {
    }
    if (!gl) {
        alert("Could not initialise WebGL, sorry :-(");
    }
}

