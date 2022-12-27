from beaker import *
from pyteal import *

class Bootcamp(Application):

    name = ApplicationStateValue(stack_type=TealType.bytes)

    @external
    def set_name(self, name:abi.String):
        return self.name.set(name.get())
    
    @external
    def get_name(self, *, output: abi.String):
        return output.set(self.name.get())
    
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

    @external
    def seq_expression(self, option: abi.String, *, output:abi.String):
        if_variable = If(Int(1) > Int(0), output.set(Bytes("True")), output.set(Bytes("False")))

        return Seq(
            if_variable,
            Cond(
                [option.get() == Bytes("A"), output.set(Bytes("A was selected"))],
                [option.get() == Bytes("B"), output.set(Bytes("B was selected"))]
            )
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
print(app_client.call(Bootcamp.seq_expression, option="A").return_value)
app_client.call(Bootcamp.set_name, name="Alejandro").return_value
print(app_client.call(Bootcamp.get_name).return_value)