import re
import string
from tinydb import TinyDB
from pathlib import Path
from typing import List
class User:

    db = TinyDB(Path(__file__).resolve().parent /'base.json', indent=4)
    def __init__(self,first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.address=address
    def __repr__(self):
        return f"User({self.first_name} {self.last_name})"
    def __str__(self):
        return f"({self.full_name} \n {self.phone_number} \n {self.address})"
    @property
    def full_name(self):
        return f"({self.first_name} {self.last_name})"
    @property
    def db_instance(self):
        return User.db.get((where('first_name')== self.first_name) & where('last_name')==self.last_name)
    #on creer une methode ki va appeler les 2 autres sans kon ai besoin de les appele un a un
    def check(self):
        self._check_names()
        self._check_phone_number()

    #la methode ki permet de verifier le numero de telephone est valide
    def _check_phone_number(self):
        #on import re , ki va nous permettre de rechercher des caracteres si trouver on le les
        #rejette de notre phone number
        phone_numero=re.sub(r"[+()\s]*", "", self.phone_number)
        #print(phone_digist)
        # si la longueur de phone digist <10 ou ne contient pas ke des nombres on leve une erreur
        if len(phone_numero) < 10 or not phone_numero.isdigit():
            raise ValueError(f"(Numero de telephone est invalid.)")
        
 # il va rechercher ses differents caractere dans phone number et replacer par: "" chaine vide
# on a mis phone number pour specifier sur koi nous allons effectuer ses actions
    def _check_names(self):
        if not(self.first_name and self.last_name):
            raise ValueError(f"(le prenom et le nom ne peuvent pas etre vide)")
        caractere_speciaux = string.punctuation + string.digits
        #print(caractere_speciaux)
        for character in self.last_name + self.first_name:
            if character in caractere_speciaux:
                raise ValueError("Nom invalid")
    #methode pour verifier si l'utilisateurs exis
    def exist(self):
        #si un user existe il renvoi true sinon false
        return bool(self.db_instance)
    
    #methode pour supprimer un utilisateur
    def delete(self) ->List[int]:
        if self.exist():
           return User.db.remove(doc_ids=[self.db_instance.doc_id])
        return[]
    
    #sauvegarder les donnees dans notre base de donnee
    def save(self, validate_data: bool=False) -> int:
        if validate_data:
            self.check()
        if self.exist():
            return -1
        else:
            User.db.insert(self.__dict__)
#on definit une methode ki recupere tous les users de la bd
def allUsers():
    return [User(**user) for user in User.db.all()]
for user in User.db.all():
    each_user = User(**user)
    print(User.db.all())
        

if __name__=="__main__":

    cece = User("cece djibril","pricemou")
    print(cece.db_instance )
    #allUsers()
#     #faker permet de generer des donnees aleatoires
#     from faker import Faker
#     fake= Faker(locals="fr_FR")
#     user=User(
#             first_name="cece djibril ",#fake.last_name()
#             last_name="pricemou",#fake.last_name()
#             phone_number="627082601",
#             address="Conakry"
#     )
#    # print(string.punctuation)
#     #print(string.digits)
#     #print(user)
#     #user._check_phone_number()
#     #user._check_names()
#         #print(repr(user))
#         #user.first_name="cece djibril"
#         #print(user.full_name)
#     #user.save(validate_data=True)
#     print(user.save())
#     print("_"*10)