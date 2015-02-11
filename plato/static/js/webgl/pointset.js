function PointSet(pos, n)
{
    this.length = pos.length/3;
    this.pos = new Float32Array(pos);

    this.center = vec3.create([0,0,0]);
    for(var i=0; i<this.length; i++)
    {
        this.center[0] += this.pos[3*i];
        this.center[1] += this.pos[3*i+1];
        this.center[2] += this.pos[3*i+2];
    }
    vec3.scale(this.center, 1/this.length);

    var rm = 0;
    for(var i=0; i<this.length; i++)
    {
        var mx = this.center[0] - pos[i*3];
        var my = this.center[1] - pos[i*3+1];
        var mz = this.center[2] - pos[i*3+2];
        rm += Math.sqrt(mx*mx + my*my + mz*mz);
    }
    rm /= this.pos.length;

    for(var i=0; i<this.pos.length/3; i++)
    {
        this.pos[3*i] -= this.center[0];
        this.pos[3*i+1] -= this.center[1];
        this.pos[3*i+2] -= this.center[2];
        this.pos[3*i] /= rm;
        this.pos[3*i+1] /= rm;
        this.pos[3*i+2] /= rm;
    }
    this.hasN = false;
    if(n.length)
    {
        this.n = new Float32Array(n);
        this.hasN = true;
    }
    // this.color = new Float32Array(size);
    this.hasColor = false;
}

PointSet.prototype.size = function()
{
    return this.length;
}

// -----------------------------------------

function Triangles(ind)
{
    this.length = ind.length;
    this.ind = new Uint16Array(ind);
}

Triangles.prototype.size = function()
{
    return this.length;
}

// -----------------------------------------

// -----------------------------------------

function Mesh(vertices, triangles, trianglesIndex)
{
    this.vertices = vertices;
    this.triangles = triangles;

    this.vertexPositionBuffer;
    this.vertexNormalBuffer;
    this.vertexColorBuffer;
    this.vertexIndexBuffer;



    // Copy positions
    this.vertexPositionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexPositionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.vertices.pos), gl.STATIC_DRAW);
    this.vertexPositionBuffer.itemSize = 3;
    this.vertexPositionBuffer.numItems = vertices.size();

    // Copy normales
    if(this.vertices.hasN)
    {
        this.vertexNormalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexNormalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.vertices.n), gl.STATIC_DRAW);
        this.vertexNormalBuffer.itemSize = 3;
        this.vertexNormalBuffer.numItems = vertices.size();
    }
    // XXX

    this.n = new Float32Array(3*this.triangles.length);
    this.pos = new Float32Array(3*this.triangles.length);
    this.vertexTrianglesPositionBuffer;
    this.vertexTrianglesNormalBuffer;

    if(trianglesIndex)
    {
        for(var i=0; i<trianglesIndex.length; i++)
        {
            var ind = trianglesIndex[i];
            this.pos[3*i] = this.vertices.pos[3*ind];
            this.n[3*i] = this.vertices.n[3*ind];
            this.pos[3*i+1] = this.vertices.pos[3*ind+1];
            this.n[3*i+1] = this.vertices.n[3*ind+1];
            this.pos[3*i+2] = this.vertices.pos[3*ind+2];
            this.n[3*i+2] = this.vertices.n[3*ind+2];
        }
        this.vertexTrianglesPositionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexTrianglesPositionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.pos), gl.STATIC_DRAW);
        this.vertexTrianglesPositionBuffer.itemSize = 3;
        this.vertexTrianglesPositionBuffer.numItems = trianglesIndex.length;

        this.vertexTrianglesNormalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexTrianglesNormalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.n), gl.STATIC_DRAW);
        this.vertexTrianglesNormalBuffer.itemSize = 3;
        this.vertexTrianglesNormalBuffer.numItems = trianglesIndex.length;
    }
    else
    {
        for(var i=0; i<triangles.length; i++)
        {
            var ind = triangles.ind[i];
            this.pos[3*i] = this.vertices.pos[3*ind];
            this.n[3*i] = this.vertices.n[3*ind];
            this.pos[3*i+1] = this.vertices.pos[3*ind+1];
            this.n[3*i+1] = this.vertices.n[3*ind+1];
            this.pos[3*i+2] = this.vertices.pos[3*ind+2];
            this.n[3*i+2] = this.vertices.n[3*ind+2];
        }
        this.vertexTrianglesPositionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexTrianglesPositionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.pos), gl.STATIC_DRAW);
        this.vertexTrianglesPositionBuffer.itemSize = 3;
        this.vertexTrianglesPositionBuffer.numItems = triangles.length;

        this.vertexTrianglesNormalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertexTrianglesNormalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.n), gl.STATIC_DRAW);
        this.vertexTrianglesNormalBuffer.itemSize = 3;
        this.vertexTrianglesNormalBuffer.numItems = triangles.length;
    }

    // XXX

    // Copy triangles
    this.vertexIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.vertexIndexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(this.triangles.ind), gl.STATIC_DRAW);
    this.vertexIndexBuffer.itemSize = 1;
    this.vertexIndexBuffer.numItems = this.triangles.size();

    this.positionBuffer = function()
    {
        return this.vertexPositionBuffer;
    }

    this.normalBuffer = function()
    {
        return this.vertexNormalBuffer;
    }

    this.indexBuffer = function()
    {
        return this.vertexIndexBuffer;
    }

}

