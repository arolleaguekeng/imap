from collections import deque

from rest_framework.decorators import api_view
from typing import List

from imap_api.serializers import *
from imap_api.services import *



# region Batiment views

# POST Batiment
@api_view(['POST'])
def batiment_save(request):
    return generic_post(request=request, obj_serializer=BatimentSerializer)


# Get All Batiments
@api_view(['GET'])
def batiment_list(request):
    return generic_get_all(request=request, obj=Batiment, obj_serializer=BatimentSerializer)


# Get Batiment By Id
@api_view(['GET'])
def batiment_detail(request, pk):
    return generic_get_by_id(request=request, pk=pk, obj=Batiment, obj_serializer=BatimentSerializer)


# Edit Batiment
@api_view(['PUT'])
def batiment_edit(request, pk):
    return generic_put(request=request, pk=pk, obj=Batiment, obj_serializer=BatimentSerializer)


# Delete Batiment
@api_view(['DELETE'])
def batiment_delete(request, pk):
    return generic_delete(request=request, pk=pk, obj=Batiment)


# endregion


# region Salles views

# POST Salle
@api_view(['POST'])
def salle_save(request):
    return generic_post(request=request, obj_serializer=SalleSerializer)


# Get All Salles
@api_view(['GET'])
def salle_list(request):
    return generic_get_all(request=request, obj=Salle, obj_serializer=SalleSerializer)


# Get Salle By Id
@api_view(['GET'])
def salle_detail(request, pk):
    return generic_get_by_id(request=request, pk=pk, obj=Salle, obj_serializer=SalleSerializer)


# Edit Salle
@api_view(['PUT'])
def salle_edit(request, pk):
    return generic_put(request=request, pk=pk, obj=Salle, obj_serializer=SalleSerializer)


# Delete Salle
@api_view(['DELETE'])
def salle_delete(request, pk):
    return generic_delete(request=request, pk=pk, obj=Salle)


# endregion


# region CheckPoint views

# POST CheckPoint
@api_view(['POST'])
def check_point_save(request):
    return generic_post(request=request, obj_serializer=CheckPointSerializer)


# Get All CheckPoint
@api_view(['GET'])
def check_point_list(request):
    return generic_get_all(request=request, obj=CheckPoint, obj_serializer=CheckPointSerializer)


# Get CheckPoint By Id
@api_view(['GET'])
def check_point_detail(request, pk):
    return generic_get_by_id(request=request, pk=pk, obj=CheckPoint, obj_serializer=CheckPointSerializer)


# Edit CheckPoint
@api_view(['PUT'])
def check_point_edit(request, pk):
    return generic_put(request=request, pk=pk, obj=CheckPoint, obj_serializer=CheckPointSerializer)


# Delete CheckPoint
@api_view(['DELETE'])
def check_point_delete(request, pk):
    return generic_delete(request=request, pk=pk, obj=CheckPoint)


# endregion


# region Cable views

# POST Cable
@api_view(['POST'])
def cable_save(request):
    return generic_post(request=request, obj_serializer=CableSerializer)


# Get All Cable
@api_view(['GET'])
def cable_list(request):
    return generic_get_all(request=request, obj=Cable, obj_serializer=CableSerializer)


# Get Cable By Id
@api_view(['GET'])
def cable_detail(request, pk):
    return generic_get_by_id(request=request, pk=pk, obj=Cable, obj_serializer=CableSerializer)


# Edit Cable
@api_view(['PUT'])
def cable_edit(request, pk):
    return generic_put(request=request, pk=pk, obj=Cable, obj_serializer=CableSerializer)


# Delete Cable
@api_view(['DELETE'])
def cable_delete(request, pk):
    return generic_delete(request=request, pk=pk, obj=Cable)


# endregion


# region Etage views

# POST Cable
@api_view(['POST'])
def etage_save(request):
    return generic_post(request=request, obj_serializer=EtageSerializer)


# Get All Etage
@api_view(['GET'])
def etage_list(request):
    get_routes("E", "C")
    return generic_get_all(request=request, obj=Etage, obj_serializer=EtageSerializer)


