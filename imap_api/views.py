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
    get_routes("CPB0", "CPA1")
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


def get_routes(current_cp_id, final_cp_id):
    n = 0
    final_cp_id = final_cp_id
    routes_cables = []

    all_cables: List[Cable] = Cable.objects.all()
    for cable in cables:
        destination = cables[i].id_cp_destination
        destination = destination.id_checkpoint
        current_route = []
        print("*******************destinations*******************")
        print(destination)
        if destination == current_cp_id:
            if destination == final_cp_id:
                routes_cables.append(current_route)
                n += 1
                continue

            current_route.append(cables[i].id_cp_destination)
            get_routes(destination, final_cp_id)
            print(current_route)
        else:
            print("//////////////////////////////////////////////")
            print(current_cp_id)
            print("*******************          not destination          *******************")
            print(destination)

    def get_all_routes(current_check_point: CheckPoint):
        cables_routes = []
        for cable in all_cables:
            if cable.id_cp_origine is current_check_point:
                cables_routes.append(cable)
                all_cables.remove(cable)
                get_all_routes(cable.id_cp_destination)

            if cable.id_cp_destination is current_check_point:
                cables_routes.append(cable)
                all_cables.remove(cable)
                get_all_routes(cable.id_cp_origine)
    return routes_cables


def calcul_route_distances(routes_cables: [[]]):
    distances = []
    chemins_possible = {}
    for i in range(0, len(routes_cables)):
        chemins_possible[routes_cables[i]] = 0
    for cables in routes_cables:
        distance = 0
        for cable in cables:
            distance += cable.longr
        chemins_possible[cables] = distance
    distances.sort()

    return distances