function loadPlyFile(data)
{
    var vertexSize = 0;
    var triangleSize = 0;
    var hasNormal = false;
    var hasEndHeader = false;

    var lignes = data.split(/\n/);

    // Lecture Header
    var i;
    for (i = 0; l = lignes[i]; ++i)
    {
        var mots = l.split(/\s/);
        if(mots[0] == "comment") continue;
        else if(mots[0] == "element")
        {
            if(mots[1] == "vertex")
            {
                vertexSize = parseInt(mots[2]);
            }
            else if(mots[1] == "face")
            {
                triangleSize = parseInt(mots[2]);
            }
        }
        else if(mots[0] == "property")
        {
            if(mots[2] == "nx")
            {
                hasNormal = true;
            }
        }
        else if(mots[0] == "end_header")
        {
            hasEndHeader = true;
            ++i;
            break;
        }
        console.log(mots[0]);
    }
    if(!hasEndHeader)
    {
        alert(".ply file doesn't have a correct header ");
    }

    console.log(triangleSize);
    var vertexPos = new Float32Array(3*vertexSize);
    var vertexN = new Float32Array(hasNormal ? 3*vertexSize:0);
    for(var v = 0 ; v < vertexSize && (l = lignes[i]); ++v,++i)
    {
        var mots = l.split(/\s/);
        vertexPos[3*v] = parseFloat(mots[0])*2;
        vertexPos[3*v + 1] = parseFloat(mots[1])*2;
        vertexPos[3*v + 2] = parseFloat(mots[2])*2;
        if(hasNormal)
        {
            vertexN[3*v] = parseFloat(mots[3]);
            vertexN[3*v + 1] = parseFloat(mots[4]);
            vertexN[3*v + 2] = parseFloat(mots[5]);
        }
    }
    var trianglesIndex = new Uint32Array(3*triangleSize);
    var triangles = new Uint16Array(3*triangleSize);
    for(var t = 0 ; t < triangleSize && (l = lignes[i]); ++t, ++i)
    {
        var mots = l.split(/\s/);
        trianglesIndex[t*3] = parseInt(mots[1]);
        trianglesIndex[t*3+1] = parseInt(mots[2]);
        trianglesIndex[t*3+2] = parseInt(mots[3]);
        triangles[t*3] = parseInt(mots[1]);
        triangles[t*3+1] = parseInt(mots[2]);
        triangles[t*3+2] = parseInt(mots[3]);
    }
    mesh = new Mesh (new PointSet(vertexPos, vertexN)
            ,new Triangles(triangles), trianglesIndex);
}