# Get Etage By Id
@api_view(['GET'])
def etage_detail(request, pk):
    return generic_get_by_id(request=request, pk=pk, obj=Etage, obj_serializer=EtageSerializer)


# Edit Etage
@api_view(['PUT'])
def etage_edit(request, pk):
    return generic_put(request=request, pk=pk, obj=Etage, obj_serializer=EtageSerializer)


# Delete Etage
@api_view(['DELETE'])
def etage_delete(request, pk):
    return generic_delete(request=request, pk=pk, obj=Etage)


# endregion


def get_routes(current_cp, final_cp):
    print("--------------------------------------------------")
    print("******Chemains pour quitter de [{}] à [{}] *******".format(current_cp, final_cp))
    print("--------------------------------------------------")
    print()

    all_cables: List[Cable] = list(Cable.objects.all())

    def get_matrice():
        graph = {}
        list_cp = list(CheckPoint.objects.all())
        for cp in list_cp:
            trs = {}
            for cable in all_cables:
                current_cp = cp.id_checkpoint
                destination_cp = cable.id_cp_destination.id_checkpoint
                origin_cp = cable.id_cp_origine.id_checkpoint
                if destination_cp == current_cp:
                    trs[cable.id_cp_origine.id_checkpoint] = cable.longr
                if origin_cp == current_cp:
                    trs[cable.id_cp_destination.id_checkpoint] = cable.longr
                graph[cp.id_checkpoint] = trs
        return graph


    def dijktra(graph: dict, source):
        print('--------Checkpoints connectés-----------------')
        print(graph)
        assert all(graph[u][v] >= 0 for u in graph.keys() for v in graph[u].keys())
        precedent = {x: None for x in graph.keys()}
        dejaTraite = {x: False for x in graph.keys()}
        distance = {x: float('inf') for x in graph.keys()}
        distance[source] = 0
        a_traiter = [(0, source)]
        n=0
        while a_traiter:
            dist_noeud, noeud = a_traiter.pop()
            if not dejaTraite[noeud]:
                dejaTraite[noeud] = True
                for voisin in graph[noeud].keys():
                    dist_voisin = dist_noeud + graph[noeud][voisin]

                    n = n+1
                    print(n)
                    if dist_voisin < distance[voisin]:
                        print('----------------------------')
                        print(print("{}".format(distance)))
                        distance[voisin] = dist_voisin
                        precedent[voisin] = noeud
                        a_traiter.append((dist_voisin, voisin))
            a_traiter.sort(reverse=True)
        return distance


    def dijkstraa(graph:dict, start, goal):
        shorted_distance = {}
        track_predecessor = {}
        unseenNodes = graph
        infity=999999
        track_path = []

        for node in unseenNodes:
            shorted_distance[node] = infity
        shorted_distance[start] = 0

        while unseenNodes:

            min_distance_node = None

            for node in unseenNodes:
                if min_distance_node is None:
                    min_distance_node = node
                elif shorted_distance[node] < shorted_distance[min_distance_node]:
                    min_distance_node = node

            path_options = graph[min_distance_node].items()

            for child_node, weight in path_options:

                if weight + shorted_distance[min_distance_node] < shorted_distance[child_node]:
                    shorted_distance[child_node] = weight + shorted_distance[min_distance_node]
                    track_predecessor[child_node] = min_distance_node
            unseenNodes.pop(min_distance_node)
        current_Node = goal

        while current_Node != start:
            try:
                track_path.insert(0, current_Node)
                current_Node = track_predecessor[current_Node]
            except KeyError:
                print("Path is not reachable")
                break

        track_path.insert(0, start)

        if shorted_distance[goal] != infity:
            print("shotest distance is" + str(shorted_distance[goal]))
            print("Le meilleur chemain e" + str(track_path))


    chemain = dijkstraa(graph=get_matrice(), start="B", goal="D")
    print('*************************** chemains ***********************************')
    print(chemain)



