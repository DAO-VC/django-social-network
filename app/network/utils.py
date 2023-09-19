from network.models import Network
import random


class ConnectNetwork(object):
    def connect_all(self) -> None:
        all_networks_queryset = Network.objects.all()
        # list_id_networks = [item for item in Network.objects.all()]

        for network in all_networks_queryset:
            while True:
                random_network = random.choice(all_networks_queryset)
                if network.connect_network:
                    if random_network.id != network.connect_network.id:
                        network.connect_network.id = random_network.id
                        network.save()
                        break
                else:
                    network.connect_network = random_network
                    network.save()
                    break
