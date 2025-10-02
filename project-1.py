"""
Name: Blake Lovasz
Email: lovasz@umich.edu
ID: 7535 2261
"""
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
            self.dict[key].append(split[x])
    
    def build_dict(self):
        """
        Looping through the data to build
        the dictionairy.
        """
        for line in self.data[1:]:
            split = line.split(",")
            self.dict["num"].append(str(split[0]))
            self.dict["species"].append(str(split[1]))
            self.dict["island"].append(str(split[2]))
            self.checking_data(split, "bill len",3)
            self.checking_data(split, "bill depth", 4)
            self.checking_data(split, "flipper len", 5)
            self.checking_data(split, "body mass", 6)
            self.checking_data(split, "sex", 7)
            self.dict["year"].append(int(split[8]))
    
    def get_dict(self):
        """
        Returns the dictionairy.
        """
        return self.dict
    
    def i_avg_bill(self, island):
        """
        Returning the average bill length
        and depth based on the different
        island the penguins are on.

        Should return as a tupple.
        """
        sum_blen = 0
        sum_bdep = 0
        count = 0

        for i in range (0, len(self.dict["island"])):
            if self.dict["island"][i] == island:
                sum_blen += self.dict["bill len"][i]
                sum_bdep += self.dict["bill depth"][i]
                count += 1
        
        return (sum_blen / count, sum_bdep / count)


    def s_avg_bill(self, species):
        """
        Returning the average bill length
        and depth based on the different
        species of the penguins.

        Should return as a tupple.
        """
        sum_blen = 0
        sum_bdep = 0
        count = 0

        for i in range (0, len(self.dict["species"])):
            if self.dict["species"][i] == species:
                sum_blen += self.dict["bill len"][i]
                sum_bdep += self.dict["bill depth"][i]
                count += 1
        
        return (sum_blen / count, sum_bdep / count)

class TestPendata(unittest.TestCase):
    """
    A class for testing Pendata
    """
    def setUp(self):
        self.data = Pendata("penguins.csv")
        self.data.build_dict()

    def test_build_dict(self): # Edge Test #1
        """
        Testing the first 20 and last 20 datasets
        in the dictionairy.
        """
    def test_txtfile(self): # Edge Test #2
        """
        Testing if first two and last two
        lines are correct.
        """

    def test_s_avg_bill(self): # Gen Test #1
        """
        Testing if the tupple returned is correct
        """

    def test_i_avg_bill(self): #Gen Test #2
        """
        Testing if the tupple returned is correct
        """



def writing(penguin, fname):
    """
    Organizing the data of the average
    bill length and depth. Based on the
    island and species of the penguins.
    """
    file = open(fname,"w")
    dic = penguin.get_dict()
    s_used = []
    i_used = []

    file.write("Average Bill Length & Depth (mm) for Different Penguin Species:\n")
    for s in dic["species"]:
        if s not in s_used:
            len, dep = penguin.s_avg_bill(s)
            file.write(f"Species: {s} Bill Length: {len:.1f} Bill Depth: {dep:.1f}\n")
            s_used.append(s)

    file.write("\nAverage Bill Length & Depth (mm) for Penguins on Different Islands:\n")
    for i in dic["island"]:
        if i not in i_used:
            len,dep = penguin.i_avg_bill(i)
            file.write(f"Island: {i} Bill Length: {len:.1f} Bill Depth: {dep:.1f}\n")
            i_used.append(i)

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
    unittest.main()