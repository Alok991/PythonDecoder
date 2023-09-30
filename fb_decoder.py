import flatbuffers
from fb import Client, ClientType, Group, Person, Gender
import sys


if len(sys.argv) < 2:
    print("Usage : ./fb_decoder.py <path-to-file.bin>")
    sys.exit(1)

fb_bin_file = sys.argv[1]


def deserialize_and_print(flatbuffer_data):
    client = Client.Client.GetRootAs(flatbuffer_data, 0)
    if client.ClientTypeType() == ClientType.ClientType().Person:
        p = Person.Person()
        p.Init(client.ClientType().Bytes, client.ClientType().Pos)
        gender = "Male" if p.Gender()==0 else "Female"
        print(f"{{{p.Name().decode('utf-8')}, {p.Age()}, {p.Weight()}, {gender}}}")
    if client.ClientTypeType() == ClientType.ClientType().Group:
        g = Group.Group()
        g.Init(client.ClientType().Bytes, client.ClientType().Pos)
        
        all_names = []
        for i in range(0, g.NamesListLength()):
            all_names.append(g.NamesList(i).decode('utf-8'))

        print(f"{{{ g.GroupName().decode('utf-8')}, {g.AverageAge()}, {g.AverageWeight()}, {{{  ','.join(all_names)  }}}}}")
    
#{FightClub, 24.5, 66, {Ram, Shayam, Raghuveer} }

with open(fb_bin_file, "rb") as bin_file:
    buffer = bin_file.read()
    idx = 0
    total_sz = len(buffer)
    
    while idx < total_sz:
        # read size of buffer
        size_of_buffer = int.from_bytes(buffer[idx:idx+8], "little")
        idx += 8
        flatbuffer_data = buffer[idx:idx+size_of_buffer]
        idx=idx+size_of_buffer
        deserialize_and_print(flatbuffer_data)
