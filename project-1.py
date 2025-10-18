"""
Name: Blake Lovasz
Email: lovasz@umich.edu
ID: 7535 2261
Did not use GenAI
"""
#FINAL SUBMITION:
import os
import unittest

class Pendata():
    """
    A class for reading and getting averages
    from the data.
    """
    def __init__(self, file):
        """
        Opening the csv file.
        Creating the empty dictionairy.

        file (string) is the name of the file we're opening 
        """
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, file)

        self.fileobj = open(self.full_path)
        self.data = self.fileobj.readlines()
        self.fileobj.close()

        self.dict = {
            "num": [],
            "species": [],
            "island": [],
            "bill len": [], # measured in milimeters
            "bill depth": [], # measured in milimeters
            "flipper len": [], # measured in milimeters
            "body mass":  [],
            "sex": [],
            "year": []
        }

    def checking_data(self, split, key, x):
        """
        Checking if data == NA

        split (list) is a line in the file seperated by commas
        key (string) is the key name we're going to access in the dictionairy
        x (int) is the index in split we're pulling from 
        """
        if split[x] == "NA":
            if key == "sex":
                self.dict[key].append("x")
            else:
                self.dict[key].append(0)
        elif key == "bill len" or key == "bill depth":
            self.dict[key].append(float(split[x]))
        elif key == "flipper len" or key =="body mass":
            self.dict[key].append(int(split[x]))
        else:
            self.dict[key].append(str(split[x].strip('"')))
    
    def build_dict(self):
        """
        Looping through the data to build
        the dictionairy.
        """
        for line in self.data[1:]:
            split = line.split(",")
            self.dict["num"].append(str(split[0].strip('"')))
            self.dict["species"].append(str(split[1].strip('"')))
            self.dict["island"].append(str(split[2].strip('"')))
            self.checking_data(split, "bill len",3)
            self.checking_data(split, "bill depth", 4)
            self.checking_data(split, "flipper len", 5)
            self.checking_data(split, "body mass", 6)
            self.checking_data(split, "sex", 7)
            self.dict["year"].append(int(split[8]))

    def s_avg_bill(self, species):
        """
        Returning the average bill length
        and depth based on the different
        species of the penguins.

        Should return as a tupple.

        species (string) the name of the species we're looking at
        """
        sum_blen = 0
        sum_bdep = 0
        blencount = 0
        bdepcount = 0

        for i in range (0, len(self.dict["species"])):
            if self.dict["species"][i] == species:
                if self.dict["bill len"][i] != 0: 
                    sum_blen += self.dict["bill len"][i]
                    blencount += 1
                if self.dict["bill depth"][i] != 0:
                    sum_bdep += self.dict["bill depth"][i]
                    bdepcount += 1
        
        x = sum_blen/blencount
        y = sum_bdep/bdepcount
        
        return (round(x,2), round(y,2))
    
    def flipper_sex(self, species): #changed name from flowchart after remembering its sex and not gender
        """
        Getting avg flipper length by sex for each species

        Species (string) name of the species we're looking at
        """
        m = 0
        m_count = 0
        f = 0
        f_count = 0
        x = 0
        x_count = 0

        for s in range(0, len(self.dict["species"])):
            if self.dict["species"][s] == species:
                if self.dict["sex"][s] == "male":
                    if self.dict["flipper len"][s] != 0:
                        m += self.dict["flipper len"][s]
                        m_count += 1
                elif self.dict["sex"][s] == "female":
                    if self.dict["flipper len"][s] != 0:
                        f += self.dict["flipper len"][s]
                        f_count += 1
                elif self.dict["sex"][s] == "x": 
                    if self.dict["flipper len"][s] != 0:
                        x += self.dict["flipper len"][s]
                        x_count += 1
        
        avg_m = m/m_count
        avg_f = f/f_count
        if x_count != 0:
            avg_x = x/x_count
        else:
            avg_x = 0

        return (round(avg_m, 2), round(avg_f, 2), round(avg_x, 2))

