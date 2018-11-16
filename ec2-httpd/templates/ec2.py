from troposphere import Join, Ref, Template, GetAtt, Output, Base64
from troposphere.ec2 import Instance

class EC2Instance():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.add_instance()
        self.add_outputs()

    def add_instance(self):
        # print self.sceptre_user_data
        if "UserData" in self.sceptre_user_data:
            path = self.sceptre_user_data.get("UserData").pop("Path")
            with open(path) as f:
                userdata = Base64(f.read())
            self.sceptre_user_data.update({"UserData": userdata})
        self.ec2 = self.template.add_resource(Instance(
            "EC2Instance",
            **self.sceptre_user_data
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("Ref", Value=Ref(self.ec2)),
            Output("AvailabilityZone", Value=GetAtt(self.ec2, "AvailabilityZone")),
            Output("PrivateDnsName", Value=GetAtt(self.ec2, "PrivateDnsName")),
            Output("PublicDnsName", Value=GetAtt(self.ec2, "PublicDnsName")),
            Output("PrivateIp", Value=GetAtt(self.ec2, "PrivateIp")),
            Output("PublicIp", Value=GetAtt(self.ec2, "PublicIp")),
        ])

def sceptre_handler(sceptre_user_data):
    return EC2Instance(sceptre_user_data).template.to_yaml()
