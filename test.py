from src.main import SVBACH


# create ach
def create_ach():
    ach = SVBACH(api_key="test_8697fFXs8T89MQrhbVWJgjath9rljPys",
                 api_secret="Fg6BJMjck4ebzKRrfP4p2ZHCUygLYSdBInMGkqVjhlheeoEjjoN6ESIXsnZV+cV6",
                 env="sandbox",
                 account_number="111111111",
                 amount=10003,
                 direction="credit",
                 receiver_account_number="2222220",
                 receiver_account_type="checking",
                 receiver_name="George Kane",
                 receiver_routing_number="321081669",
                 sec_code="ppd",
                 )
    print(ach.create_ach())


# retrieve ach
def retrieve_ach():
    ach = SVBACH(api_key="test_8697fFXs8T89MQrhbVWJgjath9rljPys",
                 api_secret="Fg6BJMjck4ebzKRrfP4p2ZHCUygLYSdBInMGkqVjhlheeoEjjoN6ESIXsnZV+cV6",
                 env="sandbox",
                 ach_id=24833,
                 )
    print(ach.retrieve_ach())


# update ach
def update_ach():
    ach = SVBACH(api_key="test_8697fFXs8T89MQrhbVWJgjath9rljPys",
                 api_secret="Fg6BJMjck4ebzKRrfP4p2ZHCUygLYSdBInMGkqVjhlheeoEjjoN6ESIXsnZV+cV6",
                 env="sandbox",
                 ach_id=24833,
                 status="canceled"
                 )
    print(ach.update_ach())


# list ach
def list_ach():
    ach = SVBACH(api_key="test_8697fFXs8T89MQrhbVWJgjath9rljPys",
                 api_secret="Fg6BJMjck4ebzKRrfP4p2ZHCUygLYSdBInMGkqVjhlheeoEjjoN6ESIXsnZV+cV6",
                 env="sandbox",
                 )
    print(ach.list_ach())


if __name__ == "__main__":
    # create_ach()
    retrieve_ach()
    # update_ach()
    # list_ach()
