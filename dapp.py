from beaker import *
from pyteal import *

class Bootcamp(Application):
    
    @create
    def create(self):
        return Approve()

    @external
    def hello_name(self, name: abi.String, *, output: abi.String):
        return output.set(Concat(Bytes("Hello "), name.get()))

    @external
    def hello_sender(self, *, output: abi.Address):
        return output.set(Txn.sender())
    
    @external
    def if_condition(self, *, output:abi.String):
        return If(Int(1) > Int(0), output.set(Bytes("True")), output.set(Bytes("False")))
    
    @external 
    def cond_expression (self, option: abi.String, *, output:abi.String):
        return Cond(
            [option.get() == Bytes("A"), output.set(Bytes("A was selected"))],
            [option.get() == Bytes("B"), output.set(Bytes("B was selected"))]
        )

app = Bootcamp(version=8)
app.dump()

creator = sandbox.kmd.get_accounts()[0]

app_client = client.application_client.ApplicationClient(
    client=sandbox.clients.get_algod_client(),
    app=app,
    sender=creator.address,
    signer=creator.signer,
)

app_client.create()

print(app_client.call(Bootcamp.hello_name, name="Camilo").return_value)
print(app_client.call(Bootcamp.hello_sender).return_value)
print(app_client.call(Bootcamp.if_condition).return_value)
print(app_client.call(Bootcamp.cond_expression, option="A").return_value)