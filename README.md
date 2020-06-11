# final-graphics

## Aditi Haiman (pd10)
## Project Title: Giraphics

Features implemented:
- Ellipsoid
    - "ellipsoid x y z rx ry rz" creates an ellipsoid with the given center point and x/y/z radii
- Pyramid
    - "pyramid x1 y1 z1 x2 y2 z2 w d" creates a pyramid with a point on the base, the top point, and width/depth of the base
- Cone
    - "cone x y z r h" creates a cone with the given center of the base, radius and height
- Cylinder
    - "cylinder x y z r h" creates a cylinder with the given center of the top face, radius and height
- Prism
    - "prism x y z r h side#" creates a prism with the given number of side faces
    - ex: "prism x y z r h 5" creates a pentagonal prism with (x, y, z) as the center and the given radius and height
- Tube
    - "tube x, y, z, r1, r2, h" creates a cylinder with radius r2, with a smaller cylinder cut out of it with radius r1



Proposal:

Features to implement:
-  New primitive shapes:
    - Change sphere to ellipsoid with x,y,z radii
        - ellipsoid x y z rx ry rz
    - Change circle to ellipse
        - circle x y z rx ry rz
    - cone 
        - cone x y z radius height
    - cylinder
        - cylinder x y z radius height
    - tube/pipe? (like cylinder but with hole in the middle)
        - tube x y z inner-radius outer-radius height
- Reflecting a shape across a line
    - reflect y slope intercept (ex: reflect y 5 -2 means to reflect over y = 5x-2)
    - reflect x y-val (to reflect over a vertical line)
- Changing vary? (linear, exponential, etc)
