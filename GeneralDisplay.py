import time
from GeneralBaseClasses import *
from OpenGL.GLU import *

INIT = True
SKIP_VIEWP = False
screenWidth = 600
screenHeight = 600
t0 = 0
ACTIVE = []
QUEUE = None
PASSIVE = []
CONFIG = {'screen_width': 600, 'screen_height': 600, 'screen_color': [0.0, 0.0, 0.0], 'delta_t': 1,
          'canvas': (-650, 650, -650, 650), 'zoom': 1, 'Logical_3D_view': False,
          'light': [[[20, -20, 20, 1], [1.0, 1.0, 1.0, 1.0]]]}  # {
          # 'Logical_3D_view': True, 'perspective': (62, 1, 0.1, 500),
          # 'lookat': (40.0, -20.0, 42.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)}


def on_init(queue):
    global QUEUE
    QUEUE = queue


def check_name_in_list_of_objects(attr_name, obj_list):
    if len(obj_list) == 0:
        return False
    for o in obj_list:
        if o.id == attr_name:
            return True
    return False


def get_index_of_object_from_list_by_name(attr_name, obj_list):
    if len(obj_list) == 0:
        return False
    for o in obj_list:
        if o.id == attr_name:
            return obj_list.index(o)
    return None


def create_init_dict(object_data_dict):
    init = {}
    if 'name' not in object_data_dict:
        print('No name for object!!!!!')
        return {}
    init['id'] = object_data_dict['name']
    if 'color' in object_data_dict:
        init['color'] = color_factory(object_data_dict['color'])
    if 'coordinates' in object_data_dict:
        if object_data_dict['geom_type'] == 'polyline':
            init['coordinates'] = vector_factory(object_data_dict['coordinates'])
        elif object_data_dict['geom_type'] == 'triangleset':
            init['coordinates'] = create_vectors_for_triangleset(object_data_dict['coordinates'])
        else:
            if len(object_data_dict['coordinates']) == 1:
                init['coordinates'] = vector_from_list(object_data_dict['coordinates'][0])
    if 'measurement_scale' in object_data_dict['data']:
        init['scale'] = object_data_dict['data']['measurement_scale']
    if 'measurement_type' in object_data_dict['data']:
        init['type'] = object_data_dict['data']['measurement_type']
    if 'width' in object_data_dict['data']:
        init['width'] = object_data_dict['data']['width']
    if 'height' in object_data_dict['data']:
        init['height'] = object_data_dict['data']['height']
    if 'filled' in object_data_dict['data']:
        init['filled'] = object_data_dict['data']['filled']
    if 'a' in object_data_dict['data']:
        init['a'] = object_data_dict['data']['a']
    if 'b' in object_data_dict['data']:
        init['b'] = object_data_dict['data']['b']
    if 'side' in object_data_dict['data']:
        init['side'] = object_data_dict['data']['side']
    if 'rotate' in object_data_dict['data']:
        init['rotate'] = object_data_dict['data']['rotate']
    if 'radius' in object_data_dict['data']:
        init['radius'] = object_data_dict['data']['radius']
    return init


def factory(object_data_dict):
    """
    Instantiate a class from parameters
    :param object_data_dict:
    :return:
    """
    obj = None

    if object_data_dict['geom_type'] == 'grid':
        obj = Grid(zoom=CONFIG['zoom'])
    elif object_data_dict['geom_type'] == 'polyline':
        obj = Polyline()
        obj.from_dict(create_init_dict(object_data_dict))
    elif object_data_dict['geom_type'] == 'rectangle':
        obj = Rectangle()
        obj.from_dict(create_init_dict(object_data_dict))
    elif object_data_dict['geom_type'] == 'cube':
        obj = Cube()
    elif object_data_dict['geom_type'] == 'sphere':
        obj = Sphere()
    elif object_data_dict['geom_type'] == 'triangleset':
        obj = TriangleSet()
    else:
        print('No match for geom_type!')
        return

    obj.from_dict(create_init_dict(object_data_dict))
    return obj


def draw(passive, active):
    """
    :param passive:
    :param active:
    :return:
    """
    # Grid is under construction
    # g = Grid(scale=CONFIG['measurement_scale'], type=CONFIG['measurement_type'])
    # g.draw()
    if len(passive) > 0:
        for p in passive:
            p.draw()

    if len(active) > 0:
        for a in active:
            a.draw()


def draw3d(passive, active):
    """
    :param passive, active:
    :return:
    """

    if len(passive) > 0:
        for p in passive:
            if hasattr(p, "draw3d"):
                p.draw3d()
            else:
                p.draw()

    if len(active) > 0:
        for a in active:
            if hasattr(a, "draw3d"):
                a.draw3d()
            else:
                a.draw()


