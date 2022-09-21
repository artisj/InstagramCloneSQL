from pymongo import MongoClient
from bson import ObjectId
import os


# start connection
def connect(db_name):
  client = MongoClient(os.environ['MONGODB_URI'])
  collection = client.insta[db_name]
  return collection
  
# create
def add_entry(db_name, entry):
  collection = connect(db_name)
  collection.insert_one(entry)
  collection.database.client.close

# update
def update_entry(db_name,id,update_entry):
  collection = connect(db_name)
  # if(ObjectId.is_valid(id) == False):
  #   return {'error': 'ObjectId is not valid', 'status': 404}

  try:
    check = collection.find_one_and_update({'_id': ObjectId(id)},{ '$set': update_entry})
    if(check == None):
      return {'error': 'Id not found', 'status': 404}
  except Exception as e:
    print(e)
    return {'error': str(e), 'status': 400}
  
# delete
def delete(db_name,id):
  collection = connect(db_name)
  collection.find_one_and_delete({'_id': ObjectId(id)})  

# read items
def list_items(db_name, id):
  collection = connect(db_name)
  collection.database.client.close
  return collection.find({'id': id})

def get_user_by(db_name, key,entry):
  collection = connect(db_name)
  if key == 'id':
    return collection.find_one({'_id': ObjectId(entry)})
  return collection.find_one({key: entry})