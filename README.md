# parametric_stl Overview

This is an example project which looks at parameterizing and creating a 3D digital asset. The script takes in a UInt64 which is treated as a the dna representation of the 3D model. This 'dna' is split into sections which act as the gene definition. Each gene is normalized to determine how far a vertex should move from its baseline position. Then the vertex locations are modified based on the normalized values and a maximum perturbation value.

![data_flow](https://github.com/kingschmidty/parametric_stl/assets/138631273/d3c76de6-bf72-4197-b059-c73260ceeada)

In this example, there are seven parameters which modify mouth height, mouth width, inner eyebrow height, outer eyebrow height, nose length, nose width, and nose height. With these few degrees of freedom, you can create some interesting combinations.
![collage](https://github.com/kingschmidty/parametric_stl/assets/138631273/fe738694-272d-4f1a-8bc6-3e3c87640a9b)

After updating the vertex locations for the stl, the normals for some of the faces have changed. To account for this, the script loops through the effected faces, and performs the calculation to get the new normal direction. This requires performing a crossproduct and magnitude calculation. Then dividing the crossproduct by the magnitude, we receive the face normal. This is then converted to a string with 4 digits of precision. The strings are combined to a byte array representation, which will be used in Many of the functions in this section required using signed integers operations, and conversions to strings. I make no promises as to the correctness, generalizability, or efficiency of those subroutines.

Finally, the sizes of the header, modified faces section, and footer are used to create/resize a box. Then the byte arrays for the various sections are used to write into the box. I kept running into a bytearray length limit here, so that is why there are multiple Box Replace commands. Maybe I was just being dumb. I'm sure there is a better way of doing it.

At the end you have a nice new stl, in ascii format, stuffed in a box. What is pretty cool is that there are 2^28 different configurations that the stl could be. I haven't checked to see if any combinations create bad face combinations, such as colinear points.

## Getting Started

The code was developed using Algokit and the puya compiler. You can learn about algokit [here](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md). And you can learn about puya, [here](https://algorandfoundation.github.io/puya/language-guide.html). 

To get started fork the repo, and launch the workspace.

There should be a baseline teal in the artifacts folder, but if there is not you can compile yourself with the 'algokit project run build' command. After its compiled, you can deploy the contract with 'algokit run deploy'

The deploy script will deploy the contract and fund the contract account. Then it creates a random int below 2^64, and uses that to call the create_stl method. That method does all of the work to create the box containing the stl file. Next, the deploy script will query the box in the contract, and read its contents. Then the contents are written to file. This file will be called head.stl, and you can visualize the stl in a website such as [https://www.viewstl.com/](https://www.viewstl.com/) or with a python toolbox such as open3d.

### What's Next

This was a fun project for me. I learned a lot about the AVM. However, I am not a dev, and have a FT job, and have no real front-end abilities. In short, I don't have plans to productionize anything, so take anything and run with it.

If you would like to build on top of this example, here are some ideas you may consider trying out:
1) Adding more parameters
2) Utilizing a different baseline stl model
3) Adding a parent contract that randomizes the UInt64 creation
4) Adding a parent contract that breeds to UInt64s to create a new UInt representation (something like (dna_1 & rand_int) | (dna_2 & ~rand_int) should do it)
5) Buildin a workflow which reads the stl for usage in a gaming/rendering engine
