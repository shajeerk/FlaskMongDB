from pymongo import MongoClient


class MongoDB:
    
    def __init__(self):
        self.client = MongoClient('10.161.113.156', 27017)
        self.db = self.client.openstack
        
    
    def check_user(self,user,password):
        try:
            res = self.db.users.find_one({"username":str(user),"password":str(password)})
            return res
        except Exception as e:
            print(e)
            
            
    def check_access_right(self,user):
        try:
            res = self.db.users.find_one({"username":str(user),"is_admin":"True"})
            return res
        except Exception as e:
            print(e)
    
    
    def set_user(self,val):
        
        try:
            res = self.check_user(val.get("username"),val.get("password"))
            if not res:
                res = self.db.users.insert_one(val)
            else:
                return "user already exits"
        except Exception as e:
            print(e)
                
        return True
    
    
    def group_list(self):
        l1 = []
        try:
            res = self.db.groups.find({}, {"_id":0})
            for i in res:
                l1.append(i['name'])
            return l1
                
        except Exception as e:
            print(e)
            
            
    def users_list(self):
        l1 = []
        try:
            res = self.db.users.find({}, {"_id":0})
            for i in res:
                l1.append(i)
            return l1
                
        except Exception as e:
            print(e)
            
    
    
    def check_group(self,group):
        try:
            res = self.db.groups.find_one({"name":str(group)})
            return res
        except Exception as e:
            print(e)
    
    
    def set_group(self,group):
        
        try:
            res = self.check_group(group)
            if not res:
                res = self.db.groups.insert_one(
                    {
                    "name": group
                    })
            else:
                return "group already exits"
        except Exception as e:
            print(e)
                
        return True
    
    
    def set_collection(self,val):
        
        try:
            res = self.check_collection(val.get("phone"))
            if not res:
                res = self.db.collections.insert_one(val)
            else:
                return "Phone already exists"
        except Exception as e:
            print(e)
                
        return True