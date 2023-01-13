from application.goods.model import get_traindata,\
                                    get_recordby_id,\
                                    post_train_model,\
                                    update_traindata,\
                                    delete_traindata                                    


# Validating the Get method
def get_validator_control():    
    return get_traindata()


# Validating the Get method
def get_singleid_control(id):
    return get_recordby_id(id)


# Validating the Get method
def post_validator_control():        
    return post_train_model()


# Validating the Get method
def put_validator_control(id):
    return update_traindata(id)    


# Validating the Get method
def del_validator_control(id):
    return delete_traindata(id)    
