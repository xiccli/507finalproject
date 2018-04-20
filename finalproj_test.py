from finalproj_part2 import *
import unittest

class TestFinalProject(unittest.TestCase):

    def test_species_amount(self):
        self.assertEqual(len(species_dr), 100)

    def test_species_detail(self):
        self.assertEqual(species_dr["Giant Panda"]["Status"],"Vulnerable")
        self.assertEqual(species_dr["Sloth"]["Place"],"Amazon")
        self.assertEqual(species_dr["Tiger"]["Length"],"6–10 feet")
        self.assertTrue(species_dr["Jaguar"])

    def test_class(self):
        self.assertEqual(species_class_ls[0].scientificname,"Loxodonta africana")
        output_test="Albacore Tuna (Thunnus alalunga): Near Threatened animal, has a population of around None. It lives in habitats with Ocean Habitat, currently in The Galápagos, Coral Triangle, Coastal East Africa"
        self.assertEqual(species_class_ls[2].__str__(),output_test)
        self.assertEqual(species_class_ls[8].length,"around 21 feet")
        self.assertTrue(species_class_ls[-1].name,"Yellowfin Tuna")

    def test_db(self):
        try:
            print ("connect to local sql file...")
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
        except:
            print ("error")

        statement_test='''
            SELECT COUNT(*)
            FROM InfoVis
        '''
        result=cur.execute(statement_test).fetchone()[0]
        self.assertEqual(result,100)

        statement_test_02='''
            SELECT COUNT(*)
            FROM Species
        '''
        result_02=cur.execute(statement_test_02).fetchone()[0]
        self.assertEqual(result,100)

        statement_test_03='''
             SELECT *
             FROM InfoVis
                JOIN Species
                ON InfoVis.Name=Species.Name
	            WHERE Species.Status = "Endangered"
        '''
        result_03=cur.execute(statement_test_03).fetchall()
        self.assertEqual(len(result_03),27)
        conn.close()

    def test_show_map(self):
        try:
            plot_speciesloc()
        except:
            self.fail()

    def test_show_population(self):
        try:
            plot_population("Vulnerable")
        except:
            self.fail()

    def test_show_population_2(self):
        try:
            plot_population("Least Concern")
        except:
            self.fail()





if __name__ == '__main__':
    unittest.main()
