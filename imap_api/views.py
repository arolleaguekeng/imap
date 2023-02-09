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

@api_view(['GET'])
def get_routes(request, source, destination):
    print("--------------------------------------------------")
    print("******Chemains pour quitter de [{}] à [{}] *******".format(source, destination))
    print("--------------------------------------------------")
    print()

    # Pour retourner l'orientation inverse
    def orientation_inverse(orientation: str):

        # Dictionaire des orientations avec leur contraire
        dif_graph = [
            {"N": "S"},
            {"S": "N"},
            {"W": "E"},
            {"E": "W"},
            {"NW": "SE"},
            {"SW": "NE"},
            {"NE": "SW"},
            {"SE": "NW"},
        ]

        # Parcour le dictionnaire et retourne la valeure
        # de l'élément entrée en paramètre de la fonction
        for ortion in dif_graph:
            for i in ortion.keys():
                if i == orientation:
                    print(ortion.get(i))
                    return ortion.get(i)

    # Recupère tous les cables de la base de donnée
    all_cables: List[Cable] = list(Cable.objects.all())

    # Genere une matrice adjacente en fonction des Checkpoints
    def get_matrice():
        graph = {}
        # Recupère tous les cables de la base de donnée
        list_cp = list(CheckPoint.objects.all())
        for cp in list_cp:
            graph_item = {}
            # Parcour la liste des Checkpoints pour générer le graph
            for cable in all_cables:

                # initialisation du point actuel, de l'origine et de la destination
                current_cp = cp.id_checkpoint
                destination_cp = cable.id_cp_destination.id_checkpoint
                origin_cp = cable.id_cp_origine.id_checkpoint

                # si le point courant est égale au point destination
                # du du cable courrant, on ajoute le cable dans le dictionaire
                if destination_cp == current_cp:
                    graph_item[cable.id_cp_origine.id_checkpoint] = cable
                if origin_cp == current_cp:
                    graph_item[cable.id_cp_destination.id_checkpoint] = cable
                graph[cp.id_checkpoint] = graph_item

        return graph

    def dijkstra(graph: dict, start, goal):
        # stocke la plus petite distance
        shorted_distance = {}

        # stocke le point précédent
        track_predecessor = {}

        # stocke les noeux non visité
        unseenNodes = graph

        infity = 999999

        # Stocke le chemain le plus court
        track_path = []

        # Initialisation des plus petites distances
        for node in unseenNodes:
            shorted_distance[node] = infity

        # Initialise la plus petite distance de tous les points à 0
        shorted_distance[start] = 0

        # Vérifier si tous les noeuds ont été parcourus
        while unseenNodes:

            # Initialise la distance minimale du noeud à None
            min_distance_node = None

            # Parcoure les noeuds non consulté
            for node in unseenNodes:
                # Si
                if min_distance_node is None:
                    min_distance_node = node
                elif shorted_distance[node] < shorted_distance[min_distance_node]:
                    min_distance_node = node
                    print('*******************************************************')
                    print(type(min_distance_node))

            path_options = graph[min_distance_node].items()

            for child_node, weight in path_options:
                if weight.longr + shorted_distance[min_distance_node] < shorted_distance[child_node]:
                    shorted_distance[child_node] = weight.longr + shorted_distance[min_distance_node]
                    track_predecessor[child_node] = min_distance_node
            unseenNodes.pop(min_distance_node)
        current_Node = goal

        while current_Node != start:
            try:
                track_path.insert(0, CheckPoint.objects.get(id_checkpoint=current_Node))
                current_Node = track_predecessor[current_Node]
            except KeyError:
                print("Path is not reachable")
                break
        track_path.insert(0, CheckPoint.objects.get(id_checkpoint=start))

        if shorted_distance[goal] != infity:
            print("La plus petite distance est:  " + str(shorted_distance[goal]))
            print("Le meilleur chemain est:  " + str(track_path))

            return {"distance": shorted_distance[goal], "path": track_path}

    chemain = dijkstra(graph=get_matrice(), start=source, goal=destination)
    print(chemain)
    route = []
    # On parcoure la liste des cables qui constituent le chemain
    for i in range(len(chemain["path"]) - 1):
        cp = chemain["path"][i].id_checkpoint
        second_cp = chemain["path"][i + 1].id_checkpoint
        # Parcour la liste de tous les cables pour rechercher les cables de la route
        for cable in all_cables:
            cbl_o = cable.id_cp_origine.id_checkpoint
            cbl_d = cable.id_cp_destination.id_checkpoint

            # On vérifie si le cable fait partir des cables de la route
            if (cbl_o is cp or cbl_d is cp) and (cbl_o is second_cp or cbl_d is second_cp):

                # Si l'orignie du cable est un checkpoint de la route
                if cbl_o is cp:
                    pass

                # Si la destination du cable est le prochain
                else:
                    # Inverse l'origine du cable
                    inverse = orientation_inverse(cable.direction_origine)
                    cable.direction_origine = inverse
                route.append(cable)
    print(route)
    serializer = CableSerializer(route, many=True)
    chemain["route"] = serializer.data
    cp_serializer = CheckPointSerializer(chemain.get("path"), many=True)
    chemain["path"] = cp_serializer.data
    return Response(chemain)
