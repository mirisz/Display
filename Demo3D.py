import GeneralDisplay
import multiprocessing


data_queue = multiprocessing.Queue()


def put_data():
    handover = {'passive': {'stored_selection': {'data': [
                                                          {'name': 'Border',
                                                           'geom_type': 'polyline',
                                                           'coordinates': [[-100, -100, 0],
                                                                           [100, -100, 0],
                                                                           [100, 100, 0],
                                                                           [-100, 100, 0],
                                                                           [-100, -100, 0]],
                                                           'data': {'width': 1.5, 'filled': True},
                                                           'color': [255, 255, 255]
                                                           }
                                                          ]
                                                 },
                            'config': {'delta_t': 1,
                                       'Logical_3D_view': True,
                                       'zoom': 0.8,
                                       'perspective': (80, 1, 0.1, 500),
                                       'lookat': (0.0, 100.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
                                       'canvas': (-80, 80, -80, 80),
                                       'light': [[[-20, 120, 120, 1], [1.0, 1.0, 1.0, 1.0]]]
                                       }
                            },
                'active': {'HighestFitness': 0.97,
                           'stored_selection': {'36.41': [{'name': 'Building_A',
                                                           'geom_type': 'cube',
                                                           'coordinates': [[0.0, 0.0, 0.0]],
                                                           'data': {'side': [5, 5, 5], 'filled': True},
                                                           'color': [1, 120, 100]
                                                           },
                                                          {'name': 'Building_B',
                                                           'geom_type': 'cube',
                                                           'coordinates': [[74.5, 57.0, 0.0]],
                                                           'data': {'side': [5, 5, 5], 'filled': True},
                                                           'color': [100, 120, 100]
                                                           }
                                                          ],
                                                '36.45': [{'name': 'Building_A',
                                                           'geom_type': 'cube',
                                                           'coordinates': [[31.7, 13.5, 2.5]],
                                                           'data': {'side': [25, 5, 5], 'filled': True},
                                                           'color': [1, 120, 100]
                                                           },
                                                          {'name': 'Building_B',
                                                           'geom_type': 'cube',
                                                           'coordinates': [[44.0, -67.5, 7.5]],
                                                           'data': {'side': [15, 15, 15], 'filled': True},
                                                           'color': [255, 0, 0]
                                                           },
                                                          {'name': 'Sphere_A',
                                                           'geom_type': 'sphere',
                                                           'coordinates': [[-10.0, 10.0, 20.0]],
                                                           'data': {'radius': 20, 'filled': True},
                                                           'color': [200, 220, 100]
                                                           }
                                                          ]
                                                }
                           }
                }
    data_queue.put(handover)
    data_queue.put(handover)
    # for k in range(3):
    #     for i in range(0, 191):
    #         handover['active']['stored_selection']['1.1'][0]['coordinates'] = [[-95.0 + i, -95.0 + i, 0.0]]
    #         handover['active']['stored_selection']['1.1'][0]['color'] = [255, 0, 0]
    #         data_queue.put(copy.deepcopy(handover))
    #     for j in range(190, -1, -1):
    #         handover['active']['stored_selection']['1.1'][0]['coordinates'] = [[-95.0 + j, -95.0 + j, 0.0]]
    #         handover['active']['stored_selection']['1.1'][0]['color'] = [0, 0, 255]
    #         data_queue.put(copy.deepcopy(handover))

if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=put_data())
    process_1.start()
    GeneralDisplay.main(data_queue)