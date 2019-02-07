from troposphere import Join, Ref, Template, GetAtt, Output, Tags
from troposphere.ec2 import VPC, InternetGateway, VPCGatewayAttachment

class SceptreRessource():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        if self.sceptre_user_data.pop("InternetGateway", False):
            self.add_igw()
        self.add_vpc()
        self.add_VPCGatewayAttachment()
        self.add_outputs()

    def add_vpc(self):
        # print self.sceptre_user_data
        self.vpc = self.template.add_resource(VPC(
            "VirtualPrivateCloud",
            **self.sceptre_user_data
        ))

    def add_igw(self):
        self.igw = self.template.add_resource(InternetGateway(
            "IGW",
            Tags=Tags(
                Name="IGW",
            ),
        ))

    def add_VPCGatewayAttachment(self):
        self.VPCGatewayAttachment = self.template.add_resource(VPCGatewayAttachment(
            "PubSubnetAssoc",
            InternetGatewayId=Ref(self.igw),
            VpcId=Ref(self.vpc)
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("VpcId", Value=Ref(self.vpc)),
            Output("IgwName", Value=Ref(self.igw)),
        ])

def sceptre_handler(sceptre_user_data):
    return SceptreRessource(sceptre_user_data).template.to_yaml()
