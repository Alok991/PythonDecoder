import flatbuffers
from fb import Client, ClientType, Group, Person, Gender
import sys


if len(sys.argv) < 2:
    print("Usage : ./fb_decoder.py <path-to-file.bin>")
    sys.exit(1)

fb_bin_file = sys.argv[1]

with open(fb_bin_file, "rb") as bin_file:
    flatbuffer_data = bin_file.read()

    # import ipdb;ipdb.set_trace()
    client = Client.Client.GetRootAs(flatbuffer_data, 0)
    if client.ClientTypeType() == ClientType.ClientType().Person:
        p = Person.Person()
        p.Init(client.ClientType().Bytes, client.ClientType().Pos)
        gender = "Male" if p.Gender()==0 else "Female"
        print(f"{{{p.Name().decode('utf-8')}, {p.Age()}, {p.Weight()}, {gender}}}")


    client = Client.Client.GetRootAs(flatbuffer_data, p.PersonLength())
    if client.ClientTypeType() == ClientType.ClientType().Group:
        g = Group.Group()
        g.Init(client.ClientType().Bytes, client.ClientType().Pos)
        print(g.GroupName())
    

