from network.models import Network
import random


class ConnectNetwork(object):
    def connect_all(self) -> None:
        all_networks_queryset = Network.objects.all()
        list_id_networks = [item.id for item in Network.objects.all()]

        for network in all_networks_queryset:
            while True:
                random_network_id = random.choice(list_id_networks)
                if random_network_id != network.connect_network.id:
                    network.connect_network.id = random_network_id
                    network.save()
                    break
