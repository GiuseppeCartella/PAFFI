from abc import ABC, abstractmethod
from collections import defaultdict
from operator import attrgetter
import copy
from paffi.linkCollection import LinkCollection


class ConnectionPolicy(ABC):
    @abstractmethod
    def connect(self, topology):
        pass

    def connect_for_same_type(self, collection):
        final_dict = {link.get_label(): link for link in collection.topology_components.values() if link.get_src_node() != link.get_dst_node()}
        return final_dict


class NaiveConnection(ConnectionPolicy):
    def __init__(self):
        pass

    def connect(self, topology):
        topology.set_connection_type("naive")
        final_dict = {}
        groups = defaultdict(list)  # SERVE PER POTER CREARE DEI RAGGRUPPAMENTI

        for collection in topology.collections.values():
            if collection.get_type().startswith("delay_"):
                link_collection = LinkCollection(collection.get_type().replace("delay_", "conn_"))

                if collection.get_src_type() == collection.get_dst_type():
                    # sono di fronte ad un caso sensors_sensor o fog_fog per esempio
                    link_collection.populate(self.connect_for_same_type(collection))
                    final_dict[link_collection.get_type()] = link_collection
                    continue

                for obj in collection.topology_components.values():
                    groups[obj.get_src_node().get_number()].append(obj)

                for grouped_links in groups.values():
                    link_collection.add(min(grouped_links, key=attrgetter("delay")))

                final_dict[link_collection.get_type()] = link_collection
                groups.clear()
        topology.collections.update(final_dict)


class AMPLConnection(ConnectionPolicy):
    def __init__(self, ampl_out):
        self.ampl_out = ampl_out

    def parse_ampl_id(self, w):
        if w.startswith(("s", "f", "c")):
            return int(w[1:])
        else:
            return None

    def read_ampl_solution(self, ampl_out, variable):
        solution = {}
        compformat = True
        with open(ampl_out, "r") as f:
            for line in f:
                if variable in line:
                    break
            for line in f:
                if ";" in line:
                    break
                if line.startswith(":"):
                    compformat = False
                else:
                    ww = line.split()
                    if compformat:
                        id1 = self.parse_ampl_id(ww[0])
                        id2 = self.parse_ampl_id(ww[1])
                        solution[str(id1)] = id2
                    else:
                        id = self.parse_ampl_id(ww[0])
                        solution[str(id)] = ww.index("1") - 1
        return solution

    def save_set(self, fout, setname, set):
        out = "set %s :=" % setname
        for i in set.topology_components.values():
            out = out + (" %s%s" % (setname.lower(), i.get_number()))
        out = out + ";\n"

        fout.write(out)

    def save_param(self, topology, nodetype, fout, param):
        out = "param %s :=\n" % param
        node_collection = topology.get_child(nodetype)
        for i in node_collection.topology_components.values():
            out = out + ("\t%s%s\t%s\n" % (nodetype[0], i.get_number(), getattr(i, param)))
        out = out + ";\n"

        fout.write(out)

    def save_distance(self, topology, delaytype, fout, pname):
        out = "param %s :=\n" % pname
        link_collection = topology.get_child(delaytype)
        for i in link_collection.topology_components.values():
            out = out + ("\t%s%s\t%s%s\t%f\n" % (
            pname.split("_")[1][0], i.get_src_node().get_number(), pname.split("_")[1][1], i.get_dst_node().get_number(), i.get_delay()))
        out = out + ";\n"

        fout.write(out)

    def write_ampl_data(self, topology):
        with open("%s.dat" % self.ampl_out, "w") as fout:
            # dump data
            # sets of sources, fog nodes, cloud
            for key, value in topology.collections.items():
                if not key.startswith(("delay_", "conn_")):
                    self.save_set(fout, key[0].upper(), value)

            # parameters lambda, mu
            self.save_param(topology, 'sensors', fout, 'lambda_sens')
            self.save_param(topology, 'fog', fout, 'mu')

            # source-to-fog and fog-to-cloud distances
            self.save_distance(topology, "delay_sensors_fog", fout, "distance_sf")
            self.save_distance(topology, 'delay_fog_cloud', fout, 'distance_fc')

    def connect(self, topology):
        topology.set_connection_type("ampl")

        link_sens_fog = LinkCollection("conn_sensors_fog", "sensors", "fog")
        del_sens_fog = topology.get_child("delay_sensors_fog")
        solution = self.read_ampl_solution(self.ampl_out, "X[s,f]")

        for src, dst in solution.items():
            # bisogna ora creare i link
            link = copy.deepcopy(del_sens_fog.get_child(str(src) + "_" + str(dst)))
            link_sens_fog.add(link)

        topology.add(link_sens_fog)

        link_fog_cloud = LinkCollection("conn_fog_cloud", "fog", "cloud")
        del_fog_cloud = topology.get_child("delay_fog_cloud")
        solution = self.read_ampl_solution(self.ampl_out, "Y[f,c]")

        for src, dst in solution.items():
            # bisogna ora creare i link
            link = copy.deepcopy(del_fog_cloud.get_child(str(src) + "_" + str(dst)))
            link_fog_cloud.add(link)

        topology.add(link_fog_cloud)

        link_fog_fog = LinkCollection("conn_fog_fog", "fog", "fog")
        coll_fog_fog = topology.get_child("delay_fog_fog")
        link_fog_fog.populate(self.connect_for_same_type(coll_fog_fog))
        topology.add(link_fog_fog)