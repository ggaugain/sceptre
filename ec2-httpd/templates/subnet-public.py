from troposphere import Join, Ref, Template, GetAtt, Output
from troposphere.ec2 import Subnet, RouteTable, Route, SubnetRouteTableAssociation

class SceptreRessource():
    def __init__(self, sceptre_user_data):
        self.sceptre_user_data = sceptre_user_data
        self.template = Template()
        self.igw_id = self.sceptre_user_data.pop("GatewayId")
        self.add_subnet_public()
        self.add_route_table()
        self.add_pub_route()
        self.add_SubnetRouteTableAssociation()
        self.add_outputs()

    def add_subnet_public(self):
        # print self.sceptre_user_data
        self.Subnet = self.template.add_resource(Subnet(
            "Subnets",
            **self.sceptre_user_data
            # call add_igw_route
        ))

    def add_route_table(self):
        # print self.sceptre_user_data
        self.PublicRouteTable = self.template.add_resource(RouteTable(
            "PublicRouteTable",
            VpcId=self.sceptre_user_data.get("VpcId")
        ))

    def add_pub_route(self):
        self.PublicRoute = self.template.add_resource(Route(
            "PublicRoute",
            GatewayId=self.igw_id,
            DestinationCidrBlock="0.0.0.0/0",
            RouteTableId=Ref(self.PublicRouteTable),
        ))

    def add_SubnetRouteTableAssociation(self):
        # print self.sceptre_user_data
        self.SubnetRouteTableAssociation = self.template.add_resource(SubnetRouteTableAssociation(
            "PubSubnetAssoc",
            SubnetId=Ref(self.Subnet),
            RouteTableId=Ref(self.PublicRouteTable)
        ))

    def add_outputs(self):
        self.out = self.template.add_output([
            Output("SubnetId", Value=Ref(self.Subnet)),
            Output("RouteTable", Value=Ref(self.PublicRouteTable)),
            Output("SubnetRouteTableAssociation", Value=Ref(self.SubnetRouteTableAssociation)),
        ])

def sceptre_handler(sceptre_user_data):
    return SceptreRessource(sceptre_user_data).template.to_yaml()