class TestPendata(unittest.TestCase):
    """
    A class for testing Pendata
    """
    def setUp(self):
        self.penguin = Pendata("penguins.csv")
        self.penguin.build_dict()

        self.species1 = "Adelie"
        self.species2 = "Gentoo"
        self.species3 = "Chinstrap"

    def test_build_dict(self): # Edge Test #1
        """
        Testing the first 5 and last 5 datasets
        in the dictionairy. As well the correct amount
        of data points entered.
        """
        self.assertEqual(len(self.penguin.dict["species"]),344)
        self.assertEqual(len(self.penguin.dict["bill len"]),344)
        self.assertEqual(self.penguin.dict["bill len"][:5],
                         [39.1,39.5,40.3,0.0,36.7])
        self.assertEqual(self.penguin.dict["bill len"][-5:],
                         [55.8,43.5,49.6,50.8,50.2])
        self.assertEqual(self.penguin.dict["bill depth"][:5],
                         [18.7,17.4,18.0,0.0,19.3])
        self.assertEqual(self.penguin.dict["bill depth"][-5:],
                         [19.8,18.1,18.2,19.0,18.7])
        self.assertEqual(self.penguin.dict["sex"][-5:],
                        ["male", "female", "male", "male", "female"])
        self.assertEqual(self.penguin.dict["sex"][:5],
                         ["male","female","female", "x", "female"])

    def test_txtfile(self): # Edge Test #2
        """
        Testing if first two and last two
        lines are correct.
        """
        file = open("avg.txt")
        f = file.readlines()

        self.assertEqual(f[:2],["Average Bill Length & Depth (mm) for Different Penguin Species:\n",
                                "Species: Adelie Bill Length: 38.79 Bill Depth: 18.35\n"])
        self.assertEqual(f[-2:],["Species: Gentoo M: 221.54 F: 212.71 Other: 215.75\n",
                                 "Species: Chinstrap M: 199.91 F: 191.74 Other: 0\n"]) 
        file.close()

    def test_s_avg_bill(self): # Gen Test #1
        """
        Testing if the tupple returned is correct
        """
        self.assertEqual(self.penguin.s_avg_bill(self.species1), (38.79,18.35))
        self.assertEqual(self.penguin.s_avg_bill(self.species2), (47.5,14.98))
        self.assertEqual(self.penguin.s_avg_bill(self.species3), (48.83,18.42))

    def test_flipper_sex(self): # Gen Test #2
        """
        Testing if tupple returned is correct
        """
        self.assertEqual(self.penguin.flipper_sex(self.species1), (192.41,187.79,185.6))
        self.assertEqual(self.penguin.flipper_sex(self.species2), (221.54,212.71,215.75))
        self.assertEqual(self.penguin.flipper_sex(self.species3), (199.91, 191.74, 0))

def writing(penguin, fname):
    """
    Organizing the data of the average
    bill length and depth. Based on the
    island and species of the penguins.

    penguin (object) is the object we're using
    fname (string) is the file name
    """
    file = open(fname,"w")
    dic = penguin.dict
    s_used = []

    file.write("Average Bill Length & Depth (mm) for Different Penguin Species:\n")
    for s in dic["species"]:
        if s not in s_used:
            len, dep = penguin.s_avg_bill(s)
            file.write(f"Species: {s} Bill Length: {len} Bill Depth: {dep}\n")
            s_used.append(s)

    s_used = []

    file.write("\nAverage Flipper Length for Each Species' Sex:\n")
    for s in dic["species"]:
        if s not in s_used:
            m, f, x = penguin.flipper_sex(s)
            file.write(f"Species: {s} M: {m} F: {f} Other: {x}\n")
            s_used.append(s)

    file.close()
    return file

def main():
    """
    Creating a Pendata object.
    Sending that object to writing with txt file.
    """
    penguin = Pendata("penguins.csv")
    penguin.build_dict()

    writing(penguin, "avg.txt")
    f = open("avg.txt")
    for line in f.readlines():
        print(line)
    f.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)