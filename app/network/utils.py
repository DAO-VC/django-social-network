from network.models import Network
import random


class ConnectNetwork(object):
    def __init__(self):
        self.all_networks_queryset = Network.objects.all()

    def connect_to_new_network(self, network: Network):
        while True:
            try:
                random_network = random.choice(self.all_networks_queryset)
            except IndexError:
                break

            network.connect_network = random_network
            break

    def connect_all(self) -> None:

        for network in self.all_networks_queryset:
            while True:
                random_network = random.choice(self.all_networks_queryset)
                if network.connect_network:
                    if random_network.id != network.connect_network.id:
                        network.connect_network = random_network
                        network.save()
                        break
                else:
                    network.connect_network = random_network
                    network.save()
                    break
