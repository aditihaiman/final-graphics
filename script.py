import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  Should set num_frames and basename if the frames
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):

    frameCheck = varyCheck = nameCheck = False
    name = ''
    num_frames = 1

    for command in commands:

        if command['op'] == 'frames':
            num_frames = int(command['args'][0])
            frameCheck = True
        elif command['op'] == 'vary':
            varyCheck = True
        elif command['op'] == 'basename':
            name = command['args'][0]
            nameCheck = True

    if varyCheck and not frameCheck:
        print('Error: Vary command found without setting number of frames!')
        exit()

    elif frameCheck and not nameCheck:
        print('Animation code present but basename was not set. Using "frame" as basename.')
        name = 'frame'

    return (name, num_frames)

"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    frames = [ {} for i in range(num_frames) ]

    for command in commands:
        if command['op'] == 'vary':
            args = command['args']
            knob_name = command['knob']
            start_frame = args[0]
            end_frame = args[1]
            start_value = float(args[2])
            end_value = float(args[3])
            value = 0

            if ((start_frame < 0) or
                (end_frame >= num_frames) or
                (end_frame <= start_frame)):
                print('Invalid vary command for knob: ' + knob_name)
                exit()

            delta = (end_value - start_value) / (end_frame - start_frame)

            for f in range(num_frames):
                if f == start_frame:
                    value = start_value
                    frames[f][knob_name] = value
                elif f >= start_frame and f <= end_frame:
                    value = start_value + delta * (f - start_frame)
                    frames[f][knob_name] = value
                #print 'knob: ' + knob_name + '\tvalue: ' + str(frames[f][knob_name])
    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames)

    for f in range(num_frames):
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []


        #Set symbol values for multiple frames
        if num_frames > 1:
            frame = frames[f]
            for knob in frame:
                symbols[knob][1] = frame[knob]
                print('\tkob: ' + knob + '\tvalue: ' + str(frame[knob]))

        for command in commands:
            #print(command)
            c = command['op']
            args = command['args']
            knob_value = 1

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'cone':
                if command['constants']:
                    reflect = command['constants']
                add_cone(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'tube':
                if command['constants']:
                    reflect = command['constants']
                add_tube(tmp, args[0], args[1], args[2], args[3], args[4], args[5], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'prism':
                if command['constants']:
                    reflect = command['constants']
                add_prism(tmp, args[0], args[1], args[2], args[3], args[4], args[5], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'cylinder':
                if command['constants']:
                    reflect = command['constants']
                add_cylinder(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'pyramid':
                if command['constants']:
                    reflect = command['constants']
                add_pyramid(tmp, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
            elif c == 'ellipsoid':
                if command['constants']:
                    reflect = command['constants']
                #print("A", args)
                add_ellipsoid(tmp,
                           args[0], args[1], args[2], args[3], args[4], args[5], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                #print("A", args)
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if command['knob']:
                    knob_value = symbols[command['knob']][1]
                tmp = make_translate(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if command['knob']:
                    knob_value = symbols[command['knob']][1]
                tmp = make_scale(args[0] * knob_value, args[1] * knob_value, args[2] * knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                if command['knob']:
                    knob_value = symbols[command['knob']][1]
                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
            # end operation loop
        if num_frames > 1:
            fname = 'anim/%s%03d.png'%(name, f)
            print('Saving frame: '  + fname)
            save_extension(screen, fname)
        # end fromes loop
    if num_frames > 1:
        make_animation(name)


"""Shape commands:
    1. box x y z w h d
        (x, y, z) is the coordinate of top left front corner
        (w, h, d) is in (x, y, z) dimension
        
    2. cone x y z r h
        (x, y, z) is center of base
        (r, h) is radius of base and height of cone
        
    3. tube x y z r1 r2 h
        (x, y, z) is center of top face
        r1 is inner radius
        r2 is outer radius
        h is height of tube
        r1 must be < r2 to get a proper looking tube
  
    4. prism x y z r h f
        (x, y, z) is the center of the top face
        (r, h) is radius and height
        f is the number of faces (ex: f = 5 is a pentagonal prism)
  
    5. cylinder x y z r h
        (x, y, z) is center of top face
        (r, h) is radius and height
  
    6. pyramid x1 y1 z1 x2 y2 z2 w d
        (x1, y1, z1) is the top of the pyramid
        (x2, y2, z2) is the front left corner of the base
        (w, d) are width and depth of the base in (x, z) dimensions
  
    7. ellipsoid x y z rx ry rz
        (x, y, z) is the center
        rx, ry, rz are radii in each direction
  
    8. sphere x y z r
        (x, y, z) is center of the sphere
        r is the radius
  
    9. torus x y z r R
        (x, y, z) is the center of the torus
        r is the radius of the circular cross-section
        R is the distance from torus center to center of circular cross-section
"""
