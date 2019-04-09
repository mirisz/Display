import GeneralDisplay
import multiprocessing
import time
import copy

data_queue = multiprocessing.Queue()


def put_data():
    handover = {'passive':
                    {'stored_selection':
                         {'data': [{'name': 'Grid',
                                    'geom_type': 'grid',
                                    'coordinates': [[0, 0, 0]],
                                    'data': {'measurement_type': "axis",
                                    'measurement_scale': 10,
                                    'width': 600, 'height': 600},
                                    'color': [100, 100, 100]
                                    },
                                    {'name': 'Border',
                                     'geom_type': 'polyline',
                                     'coordinates': [[-100, -100, 0],
                                                    [100, -100, 0],
                                                    [100, 100, 0],
                                                    [-100, 100, 0],
                                                    [-100, -100, 0]],
                                     'data': {'width': 1.5, 'filled': False},
                                     'color': [100, 120, 100]
                                      }]
                         },
                         'config': {'delta_t': 0.02,
                                     'Logical_3D_view': False,
                                     'zoom': 1.1,
                                     'perspective': (80, 1, 0.1, 500),
                                     'canvas': (-100, 100, -100, 100)
                                    }
                    },
                'active': {'stored_selection': {'1.1': [{'id': 101,
                                                         'name': 'rectangle',
                                                         'geom_type': 'rectangle',
                                                         'coordinates': [[-95.0, -95.0, 0.0]],
                                                         'data': {'a': 10, 'b': 10, 'filled': True},
                                                         'color': [1, 120, 100]}
                                                        ]
                                                }
                           }
                }
    for k in range(3):
        for i in range(0, 191):
            handover['active']['stored_selection']['1.1'][0]['coordinates'] = [[-95.0 + i, -95.0 + i, 0.0]]
            handover['active']['stored_selection']['1.1'][0]['color'] = [255, 0, 0]
            data_queue.put(copy.deepcopy(handover))
        for j in range(190, -1, -1):
            handover['active']['stored_selection']['1.1'][0]['coordinates'] = [[-95.0 + j, -95.0 + j, 0.0]]
            handover['active']['stored_selection']['1.1'][0]['color'] = [0, 0, 255]
            data_queue.put(copy.deepcopy(handover))

if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=put_data())
    process_1.start()
    GeneralDisplay.main(data_queue)