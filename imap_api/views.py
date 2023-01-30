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
    current_cp = CheckPoint.objects.get(id_checkpoint=current_cp)
    final_cp = CheckPoint.objects.get(id_checkpoint=final_cp)

    all_cables: List[Cable] = list(Cable.objects.all())
    cables_routes = []
    route = []
    print('--------Checkpoints connectés-----------------')

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
        assert all(graph[u][v] >=0 for u in graph.keys() for v in graph[u].keys())
        precedent = {x: None for x in graph.keys()}
        dejaTraite = {x: False for x in graph.keys()}
        distance = {x: float('inf') for x in graph.keys()}
        distance[source] = 0
        a_traiter = [(0, source)]
        rt = []
        while a_traiter:
            dist_noeud, noeud = a_traiter.pop()
            if not dejaTraite[noeud]:
                dejaTraite[noeud] = True
                for voisin in graph[noeud].keys():
                    dist_voisin = dist_noeud + graph[noeud][voisin]
                    if dist_voisin < distance[voisin]:
                        distance[voisin] = dist_voisin

                        precedent[voisin] = noeud
                        a_traiter.append((dist_voisin, voisin))
            a_traiter.sort(reverse=True)
        return distance

    chemain = dijktra(graph=get_matrice(),source="A")
    print('*************************** chemains***********************************')
    print(chemain)
    def get_all_routes(current_check_point: CheckPoint, final_check_point: CheckPoint):


        return cables_routes
    get_all_routes(current_cp, final_cp)


def calcul_route_distances(routes: List[Route]):
    # Sort Routes for get must small distance
    for i in range(len(routes)):
        for j in range(len(routes), 0):
            if routes[j].distance > routes[i].distance:
                permut = routes[i]
                routes[i] = routes[j]
                routes[j] = permut
    return routes






