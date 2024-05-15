from algopy import ARC4Contract, arc4, Bytes, String, subroutine, UInt64, urange, ensure_budget, OpUpFeeSource, BytesBacked, op, gtxn, itxn, Global
import typing as t


vector: t.TypeAlias = arc4.StaticArray[arc4.UInt64, t.Literal[3]] # (x,y,z) vector, treating the arc4.UInts as signed ints
vector_str: t.TypeAlias = arc4.StaticArray[arc4.String, t.Literal[3]] # (x,y,z) vector of strings
face: t.TypeAlias = arc4.StaticArray[vector, t.Literal[3]]

num_points = 31
num_faces = 58

points: t.TypeAlias = arc4.StaticArray[vector, t.Literal[31]]
points_str: t.TypeAlias = arc4.StaticArray[arc4.String, t.Literal[93]]
faces: t.TypeAlias = arc4.StaticArray[vector, t.Literal[58]]

num_parameters = 12

parameter: t.TypeAlias = arc4.StaticArray[arc4.UInt64, t.Literal[5]] # pointId, coordId (x,y,z), max change, index_1, index_2
parameterization: t.TypeAlias = arc4.StaticArray[parameter, t.Literal[12]]


class ParametricSTL(ARC4Contract):
    @arc4.abimethod()
    def create_stl(self, dna:arc4.UInt64) -> arc4.String:
        
        # making sure there is enough juicy juicy opcode budget
        ensure_budget(700*128, OpUpFeeSource.AppAccount)
        
        # generating a header and footer of faces which are unchanged by the parameterization
        header = String('solid Prop\nfacet normal -0 -0 -1\nouter loop\nvertex 0 0 0\nvertex 0 1000 0\nvertex 1000 0 0\nendloop\nendfacet\nfacet normal 0 0 -1\nouter loop\nvertex 0 1000 0\nvertex 1000 1000 0\nvertex 1000 0 0\nendloop\nendfacet\nfacet normal -1 -0 -0\nouter loop\nvertex 0 0 0\nvertex 0 0 1000\nvertex 0 1000 0\nendloop\nendfacet\nfacet normal -1 0 0\nouter loop\nvertex 0 0 1000\nvertex 0 1000 1000\nvertex 0 1000 0\nendloop\nendfacet\nfacet normal -0 -1 -0\nouter loop\nvertex 0 0 0\nvertex 1000 0 0\nvertex 1000 0 1000\nendloop\nendfacet\nfacet normal 0 -1 -0\nouter loop\nvertex 0 0 0\nvertex 1000 0 1000\nvertex 0 0 1000\nendloop\nendfacet\nfacet normal -0 0 1\nouter loop\nvertex 0 0 1000\nvertex 1000 1000 1000\nvertex 0 1000 1000\nendloop\nendfacet\nfacet normal 0 0 1\nouter loop\nvertex 0 0 1000\nvertex 1000 0 1000\nvertex 1000 1000 1000\nendloop\nendfacet\nfacet normal 0 1 0\nouter loop\nvertex 0 1000 0\nvertex 0 1000 1000\nvertex 1000 1000 1000\nendloop\nendfacet\nfacet normal 0 1 0\nouter loop\nvertex 1000 1000 1000\nvertex 1000 1000 0\nvertex 0 1000 0\nendloop\nendfacet\n')
        footer = String('facet normal 0.8944 -0.4472 0\nouter loop\nvertex 1000 0 0\nvertex 1050 100 500\nvertex 1000 0 1000\nendloop\nendfacet\nfacet normal 0.8944 0.4472 0\nouter loop\nvertex 1000 1000 0\nvertex 1000 1000 1000\nvertex 1050 900 500\nendloop\nendfacet\nfacet normal 0.4472 0 0.8944\nouter loop\nvertex 1000 0 1000\nvertex 1100 500 950\nvertex 1000 1000 1000\nendloop\nendfacet\nfacet normal 0.8944 0 -0.4472\nouter loop\nvertex 1000 0 0\nvertex 1000 1000 0\nvertex 1050 500 100\nendloop\nendfacet\nfacet normal 0.8944 -0.4472 0\nouter loop\nvertex 1000 0 1000\nvertex 1050 100 500\nvertex 1080 160 750\nendloop\nendfacet\nfacet normal 0.8944 0.4472 0\nouter loop\nvertex 1080 840 750\nvertex 1050 900 500\nvertex 1000 1000 1000\nendloop\nendfacet\nfacet normal 0.9592 -0.0400 -0.2798\nouter loop\nvertex 1000 0 0\nvertex 1050 500 100\nvertex 1050 150 150\nendloop\nendfacet\nfacet normal 0.9592 0.0400 -0.2798\nouter loop\nvertex 1000 1000 0\nvertex 1050 850 150\nvertex 1050 500 100\nendloop\nendfacet\nfacet normal 0.9592 -0.2798 -0.0400\nouter loop\nvertex 1000 0 0\nvertex 1050 150 150\nvertex 1050 100 500\nendloop\nendfacet\nfacet normal 0.9592 0.2798 -0.0400\nouter loop\nvertex 1050 850 150\nvertex 1000 1000 0\nvertex 1050 900 500\nendloop\nendfacet\nendsolid Prop\n')

        # generating the baseline design using Strings
        p_str:points_str
        p_str = points_str(arc4.String("0"), arc4.String("0"), arc4.String("0"),
                   arc4.String("0"), arc4.String("0"), arc4.String("1000"),
                   arc4.String("0"), arc4.String("1000"), arc4.String("0"),
                   arc4.String("0"), arc4.String("1000"), arc4.String("1000"),
                   arc4.String("1000"), arc4.String("0"), arc4.String("0"),
                   arc4.String("1000"), arc4.String("0"), arc4.String("1000"),
                   arc4.String("1000"), arc4.String("1000"), arc4.String("0"),
                   arc4.String("1000"), arc4.String("1000"), arc4.String("1000"),
                   arc4.String("1100"), arc4.String("500"), arc4.String("650"),
                   arc4.String("1160"), arc4.String("500"), arc4.String("470"),
                   arc4.String("1100"), arc4.String("350"), arc4.String("450"),
                   arc4.String("1100"), arc4.String("650"), arc4.String("450"),
                   arc4.String("1100"), arc4.String("500"), arc4.String("250"),
                   arc4.String("1100"), arc4.String("200"), arc4.String("230"),
                   arc4.String("1100"), arc4.String("800"), arc4.String("230"),
                   arc4.String("1130"), arc4.String("400"), arc4.String("840"),
                   arc4.String("1110"), arc4.String("200"), arc4.String("850"),
                   arc4.String("1080"), arc4.String("305"), arc4.String("700"),
                   arc4.String("1130"), arc4.String("600"), arc4.String("840"),
                   arc4.String("1110"), arc4.String("800"), arc4.String("850"),
                   arc4.String("1080"), arc4.String("695"), arc4.String("700"),
                   arc4.String("1100"), arc4.String("275"), arc4.String("560"),
                   arc4.String("1050"), arc4.String("100"), arc4.String("500"),
                   arc4.String("1100"), arc4.String("725"), arc4.String("460"),
                   arc4.String("1050"), arc4.String("900"), arc4.String("500"),
                   arc4.String("1100"), arc4.String("500"), arc4.String("950"),
                   arc4.String("1050"), arc4.String("500"), arc4.String("100"),
                   arc4.String("1080"), arc4.String("160"), arc4.String("750"),
                   arc4.String("1080"), arc4.String("840"), arc4.String("750"),
                   arc4.String("1050"), arc4.String("150"), arc4.String("150"),
                   arc4.String("1050"), arc4.String("850"), arc4.String("150"))

        # generating the baseline design using UInt64s
        p:points
        p = points(vector(arc4.UInt64(0), arc4.UInt64(0), arc4.UInt64(0)),
                   vector(arc4.UInt64(0), arc4.UInt64(0), arc4.UInt64(1000)),
                   vector(arc4.UInt64(0), arc4.UInt64(1000), arc4.UInt64(0)),
                   vector(arc4.UInt64(0), arc4.UInt64(1000), arc4.UInt64(1000)),
                   vector(arc4.UInt64(1000), arc4.UInt64(0), arc4.UInt64(0)),
                   vector(arc4.UInt64(1000), arc4.UInt64(0), arc4.UInt64(1000)),
                   vector(arc4.UInt64(1000), arc4.UInt64(1000), arc4.UInt64(0)),
                   vector(arc4.UInt64(1000), arc4.UInt64(1000), arc4.UInt64(1000)),
                   vector(arc4.UInt64(1100), arc4.UInt64(500), arc4.UInt64(650)),
                   vector(arc4.UInt64(1160), arc4.UInt64(500), arc4.UInt64(470)),
                   vector(arc4.UInt64(1100), arc4.UInt64(350), arc4.UInt64(450)),
                   vector(arc4.UInt64(1100), arc4.UInt64(650), arc4.UInt64(450)),
                   vector(arc4.UInt64(1100), arc4.UInt64(500), arc4.UInt64(250)),
                   vector(arc4.UInt64(1100), arc4.UInt64(200), arc4.UInt64(230)),
                   vector(arc4.UInt64(1100), arc4.UInt64(800), arc4.UInt64(230)),
                   vector(arc4.UInt64(1130), arc4.UInt64(400), arc4.UInt64(840)),
                   vector(arc4.UInt64(1110), arc4.UInt64(200), arc4.UInt64(850)),
                   vector(arc4.UInt64(1080), arc4.UInt64(305), arc4.UInt64(700)),
                   vector(arc4.UInt64(1130), arc4.UInt64(600), arc4.UInt64(840)),
                   vector(arc4.UInt64(1110), arc4.UInt64(800), arc4.UInt64(850)),
                   vector(arc4.UInt64(1080), arc4.UInt64(695), arc4.UInt64(700)),
                   vector(arc4.UInt64(1100), arc4.UInt64(275), arc4.UInt64(560)),
                   vector(arc4.UInt64(1050), arc4.UInt64(100), arc4.UInt64(500)),
                   vector(arc4.UInt64(1100), arc4.UInt64(725), arc4.UInt64(460)),
                   vector(arc4.UInt64(1050), arc4.UInt64(900), arc4.UInt64(500)),
                   vector(arc4.UInt64(1100), arc4.UInt64(500), arc4.UInt64(950)),
                   vector(arc4.UInt64(1050), arc4.UInt64(500), arc4.UInt64(100)),
                   vector(arc4.UInt64(1080), arc4.UInt64(160), arc4.UInt64(750)),
                   vector(arc4.UInt64(1080), arc4.UInt64(840), arc4.UInt64(750)),
                   vector(arc4.UInt64(1050), arc4.UInt64(150), arc4.UInt64(150)),
                   vector(arc4.UInt64(1050), arc4.UInt64(850), arc4.UInt64(150)))

        # defining all of the parametric modifications, looking at node, axis, max displacement, and start and end of dna
        parm = parameterization(parameter(arc4.UInt64(13), arc4.UInt64(2), arc4.UInt64(90), arc4.UInt64(0), arc4.UInt64(3)),
                                parameter(arc4.UInt64(14), arc4.UInt64(2), arc4.UInt64(90), arc4.UInt64(0), arc4.UInt64(3)),
                                parameter(arc4.UInt64(13), arc4.UInt64(1), arc4.UInt64(140), arc4.UInt64(4), arc4.UInt64(7)),
                                parameter(arc4.UInt64(14), arc4.UInt64(1), arc4.UInt64(self.subtract(UInt64(0),UInt64(140))), arc4.UInt64(4), arc4.UInt64(7)),
                                parameter(arc4.UInt64(15), arc4.UInt64(2), arc4.UInt64(40), arc4.UInt64(8), arc4.UInt64(11)),
                                parameter(arc4.UInt64(18), arc4.UInt64(2), arc4.UInt64(40), arc4.UInt64(8), arc4.UInt64(11)),
                                parameter(arc4.UInt64(16), arc4.UInt64(2), arc4.UInt64(30), arc4.UInt64(12), arc4.UInt64(15)),
                                parameter(arc4.UInt64(19), arc4.UInt64(2), arc4.UInt64(30), arc4.UInt64(12), arc4.UInt64(15)),
                                parameter(arc4.UInt64(9), arc4.UInt64(0), arc4.UInt64(140), arc4.UInt64(16), arc4.UInt64(19)),
                                parameter(arc4.UInt64(10), arc4.UInt64(1), arc4.UInt64(90), arc4.UInt64(20), arc4.UInt64(23)),
                                parameter(arc4.UInt64(11), arc4.UInt64(1), arc4.UInt64(self.subtract(UInt64(0),UInt64(90))), arc4.UInt64(20), arc4.UInt64(23)),
                                parameter(arc4.UInt64(8), arc4.UInt64(2), arc4.UInt64(100), arc4.UInt64(24), arc4.UInt64(27)))

        # Looping through the parameters to modify the vertex locations in both string and UInt definitions
        temp:UInt64
        for i in urange(parm.length):
            temp = self.add(p[parm[i][0].native][parm[i][1].native].native,self.getParm(dna, parameter.from_bytes(parm[i].bytes)).native)
            p_str[parm[i][0].native*3 + parm[i][1].native] = arc4.String(self.str(temp))
            p[parm[i][0].native][parm[i][1].native] = arc4.UInt64(temp)

        # Defining the vertices that compose each of the faces
        f:faces
        f=faces(vector(arc4.UInt64(0), arc4.UInt64(2), arc4.UInt64(4)), #0
                vector(arc4.UInt64(2), arc4.UInt64(6), arc4.UInt64(4)),
                vector(arc4.UInt64(0), arc4.UInt64(1), arc4.UInt64(2)),
                vector(arc4.UInt64(1), arc4.UInt64(3), arc4.UInt64(2)),
                vector(arc4.UInt64(0), arc4.UInt64(4), arc4.UInt64(5)),
                vector(arc4.UInt64(0), arc4.UInt64(5), arc4.UInt64(1)),
                vector(arc4.UInt64(1), arc4.UInt64(7), arc4.UInt64(3)),
                vector(arc4.UInt64(1), arc4.UInt64(5), arc4.UInt64(7)),
                vector(arc4.UInt64(2), arc4.UInt64(3), arc4.UInt64(7)),
                vector(arc4.UInt64(7), arc4.UInt64(6), arc4.UInt64(2)),
                vector(arc4.UInt64(8), arc4.UInt64(10), arc4.UInt64(9)), #10 first outside of header
                vector(arc4.UInt64(8), arc4.UInt64(9), arc4.UInt64(11)),
                vector(arc4.UInt64(9), arc4.UInt64(10), arc4.UInt64(11)),
                vector(arc4.UInt64(11), arc4.UInt64(10), arc4.UInt64(12)),
                vector(arc4.UInt64(10), arc4.UInt64(13), arc4.UInt64(12)),
                vector(arc4.UInt64(11), arc4.UInt64(12), arc4.UInt64(14)),
                vector(arc4.UInt64(17), arc4.UInt64(15), arc4.UInt64(16)),
                vector(arc4.UInt64(20), arc4.UInt64(19), arc4.UInt64(18)),
                vector(arc4.UInt64(8), arc4.UInt64(18), arc4.UInt64(15)),
                vector(arc4.UInt64(8), arc4.UInt64(17), arc4.UInt64(10)),
                vector(arc4.UInt64(8), arc4.UInt64(11), arc4.UInt64(20)), #20
                vector(arc4.UInt64(8), arc4.UInt64(15), arc4.UInt64(17)),
                vector(arc4.UInt64(8), arc4.UInt64(20), arc4.UInt64(18)),
                vector(arc4.UInt64(10), arc4.UInt64(17), arc4.UInt64(21)),
                vector(arc4.UInt64(21), arc4.UInt64(17), arc4.UInt64(22)),
                vector(arc4.UInt64(13), arc4.UInt64(21), arc4.UInt64(22)),
                vector(arc4.UInt64(10), arc4.UInt64(21), arc4.UInt64(13)),
                vector(arc4.UInt64(16), arc4.UInt64(5), arc4.UInt64(27)),
                vector(arc4.UInt64(27), arc4.UInt64(17), arc4.UInt64(16)),
                vector(arc4.UInt64(22), arc4.UInt64(17), arc4.UInt64(27)),
                vector(arc4.UInt64(5), arc4.UInt64(16), arc4.UInt64(15)), #30
                vector(arc4.UInt64(5), arc4.UInt64(15), arc4.UInt64(25)),
                vector(arc4.UInt64(11), arc4.UInt64(23), arc4.UInt64(20)),
                vector(arc4.UInt64(11), arc4.UInt64(14), arc4.UInt64(23)),
                vector(arc4.UInt64(20), arc4.UInt64(23), arc4.UInt64(24)),
                vector(arc4.UInt64(23), arc4.UInt64(14), arc4.UInt64(24)),
                vector(arc4.UInt64(20), arc4.UInt64(24), arc4.UInt64(28)),
                vector(arc4.UInt64(19), arc4.UInt64(20), arc4.UInt64(28)),
                vector(arc4.UInt64(19), arc4.UInt64(28), arc4.UInt64(7)),
                vector(arc4.UInt64(7), arc4.UInt64(18), arc4.UInt64(19)),
                vector(arc4.UInt64(7), arc4.UInt64(25), arc4.UInt64(18)), #40
                vector(arc4.UInt64(25), arc4.UInt64(15), arc4.UInt64(18)),
                vector(arc4.UInt64(12), arc4.UInt64(13), arc4.UInt64(26)),
                vector(arc4.UInt64(12), arc4.UInt64(26), arc4.UInt64(14)),
                vector(arc4.UInt64(13), arc4.UInt64(29), arc4.UInt64(26)),
                vector(arc4.UInt64(14), arc4.UInt64(26), arc4.UInt64(30)),
                vector(arc4.UInt64(13), arc4.UInt64(22), arc4.UInt64(29)),
                vector(arc4.UInt64(14), arc4.UInt64(30), arc4.UInt64(24)),
                vector(arc4.UInt64(4), arc4.UInt64(22), arc4.UInt64(5)), # footer begins here
                vector(arc4.UInt64(6), arc4.UInt64(7), arc4.UInt64(24)), #50
                vector(arc4.UInt64(5), arc4.UInt64(25), arc4.UInt64(7)),
                vector(arc4.UInt64(4), arc4.UInt64(6), arc4.UInt64(26)),
                vector(arc4.UInt64(5), arc4.UInt64(22), arc4.UInt64(27)),
                vector(arc4.UInt64(28), arc4.UInt64(24), arc4.UInt64(7)),
                vector(arc4.UInt64(4), arc4.UInt64(26), arc4.UInt64(29)),
                vector(arc4.UInt64(6), arc4.UInt64(30), arc4.UInt64(26)),
                vector(arc4.UInt64(4), arc4.UInt64(29), arc4.UInt64(22)),
                vector(arc4.UInt64(30), arc4.UInt64(6), arc4.UInt64(24)))

        # looping through all of the faces which are changing, to calculate the updated normals and create a string for that face.
        n:vector_str
        section_1=String('')
        section_2=String('')
        for i in urange(10,49):
            n = self.normal(face(vector.from_bytes(p[f[i][0].native].bytes), vector.from_bytes(p[f[i][1].native].bytes), vector.from_bytes(p[f[i][2].native].bytes)))
            if i< 35:
                section_1=section_1 + String('facet normal ') + n[0].native + String(' ') + n[1].native + String(' ') + n[2].native + String('\nouter loop\n')
                section_1=section_1 + String('vertex ') + p_str[f[i][0].native*3].native + String(' ') + p_str[f[i][0].native*3+1].native + String(' ') + p_str[f[i][0].native*3+2].native + String('\n')
                section_1=section_1 + String('vertex ') + p_str[f[i][1].native*3].native + String(' ') + p_str[f[i][1].native*3+1].native + String(' ') + p_str[f[i][1].native*3+2].native + String('\n')
                section_1=section_1 + String('vertex ') + p_str[f[i][2].native*3].native + String(' ') + p_str[f[i][2].native*3+1].native + String(' ') + p_str[f[i][2].native*3+2].native + String('\nendloop\nendfacet\n')
            else:
                section_2=section_2 + String('facet normal ') + n[0].native + String(' ') + n[1].native + String(' ') + n[2].native + String('\nouter loop\n')
                section_2=section_2 + String('vertex ') + p_str[f[i][0].native*3].native + String(' ') + p_str[f[i][0].native*3+1].native + String(' ') + p_str[f[i][0].native*3+2].native + String('\n')
                section_2=section_2 + String('vertex ') + p_str[f[i][1].native*3].native + String(' ') + p_str[f[i][1].native*3+1].native + String(' ') + p_str[f[i][1].native*3+2].native + String('\n')
                section_2=section_2 + String('vertex ') + p_str[f[i][2].native*3].native + String(' ') + p_str[f[i][2].native*3+1].native + String(' ') + p_str[f[i][2].native*3+2].native + String('\nendloop\nendfacet\n')
        
        # reading the total size of the various strings as bytes, creating a box, and stuffing them in it
        total_size = header.bytes.length + section_1.bytes.length + section_2.bytes.length + footer.bytes.length

        # checking if a box exists and if so deleting it. I think I could resize it, but this is what I found works.
        
        if op.Box.create(String('stl').bytes, total_size):
            return_string = arc4.String('Box was not found, so one was created')
        else:
            op.Box.resize(String('stl').bytes, total_size)
            return_string = arc4.String('Existing box was found and resized')
        
        op.Box.replace(String('stl').bytes, 0, (header.bytes))
        op.Box.replace(String('stl').bytes, header.bytes.length, section_1.bytes)
        op.Box.replace(String('stl').bytes, (header.bytes.length + section_1.bytes.length), section_2.bytes)
        op.Box.replace(String('stl').bytes, (header.bytes.length + section_1.bytes.length + section_2.bytes.length), footer.bytes)

        return return_string

    @subroutine
    def str_neg(self, i:UInt64) -> String:
        # getting the string representation of a number signed integer
        if i >> 63:
            return String('-') + self.str(~i)
        else:
            return self.str(i)
    
    @subroutine
    def str_dec(self, i:UInt64) -> String:
        # getting the string representation of a number bounded between -1 and 1 and has 5 decimals of precision
        if i >> 63:
            if ~i//10000:
                return String('-1')
            else:
                return String('-0.') + self.str_5_digits(~i)
        else:
            if i//10000:
                return String('1')
            else:
                return String('0.') + self.str_5_digits(i)
    
    @subroutine
    def str_5_digits(self, dec:UInt64) -> String:
        # getting a representation of the 5 digits of a decimal
        temp:String
        temp=String('')
        for i in urange(0,4):
            temp = String.from_bytes(arc4.UInt64((dec % (UInt64(10)) + UInt64(48))).bytes[7]) + temp
            dec = dec//10
        return temp

    @subroutine
    def str(self, i:UInt64) -> String:
        # getting the string representation of a positive integer
        if i==UInt64(0):
            return String('')
        else:
            if (i // UInt64(10) > UInt64(0)):
                return self.str(i // UInt64(10)) + String.from_bytes(arc4.UInt64(i % UInt64(10) + UInt64(48)).bytes[7])
            else:
                return String.from_bytes(arc4.UInt64(i % UInt64(10) + UInt64(48)).bytes[7])


    @subroutine
    def getParm(self, value:arc4.UInt64, p:parameter) -> arc4.UInt64:
        # getting the vertex displacement for a given parameter
        max_value = p[2]
        ind_1 = p[3]
        ind_2 = p[4]
        temp:UInt64
        temp=value.native
        temp = temp % (2**ind_2.native)
        temp >>= ind_1.native
        if max_value.native>>63:
            return arc4.UInt64(~((~max_value.native) * temp // (2**(ind_2.native-ind_1.native)-1)))
        else:
            return arc4.UInt64(max_value.native * temp // (2**(ind_2.native-ind_1.native)-1))

    @subroutine
    def subtract(self, a:UInt64, b:UInt64) -> UInt64:
        # subtraction for two signed integers
        if b>a:
            return ~(b-a)
        else:
            return a-b
    
    @subroutine
    def add(self, a:UInt64, b:UInt64) -> UInt64:
        # getting the addition of two signed integers
        if b>>63:
            if self.abs(b)>self.abs(a) and a>>63==UInt64(0):
                return ~(self.abs(b)-a)
            else:
                return a-self.abs(b)
        else:
            if self.abs(b)>self.abs(a) and a>>63==UInt64(1):
                return b-self.abs(a)
            else:
                return a+b

    @subroutine
    def multiply(self, a:UInt64, b:UInt64) -> UInt64:
        # getting the multiple of two signed integers
        if a >> 63 == b >> 63:
            return self.abs(a)*self.abs(b)
        else:
            return ~(self.abs(a)*self.abs(b))
    
    @subroutine
    def divide(self, a:UInt64, b:UInt64) -> UInt64:
        # dividing integers a and b, assuming b is positive, though a can be positive or negative
        if a >> 63:
            return ~(self.abs(a)//b)
        else:
            return a//b

    @subroutine
    def negCheck(self, a:UInt64) -> bool:
        # checking is a signed integer is positive or negative
        if a >> 63:
            return True
        else:
            return False
        
    @subroutine
    def abs(self, a:UInt64) -> UInt64:
        # returns the absolute value of a
        if a >> 63:
            return ~a
        else:
            return a
    
    @subroutine
    def normal(self, f:face) -> vector_str:
        # takes a face definition, performs a cross product and normalizes based on the magnitude
        # returns a vector string using four digits of precision
        u = vector(arc4.UInt64(self.subtract(f[1][0].native, f[0][0].native)),arc4.UInt64(self.subtract(f[1][1].native, f[0][1].native)),arc4.UInt64(self.subtract(f[1][2].native, f[0][2].native)))
        v = vector(arc4.UInt64(self.subtract(f[2][0].native, f[0][0].native)),arc4.UInt64(self.subtract(f[2][1].native, f[0][1].native)),arc4.UInt64(self.subtract(f[2][2].native, f[0][2].native)))
        n = self.crossproduct(u, v)
        mag = self.magnitude(n)
        #normal_str = vector_str(arc4.String(self.str_5_digits(n[0].native*10000//mag)), arc4.String(self.str_5_digits(n[1].native*10000//mag)), arc4.String(self.str_5_digits(n[2].native*10000//mag)))
        return vector_str(arc4.String(self.str_dec(self.divide(self.multiply(n[0].native,UInt64(10000)),mag))), arc4.String(self.str_dec(self.divide(self.multiply(n[1].native,UInt64(10000)),mag))), arc4.String(self.str_dec(self.divide(self.multiply(n[2].native,UInt64(10000)),mag))))
    
    @subroutine
    def crossproduct(self, u:vector, v:vector) -> vector:
        # returns a vector which is the cross product of two input vectors, u and v
        return vector(arc4.UInt64(self.subtract(self.multiply(u[1].native,v[2].native), self.multiply(u[2].native,v[1].native))), arc4.UInt64(self.subtract(self.multiply(u[2].native,v[0].native), self.multiply(u[0].native,v[2].native))), arc4.UInt64(self.subtract(self.multiply(u[0].native,v[1].native), self.multiply(u[1].native,v[0].native))))

    @subroutine
    def magnitude(self, a:vector) -> UInt64:
        # returns the magnitude of an input vector, a 
        return op.sqrt(self.abs(a[0].native)**2 + self.abs(a[1].native)**2 + self.abs(a[2].native)**2)

    
    #@subroutine
    #def normalize(self, a:vector) -> vector_str:
#
    #    return vector_str(arc4.String(self.str_neg(a[0].native)),arc4.String(self.str_neg(a[1].native)),arc4.String(self.str_neg(a[2].native)))
