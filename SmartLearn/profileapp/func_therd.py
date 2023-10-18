from .DecoratorTheard import threaClass


@threaClass
def thears(data):
    users_by_cabinet = {}
    for cabinet in data:
        users_by_cabinet[cabinet] = cabinet.users.filter(is_teacher=False)
    return users_by_cabinet



def main(data):
    process = thears(data)
    end_process = process.join()
    return end_process