function loadOffFile(data)
{

    var vertexSize = 0;
    var triangleSize = 0;
    var hasNormal = false;
    var hasEndHeader = false;

    var lignes = data.split(/\n/);
    // Lecture Header
    var i;
    for (i = 1; l = lignes[i]; ++i) //the first line is Always "OFF"
    {
        var mots = l.split(/\s/);

		if(mots[0] == "#")
		{
			continue;
		}
		else
		{
			vertexSize = parseInt(mots[0]);
			triangleSize = parseInt(mots[1]);
			++i;
			break;
        }
        console.log(mots[0]);
    }
    console.log(triangleSize);
	alert(vertexSize+" "+triangleSize)
    var vertexPos = new Float32Array(3*vertexSize);
    var vertexN = new Float32Array(hasNormal ? 3*vertexSize:0);
    for(var v = 0 ; v < vertexSize && (l = lignes[i]); ++v,++i)
    {
        var mots = l.split(/\s/);
        vertexPos[3*v] = parseFloat(mots[0])*2;
        vertexPos[3*v + 1] = parseFloat(mots[1])*2;
        vertexPos[3*v + 2] = parseFloat(mots[2])*2;
        if(hasNormal)
        {
            vertexN[3*v] = parseFloat(mots[3]);
            vertexN[3*v + 1] = parseFloat(mots[4]);
            vertexN[3*v + 2] = parseFloat(mots[5]);
        }
    }
	alert(vertexPos[3]+" "+hasNormal)
    var trianglesIndex = new Uint32Array(3*triangleSize);
    var triangles = new Uint16Array(3*triangleSize);
    for(var t = 0 ; t < triangleSize && (l = lignes[i]); ++t, ++i)
    {
        var mots = l.split(/\s/);
        trianglesIndex[t*3] = parseInt(mots[1]);
        trianglesIndex[t*3+1] = parseInt(mots[2]);
        trianglesIndex[t*3+2] = parseInt(mots[3]);
        triangles[t*3] = parseInt(mots[1]);
        triangles[t*3+1] = parseInt(mots[2]);
        triangles[t*3+2] = parseInt(mots[3]);
    }
	alert("plop"+vertexPos[0]+" "+triangles[0])
    mesh = new Mesh (new PointSet(vertexPos, vertexN)
            ,new Triangles(triangles), trianglesIndex);


}




Mesh.loadCube = function()
{
    vertices = [
        // Front face
        -1.0, -1.0,  1.0,
        1.0, -1.0,  1.0,
        1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,

        // Back face
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        1.0,  1.0, -1.0,
        1.0, -1.0, -1.0,

        // Top face
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        1.0,  1.0,  1.0,
        1.0,  1.0, -1.0,

        // Bottom face
        -1.0, -1.0, -1.0,
        1.0, -1.0, -1.0,
        1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        // Right face
        1.0, -1.0, -1.0,
        1.0,  1.0, -1.0,
        1.0,  1.0,  1.0,
        1.0, -1.0,  1.0,

        // Left face
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,
        ];
    var vertexNormals = [
        // Front face
        0.0,  0.0,  1.0,
        0.0,  0.0,  1.0,
        0.0,  0.0,  1.0,
        0.0,  0.0,  1.0,

        // Back face
        0.0,  0.0, -1.0,
        0.0,  0.0, -1.0,
        0.0,  0.0, -1.0,
        0.0,  0.0, -1.0,

        // Top face
        0.0,  1.0,  0.0,
        0.0,  1.0,  0.0,
        0.0,  1.0,  0.0,
        0.0,  1.0,  0.0,

        // Bottom face
        0.0, -1.0,  0.0,
        0.0, -1.0,  0.0,
        0.0, -1.0,  0.0,
        0.0, -1.0,  0.0,

        // Right face
        1.0,  0.0,  0.0,
        1.0,  0.0,  0.0,
        1.0,  0.0,  0.0,
        1.0,  0.0,  0.0,

        // Left face
        -1.0,  0.0,  0.0,
        -1.0,  0.0,  0.0,
        -1.0,  0.0,  0.0,
        -1.0,  0.0,  0.0
            ];
    var vertexIndices = [
        0, 1, 2,      0, 2, 3,    // Front face
        4, 5, 6,      4, 6, 7,    // Back face
        8, 9, 10,     8, 10, 11,  // Top face
        12, 13, 14,   12, 14, 15, // Bottom face
        16, 17, 18,   16, 18, 19, // Right face
        20, 21, 22,   20, 22, 23  // Left face
            ];

    return new Mesh (new PointSet(vertices, vertexNormals)
            ,new Triangles(vertexIndices));

}