def process_queue_element():
    """

    :param:
    :return:
    """
    global CONFIG, PASSIVE, ACTIVE, SKIP_VIEWP
    for p in PASSIVE:
        if isinstance(p, Grid):
            if p.type == 'axis':
                p.zoom = CONFIG['zoom']
    if QUEUE.qsize() > 0:
        temp_dict = QUEUE.get()
        if 'passive' in temp_dict:
            # update config dict
            if 'config' in temp_dict['passive']:
                if ('screen_width' or 'screen_height') in temp_dict['passive']['config']:
                    if temp_dict['passive']['config']['screen_width'] != CONFIG['screen_width'] or \
                    temp_dict['passive']['config']['screen_height'] != CONFIG['screen_height']:
                        SKIP_VIEWP = True
                for k, v in temp_dict['passive']['config'].items():
                    CONFIG[k] = v
            # update passive
            for i in temp_dict['passive']['stored_selection']['data']:
                if check_name_in_list_of_objects(i['name'], PASSIVE):
                    del PASSIVE[get_index_of_object_from_list_by_name(i['name'], PASSIVE)]
                PASSIVE.append(factory(i))
        # update active
        ACTIVE = []
        if 'active' in temp_dict:
            for ids in temp_dict['active']['stored_selection'].values():
                for i in ids:
                    ACTIVE.append(factory(i))
    return PASSIVE, ACTIVE


def display():
    """

    :return:
    """
    global INIT, SKIP_VIEWP
    glClearColor(CONFIG['screen_color'][0], CONFIG['screen_color'][1], CONFIG['screen_color'][2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # If queue is empty at the beginning
    if QUEUE.empty() and (len(ACTIVE) == 0 or len(PASSIVE) == 0):
        return
    passive, active = process_queue_element()
    if CONFIG['Logical_3D_view']:
        if INIT:
            INIT = False
            glViewport(0, 0, CONFIG['screen_width'],  CONFIG['screen_height'])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(*CONFIG['perspective'])
        gluLookAt(*CONFIG['lookat'])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, CONFIG['light'][0][0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, CONFIG['light'][0][1])
        draw3d(passive, active)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
    else:
        glutReshapeWindow(CONFIG['screen_width'], CONFIG['screen_height'])
        if SKIP_VIEWP:
            SKIP_VIEWP = False
        else:
            glViewport(0, 0, CONFIG['screen_width'], CONFIG['screen_height'])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        z = CONFIG['zoom']
        c = CONFIG['canvas']
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(c[0]*z, c[1]*z, c[2]*z, c[3]*z)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        draw(passive, active)
    glutSwapBuffers()


def on_mousewheel(button, direction, x, y):
    global CONFIG
    step = 0.1
    if direction > 0:
        CONFIG['zoom'] += step
    else:
        CONFIG['zoom'] -= step
    glutPostRedisplay()


def on_keyboard(key, x, y):
    global CONFIG
    if not CONFIG['Logical_3D_view']:
        step = (CONFIG['canvas'][1] - CONFIG['canvas'][0]) / 100
        if key == str.encode('w'):
            CONFIG['canvas'] = (CONFIG['canvas'][0], CONFIG['canvas'][1], CONFIG['canvas'][2]+step,
                                CONFIG['canvas'][3]+step)
        if key == str.encode('s'):
            CONFIG['canvas'] = (CONFIG['canvas'][0], CONFIG['canvas'][1], CONFIG['canvas'][2]-step,
                                CONFIG['canvas'][3]-step)
        if key == str.encode('d'):
            CONFIG['canvas'] = (CONFIG['canvas'][0]+step, CONFIG['canvas'][1]+step, CONFIG['canvas'][2],
                                CONFIG['canvas'][3])
        if key == str.encode('a'):
            CONFIG['canvas'] = (CONFIG['canvas'][0]-step, CONFIG['canvas'][1]-step, CONFIG['canvas'][2],
                                CONFIG['canvas'][3])
        glutPostRedisplay()


def on_idle():
    """
    :return:
    """
    global t0
    t = glutGet(GLUT_ELAPSED_TIME)
    time.sleep(CONFIG['delta_t'])
    t0 = t
    glutPostRedisplay()


def main(queue):
    """

    :param queue:
    :return:
    """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(CONFIG['screen_width'], CONFIG['screen_height'])
    glutCreateWindow(b"Display")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    on_init(queue)
    glutDisplayFunc(display)
    glutKeyboardFunc(on_keyboard)
    glutMouseWheelFunc(on_mousewheel)
    glutIdleFunc(on_idle)
    glutMainLoop()
